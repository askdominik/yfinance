from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_project.settings")

app = Celery("finance_project")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-every-hour": {
        "task": "finance_app.tasks.update_company_data",
        "schedule": crontab(minute=0, hour="*/1"),
    },
}
