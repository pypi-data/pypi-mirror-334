import decimal
import enum
import dataclasses
import hashlib
import json
from functools import cache

from django.conf import settings
from django.utils.module_loading import import_string

from statismo.models import Unit


class MetricDestination(enum.Enum):
    DEFAULT = "default"


Value = float | decimal.Decimal | int


@dataclasses.dataclass
class Dimension:
    name: str
    value: str | Value


@cache
def collector():
    return import_string(
        getattr(
            settings,
            "STATISMO_METRIC_COLLECTOR",
            "statismo.collectors.db.DatabaseCollector",
        )
    )()


def push_metric(
    key: str,
    value: Value,
    unit: Unit,
    *,
    dimensions: list[Dimension] = None,
):
    # We use ":" as a divider cache key names, and cloudwatch itself
    # forbids ":" in metric names.
    if ":" in key:
        raise ValueError("Metric key cannot contain ':'")

    dims = []
    for dimension in dimensions or []:
        if ":" in dimension.name:
            raise ValueError("Dimension name cannot contain ':'")

        dims.append({"name": dimension.name, "value": dimension.value})

    dims_hash = hashlib.md5()
    dims_hash.update(json.dumps(dims, sort_keys=True).encode("utf-8"))

    collector().save(
        key=key,
        value=value,
        unit=unit,
        dimhash=dims_hash.hexdigest(),
        dimensions=dims,
    )
