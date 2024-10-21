from settings import settings
from celery import Celery


broker = settings.CELERY_BROKER

celery = Celery("tasks", broker=broker)
celery.autodiscover_tasks(["tasks"])