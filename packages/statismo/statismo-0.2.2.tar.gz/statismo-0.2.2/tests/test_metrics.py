import pytest
from unittest.mock import patch, MagicMock

from statismo.metrics import push_metric, Dimension
from statismo.models import Unit, Metric
from statismo.collectors.db import DatabaseCollector
from statismo.collectors.redis import RedisCollector


@pytest.mark.django_db
def test_push_metric_with_db_collector():
    """Test that push_metric correctly stores data in the database."""
    with patch("statismo.metrics.collector", return_value=DatabaseCollector()):
        push_metric(
            key="test_metric",
            value=42.0,
            unit=Unit.COUNT_PER_SECOND,
            dimensions=[Dimension(name="service", value="test")],
        )

        metric = Metric.objects.get(key="test_metric")
        assert metric.value == 42.0
        assert metric.unit == "20"  # Unit.COUNT_PER_SECOND value as string
        assert len(metric.dimensions) == 1
        assert metric.dimensions[0]["name"] == "service"
        assert metric.dimensions[0]["value"] == "test"

        push_metric(
            key="test_metric",
            value=8.0,
            unit=Unit.COUNT_PER_SECOND,
            dimensions=[Dimension(name="service", value="test")],
        )

        metric.refresh_from_db()
        assert metric.value == 50.0


@pytest.mark.django_db
@pytest.mark.redis
def test_push_metric_with_redis_collector():
    """Test that push_metric correctly stores data in Redis using a mock."""
    # Skip if redis is not installed
    pytest.importorskip("redis")

    # Mock Redis client
    mock_redis = MagicMock()
    mock_redis.keys.return_value = [b"statismo:metrics:test_metric:hash123"]
    mock_redis.hgetall.return_value = {
        b"value": b"42.0",
        b"unit": b"20",  # Unit.COUNT_PER_SECOND value
        b"dimensions": b'[{"name": "service", "value": "test"}]',
    }

    class MockRedisCollector(RedisCollector):
        def __init__(self):
            self.client = mock_redis

        def get_setting(self, name):
            return "redis://localhost:6379/0"

    with patch("statismo.metrics.collector", return_value=MockRedisCollector()):
        push_metric(
            key="test_metric",
            value=42.0,
            unit=Unit.COUNT_PER_SECOND,
            dimensions=[Dimension(name="service", value="test")],
        )

        # Verify metric was saved to Redis
        mock_redis.hincrbyfloat.assert_called_with(
            f"statismo:metrics:test_metric:"
            f"{mock_redis.hincrbyfloat.call_args[0][0].split(':')[-1]}",
            "value",
            42.0,
        )
        mock_redis.hset.assert_any_call(
            mock_redis.hincrbyfloat.call_args[0][0],
            "unit",
            Unit.COUNT_PER_SECOND.value,
        )

        metrics = list(MockRedisCollector().metrics())
        assert len(metrics) == 1
        assert metrics[0].key == "test_metric"
        assert metrics[0].value == 42.0
        assert metrics[0].unit == Unit.COUNT_PER_SECOND
        assert len(metrics[0].dimensions) == 1
        assert metrics[0].dimensions[0]["name"] == "service"
        assert metrics[0].dimensions[0]["value"] == "test"

        mock_redis.hset.assert_any_call(
            mock_redis.keys.return_value[0], "value", 0
        )
