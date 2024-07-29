from metafox_shared.models.automl_job import AutoMLJob
from metafox_shared.requests.start_automl_job import StartAutoMLJob
from metafox_api.v1.controllers.base_controller import BaseController
from metafox_shared.dal.idatastore import IDataStore
from metafox_api.constants import *

class AutoMLJobController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: AutoMLJob) -> dict:
        job_details = body.__str__()
        
        id = self.data_store.generate_unique_job_key()
        
        try:
            self.data_store.set(id, job_details)
        except Exception as e:
            return {"message": "Error saving job details.", "job_id": None}
        
        try:
            self.data_store.set(CELERY_KEY_PREFIX + id, NOT_STARTED)
        except Exception as e:
            return {"message": "Error saving job status.", "job_id": None}
        
        return {"message": "Job details saved successfully.", "job_id": id}
    
    def start_automl_job(self, body: StartAutoMLJob) -> dict:
        try:
            job_details = self.data_store.get(body.job_id)
        except Exception as e:
            return {"message": "Error retrieving job details.", "job_id": None}
        
        job_details = eval(job_details)
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [job_details])
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + body.job_id, result.id)
        except Exception as e:
            return {"message": "Error saving job status.", "job_id": None}
        
        return {"message": "AutoML task started.", "job_id": result.id}
    
    def retreive_job_status(self, body: str) -> dict:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + body)
        except Exception as e:
            return {"message": "Error retrieving job status.", "job_id": None}
        
        if status == NOT_STARTED:
            return {"message": "Job not started yet.", "job_id": body, "status": status}
        
        job = self.celery.AsyncResult(status)
        return {"job_id": job.id, "status": job.status}
    
    def retrieve_job_result(self, body: str) -> dict:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + body)
        except Exception as e:
            return {"message": "Error retrieving job status.", "job_id": None}
        
        if status == NOT_STARTED:
            return {"message": "Job not started yet.", "job_id": body, "status": status}
        
        res = self.celery.AsyncResult(status)
        if res.ready():
            return {"job_id": body, "result": res.get()}
        else:
            return {"job_id": body, "result": "Job not ready yet."}