import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('finance_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly-analysis': {
        'task': 'apps.analysis.tasks.create_weekly_analysis',
        'schedule': crontab(day_of_week='monday', hour=0, minute=0),
    },
    'monthly-analysis': {
        'task': 'apps.analysis.tasks.create_monthly_analysis',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}