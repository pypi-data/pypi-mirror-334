import itertools

import boto3
from celery import shared_task
from django.db import transaction
from django.conf import settings

from statismo.models import Unit
from statismo.metrics import collector


def chunker(it, size):
    """
    Chunk an iterator into chunks of size `size`.

    If the final chunk is smaller than `size`, it will be returned as-is
    without padding.

    :param it: The iterator to chunk.
    :param size: The size of each chunk.
    :return: An iterator of chunks.
    """
    iterator = iter(it)
    while chunk := list(itertools.islice(iterator, size)):
        yield chunk


@shared_task(ignore_result=True)
def accumulate_metrics():
    """
    Accumulate metrics from the database.

    This task runs periodically to accumulate metrics from the metric collector
    and send them to CloudWatch.
    """
    if settings.DEBUG:
        return

    with transaction.atomic():
        metrics = collector().metrics()

        # Maximum # of metrics is 150 per call. Maximum payload size 1MB.
        for chunk in chunker(metrics, 75):
            chunk = list(chunk)

            client = boto3.client("cloudwatch", region_name="us-west-2")
            client.put_metric_data(
                Namespace=getattr(
                    settings, "STATISMO_METRIC_NAMESPACE", "statismo"
                ),
                MetricData=[
                    {
                        "MetricName": m.key,
                        "Dimensions": [
                            {
                                "Name": d["name"],
                                "Value": d["value"],
                            }
                            for d in (m.dimensions or [])
                        ],
                        "Value": m.value,
                        "Unit": {
                            Unit.SECONDS: "Seconds",
                            Unit.COUNT_PER_SECOND: "Count/Second",
                            Unit.NONE: "None",
                        }.get(m.unit, "None"),
                    }
                    for m in chunk
                ],
            )
