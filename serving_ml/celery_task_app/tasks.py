import importlib
import logging
from celery import Task

from .worker import app
from celery_task_app.ml.model import ChurnModel 
import pandas as pd

class TrainTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True
    model = None

    def __init__(self):
        super().__init__()
        self.model = ChurnModel()

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            self.model = ChurnModel()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)



@app.task(bind=True, base=TrainTask, name='{}.{}'.format(__name__, 'Train'))
def train_model(self, data, target_column):
    self.model.train(data, target_column)
    return 'Model trained successfully'