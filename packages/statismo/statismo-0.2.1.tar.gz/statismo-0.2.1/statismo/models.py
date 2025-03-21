from django.db import models


class Unit(models.IntegerChoices):
    SECONDS = (10, "Seconds")
    COUNT_PER_SECOND = (20, "Count/Second")
    NONE = (30, "None")


class Metric(models.Model):
    """
    Simple database-backed metric accumulator.

    .. note::

        Not at all suitable for high-volume metrics, but good enough for
        basic usage. Make sure to vacuum the table frequently.
    """

    key = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=4, max_digits=10)
    dimensions = models.JSONField(default=list)
    dimensions_hash = models.CharField(max_length=255, null=True)
    unit = models.CharField(choices=Unit.choices, max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["key"]),
        ]
        constraints = [
            models.UniqueConstraint(
                name="statismo_unique_metric",
                fields=["key", "dimensions_hash"],
            ),
        ]
