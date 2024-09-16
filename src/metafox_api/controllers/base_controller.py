from metafox_shared.dal.idatastore import IDataStore
from celery import Celery
from metafox_shared.constants.api_constants import CELERY_KEY_PREFIX

class BaseController:
    
    def __init__(self, data_store: IDataStore) -> None:
        self.data_store = data_store
        self.celery = Celery()
        self.celery.config_from_object('metafox_api.celeryconfig')
        
    def _get_task_id(self, automl_job_id: str) -> str:
        try:
            return self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return None
        
    def _get_automl_job_details(self, automl_job_id: str) -> dict:
        try:
            job_details = self.data_store.get(automl_job_id)
        except Exception as e:
            return None
        
        return eval(job_details) if job_details else None