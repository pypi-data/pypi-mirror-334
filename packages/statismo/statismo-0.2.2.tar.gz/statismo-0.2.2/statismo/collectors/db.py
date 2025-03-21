from typing import Iterator

from django.db import transaction
from django.db.models import F

from statismo.collectors.base import BaseCollector
from statismo.metrics import Value, Dimension
from statismo.models import Metric, Unit


class DatabaseCollector(BaseCollector):
    def metrics(self) -> Iterator[Metric]:
        """
        Returns an iterator over all available metrics.
        """
        with transaction.atomic():
            q = Metric.objects.select_for_update()

            for metric in q:
                yield metric

            q.update(value=0)

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
        """
        metric, created = Metric.objects.get_or_create(
            key=key,
            dimensions_hash=dimhash,
            defaults={"value": value, "unit": unit, "dimensions": dimensions},
        )
        if not created:
            metric.value = F("value") + value
            metric.save(update_fields=["value"])
