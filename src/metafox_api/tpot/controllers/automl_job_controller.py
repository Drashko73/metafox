from metafox_shared.models.automl_job import AutoMLJob
from metafox_shared.requests.start_automl_job import StartAutoMLJob
from metafox_api.tpot.controllers.base_controller import BaseController
from metafox_shared.dal.idatastore import IDataStore
from metafox_api.constants import *

class AutoMLJobController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: AutoMLJob) -> dict:
        """
        Creates an AutoML job with the given details.
        Args:
            body (AutoMLJob): The details of the AutoML job.
        Returns:
            dict: A dictionary containing the status of the job creation.
                - If the job details are saved successfully, the dictionary will have the following keys:
                    - "message": A success message.
                    - "automl_job_id": The ID of the created AutoML job.
                - If there is an error saving the job details or the celery task ID status, the dictionary will have the following keys:
                    - "message": An error message.
                    - "automl_job_id": None.
        """
        job_details = body.__str__()
        
        id = self.data_store.generate_unique_job_key()
        
        try:
            self.data_store.set(id, job_details)
        except Exception as e:
            return {"message": "Error saving AutoML job details.", "automl_job_id": None}
        
        try:
            self.data_store.set(CELERY_KEY_PREFIX + id, NOT_STARTED)    # Set celery task id to NOT_STARTED
        except Exception as e:
            return {"message": "Error saving celery task id status.", "automl_job_id": None}
        
        return {"message": "AutoML job details saved successfully.", "automl_job_id": id}
    
    def start_automl_job(self, body: StartAutoMLJob) -> dict:
        """
        Starts an AutoML job.
        Args:
            body (StartAutoMLJob): The body of the request containing the job ID.
        Returns:
            dict: A dictionary containing the message indicating the status of the job.
        """
        try:
            job_details = self.data_store.get(body.job_id)
        except Exception as e:
            return {"message": "Error retrieving job details."}
        
        job_details = eval(job_details) # Convert string to dictionary
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [job_details])
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + body.job_id, result.id)  # Update celery task id status to the task id
        except Exception as e:
            return {"message": "Error updating celery task status."}
        
        return {"message": "AutoML job started."}
    
    def retreive_job_status(self, body: str) -> dict:
        """
        Retrieves the status of an AutoML job.
        Args:
            body (str): The body of the request.
        Returns:
            dict: A dictionary containing the status of the AutoML job.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + body)
        except Exception as e:
            return {"message": "Error retrieving celery task id."}
        
        if status == NOT_STARTED:
            return {"message": "AutoML job not started. Celery task id not set.", "status": status}
        
        job = self.celery.AsyncResult(status)
        return {"message": "AutoML job status obtained.", "status": job.status}
    
    def retrieve_job_result(self, body: str) -> dict:
        """
        Retrieves the result of an AutoML job.
        Args:
            body (str): The body of the job.
        Returns:
            dict: A dictionary containing the message and the result of the job.
                - If an error occurs while retrieving the celery task id, the message will be "Error retrieving celery task id." and the result will be None.
                - If the AutoML job has not started, the message will be "AutoML job not started. Celery task id not set." and the result will be None.
                - If the AutoML job result is ready, the message will be "AutoML job result obtained." and the result will be the obtained result.
                - If the AutoML job result is not ready yet, the message will be "AutoML job result not ready yet" and the result will be None.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + body)
        except Exception as e:
            return {"message": "Error retrieving celery task id.", "result": None}
        
        if status == NOT_STARTED:
            return {"message": "AutoML job not started. Celery task id not set.", "result": None}
        
        res = self.celery.AsyncResult(status)
        if res.ready():
            return {"message": "AutoML job result obtained.", "result": res.get()}
        else:
            return {"message": "AutoML job result not ready yet", "result": None}