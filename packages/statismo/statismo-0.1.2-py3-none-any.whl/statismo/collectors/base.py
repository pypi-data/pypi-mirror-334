import abc
from typing import Iterable

from django.conf import settings

from statismo.metrics import Value, Dimension
from statismo.models import Unit, Metric


class BaseCollector(abc.ABC):
    def metrics(self) -> Iterable[Metric]:
        """
        Returns an iterator over all available metrics.
        """

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

    @staticmethod
    def get_setting(name, default=None):
        """
        Get a setting from the Django settings.

        :param name: The name of the setting.
        :param default: The default value to return if the setting is not set.
        :return: The value of the setting.
        """
        return getattr(settings, f"STATISMO_METRIC_{name}", default)
