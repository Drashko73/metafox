from metafox_shared.models.automl_job import AutoMLJob
from metafox_shared.requests.start_automl_job import StartAutoMLJob
from metafox_api.v1.controllers.base_controller import BaseController
from metafox_shared.dal.idatastore import IDataStore

class AutoMLJobController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: AutoMLJob) -> dict:
        job_details = body.__str__()
        
        id = self.data_store.generate_unique_job_key("AUTOML_JOB")
        
        try:
            self.data_store.set(id, job_details)
        except Exception as e:
            return {"message": "Error saving job details.", "job_id": None}
        
        return {"message": "Job details saved successfully.", "job_id": id}
    
    def start_automl_job(self, body: StartAutoMLJob) -> dict:
        try:
            job_details = self.data_store.get(body.job_id)
        except Exception as e:
            return {"message": "Error retrieving job details.", "job_id": None}
        
        job_details = eval(job_details)
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [job_details])
        return {"message": "AutoML task started.", "job_id": result.id}
    
    def retreive_job_status(self, body: str) -> dict:
        job = self.celery.AsyncResult(body)
        return {"job_id": job.id, "status": job.status}
    
    def retrieve_job_result(self, body: str) -> dict:
        res = self.celery.AsyncResult(body)
        if res.ready():
            return {"job_id": body, "result": res.get()}
        else:
            return {"job_id": body, "result": "Job not ready yet."}