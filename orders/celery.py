import os
from celery import Celery
from orders.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')

app = Celery('orders')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

