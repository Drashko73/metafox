import os
from celery import Celery

BROKER_URL = 'pyamqp://guest@localhost:5672//'
BACKEND_URL = 'rpc://'

app = Celery(
    'celery_app',
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=['celery_task_app.tasks']
)