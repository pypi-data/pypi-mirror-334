import json
from typing import Iterator

import redis

from statismo.collectors.base import BaseCollector
from statismo.metrics import Dimension, Value
from statismo.models import Unit, Metric


class RedisCollector(BaseCollector):
    """
    Stores metrics in Redis.
    """

    def __init__(self):
        self.client = redis.from_url(self.get_setting("URL"))

    def metrics(self) -> Iterator[Metric]:
        """
        Returns an iterator over all available metrics.

        Each value is reset to 0 after being read.
        """
        metric_keys = self.client.keys("statismo:metrics:*")
        for key in metric_keys:
            result = self.client.hgetall(key)
            yield Metric(
                key=key.decode("utf-8").split(":")[2],
                value=float(result[b"value"]),
                unit=Unit(int(result[b"unit"])),
                dimensions=(
                    json.loads(result[b"dimensions"])
                    if result.get(b"dimensions")
                    else None
                ),
            )
            self.client.hset(key, "value", 0)

    def save(
        self,
        key: str,
        value: Value,
        unit: Unit,
        dimhash: str,
        *,
        dimensions: list[Dimension] = None,
    ):
        """
        Save a metric to the collector.

        Increments the existing value, if any.
        """
        key = f"statismo:metrics:{key}:{dimhash}"
        self.client.hincrbyfloat(key, "value", value)
        self.client.hset(key, "unit", unit.value)
        if dimensions:
            self.client.hset(key, "dimensions", json.dumps(dimensions))
