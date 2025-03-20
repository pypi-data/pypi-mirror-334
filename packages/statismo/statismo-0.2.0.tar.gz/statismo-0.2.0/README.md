Statismo
========

Statismo is minimal collector of custom metrics for django applications. It
aggregates statistics into a configurable backend before periodically
pushing them to an external service such as Cloudwatch.

Currently, supports the following backends:

- Django's database
- Redis

And the following services:

- AWS Cloudwatch

Installation
------------

To install statismo, simply run:

```bash
pip install statismo
```

To use statismo with redis:

```bash
pip install statismo[redis]
```


Configuration
-------------

Add `statismo` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...,
    'statismo',
]
```

Add the following settings to your `settings.py` to use the django database
collector, which is suitable for small to medium-sized applications:

```python
STATISMO_METRIC_COLLECTOR = 'statismo.collectors.db.DatabaseCollector'
```

For larger applications, you may want to use the Redis collector:

```python
STATISMO_METRIC_COLLECTOR = 'statismo.collectors.redis.RedisCollector'
STATISMO_METRIC_URL = 'redis://localhost:6379/0'
```

Finally, to use a custom namespace for your metrics other than the default of
`statismo`, add the following setting:

```python
STATISMO_METRIC_NAMESPACE = 'myapp'
```

Finally, the periodic task that uploads metrics needs to be enabled. If you're
using Celery's django integration, this can be done by adding the following to
your `settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    "accumulate-metrics-every-5-minutes": {
        "task": "statismo.tasks.accumulate_metrics",
        "schedule": 60 * 5,
    }
}
```
