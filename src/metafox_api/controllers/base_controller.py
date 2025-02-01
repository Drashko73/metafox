import os
from dotenv import load_dotenv
from celery import Celery
from metafox_shared.constants.api_constants import CELERY_KEY_PREFIX
from metafox_shared.constants.string_constants import TASK_ID
from metafox_shared.dal.idatastore import IDataStore

class BaseController:
    """
    Base controller class for all controllers.
    """
    
    def __init__(self, data_store: IDataStore) -> None:
        """
        Constructor for the BaseController class.
        Args:
            data_store (IDataStore): Data store object.
        """
        load_dotenv()
        
        self.data_store = data_store
        self.celery = Celery()
        self.celery.config_from_object('metafox_api.celeryconfig')
        self.collection_task_meta = os.getenv('MONGO_COLLECTION_TASK_META', '*')
        self.collection_automl_job_details = os.getenv('MONGO_COLLECTION_AUTOML_JOB_DETAILS', '*')
        self.collection_task_info = os.getenv('MONGO_COLLECTION_TASK_INFO', '*')
        
    def _get_task_id(self, automl_job_id: str) -> str:
        """
        Method to get the task id for a given automl job id.
        Args:
            automl_job_id (str): The automl job id.

        Returns:
            str: The task id if found, else None.
        """
        try:
            return eval(self.data_store.get(CELERY_KEY_PREFIX + automl_job_id, self.collection_task_info))[TASK_ID]
        except Exception as e:
            return None
        
    def _get_automl_job_details(self, automl_job_id: str) -> dict:
        """
        Method to get the automl job details for a given automl job id.
        Args:
            automl_job_id (str): The automl job id.

        Returns:
            dict: The automl job details if found, else None.
        """
        try:
            job_details = self.data_store.get(automl_job_id, self.collection_automl_job_details)
        except Exception as e:
            return None
        
        return eval(job_details) if job_details else None