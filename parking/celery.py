from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# from parking import local_settings
from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking.local_settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking.settings')

app = Celery('parking')

app.conf.enable_utc = False

app.conf.update(BROKER_URL=os.environ['REDIS_URL'], timezone='US/Central')

# app.config_from_object(local_settings, namespace='CELERY')

app.config_from_object(settings, namespace='CELERY')

# Set schedule for celery to run
app.conf.beat_schedule = {
    'Send_due_payment_reminder_to_customers': {
        'task': 'users.tasks.send_due_payment_reminder',
        'schedule': 172800.0,
    },

    'Delete_already_sent_email': {
        'task': 'users.tasks.delete_already_sent_reminders',
        'schedule': 190800.0,
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
