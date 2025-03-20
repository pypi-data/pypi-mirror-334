from django.contrib import admin

from statismo.models import Metric


# Register your models here.
@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value",
        "unit",
    )
    list_filter = ("key",)
    search_fields = ("key",)
