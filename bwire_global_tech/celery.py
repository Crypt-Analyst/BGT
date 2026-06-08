from __future__ import annotations

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bwire_global_tech.settings")

try:
    from celery import Celery

    app = Celery("bwire_global_tech")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    app.autodiscover_tasks()

    @app.task(bind=True)
    def debug_task(self):
        print(f"Request: {self.request!r}")

except ModuleNotFoundError:
    # Celery not installed in this environment; define a no-op placeholder
    app = None
