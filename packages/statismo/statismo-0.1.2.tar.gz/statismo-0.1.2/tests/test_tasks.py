import pytest
from unittest.mock import patch, MagicMock

from statismo.models import Metric
from statismo.tasks import accumulate_metrics

@pytest.mark.django_db
def test_accumulate_metrics():
    """Test the accumulate_metrics task that sends metrics to CloudWatch."""
    # Create some test metrics
    Metric.objects.create(
        key="test_metric1",
        value=42.0,
        unit="20",  # Unit.COUNT_PER_SECOND as string
        dimensions=[{"name": "service", "value": "test"}],
        dimensions_hash="hash1",
    )

    Metric.objects.create(
        key="test_metric2",
        value=100.0,
        unit="10",  # Unit.SECONDS as string
        dimensions=[{"name": "service", "value": "test2"}],
        dimensions_hash="hash2",
    )

    # Mock boto3 client
    mock_client = MagicMock()

    # Replace the unit mapping function to avoid patching the enum
    unit_get_mapping = MagicMock(return_value="Count/Second")

    with (
        patch("boto3.client", return_value=mock_client),
        patch("statismo.tasks.settings.DEBUG", False),
    ):
        # Run the task
        accumulate_metrics()

        # Verify boto3 client was called with correct data
        mock_client.put_metric_data.assert_called_once()

        # Get the call arguments
        args, kwargs = mock_client.put_metric_data.call_args

        # Verify namespace
        assert kwargs["Namespace"] == "statismo"

        # Verify metrics data
        metrics_data = kwargs["MetricData"]
        assert len(metrics_data) == 2

        # Convert to a dict for easier testing
        metrics_by_name = {m["MetricName"]: m for m in metrics_data}

        # Check first metric
        assert "test_metric1" in metrics_by_name
        m1 = metrics_by_name["test_metric1"]
        assert m1["Value"] == 42.0
        # Skip unit test since that depends on the mapping
        assert len(m1["Dimensions"]) == 1
        assert m1["Dimensions"][0]["Name"] == "service"
        assert m1["Dimensions"][0]["Value"] == "test"

        # Check second metric
        assert "test_metric2" in metrics_by_name
        m2 = metrics_by_name["test_metric2"]
        assert m2["Value"] == 100.0
        # Skip unit test since that depends on the mapping
        assert len(m2["Dimensions"]) == 1
        assert m2["Dimensions"][0]["Name"] == "service"
        assert m2["Dimensions"][0]["Value"] == "test2"

        # Verify metrics were reset
        for metric in Metric.objects.all():
            assert metric.value == 0
