from metafox_shared.constants.api_constants import *
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.models.tpot_job import TPOTAutoMLJob
from metafox_api.tpot.controllers.base_controller import BaseController

class AutoMLJobController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: TPOTAutoMLJob) -> dict:
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
    
    def start_automl_job(self, automl_job_id: str) -> dict:
        try:
            job_details = self.data_store.get(automl_job_id)
        except Exception as e:
            return {"message": "Error retrieving job details."}
        
        job_details = eval(job_details) # Convert string to dictionary
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [{"details": job_details, "id": automl_job_id}])
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + automl_job_id, result.id)  # Update celery task id status to the task id
        except Exception as e:
            return {"message": "Error updating celery task status."}
        
        return {"message": "AutoML job started."}
    
    def stop_automl_job(self, automl_job_id: str) -> dict:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return {"message": "Error retrieving celery task id."}
        
        if status == NOT_STARTED:
            return {"message": "AutoML job not started. Celery task id not set."}
        
        self.celery.control.revoke(status, terminate=True)
        
        return {"message": "AutoML job stopped."}
    
    def retreive_job_status(self, automl_job_id: str) -> dict:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return {"message": "Error retrieving celery task id."}
        
        if status == NOT_STARTED:
            return {"message": "AutoML job not started. Celery task id not set.", "status": status}
        
        job = self.celery.AsyncResult(status)
        
        logs = self.celery.send_task('metafox_worker.tasks.retrieve_logs.retrieve_logs', [automl_job_id, LOG_LINES])
        logs.wait()
        
        return {
            "message": "AutoML job status obtained.", 
            "status": job.status, 
            "logs": logs.get()
        }
    
    def retrieve_job_result(self, automl_job_id: str) -> dict:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return {"message": "Error retrieving celery task id.", "result": None}
        
        if status == NOT_STARTED:
            return {"message": "AutoML job not started. Celery task id not set.", "result": None}
        
        res = self.celery.AsyncResult(status)
        if res.ready():
            return {"message": "AutoML job result obtained.", "result": res.get()}
        else:
            return {"message": "AutoML job result not ready yet", "result": None}