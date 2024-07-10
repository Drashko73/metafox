from metafox.schemas.automl_job import AutoMLJob
from metafox.schemas.requests.start_automl_job import StartAutoMLJob
from metafox.app.api.v1.controllers.base_controller import BaseController
from metafox.worker.tasks.start_training import start_automl_train

class AutoMLJobController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
    def create_automl_job(self, body: AutoMLJob) -> dict:
        job_details = body.__str__()
        
        id = self.redis_client.generate_unique_job_key("AUTOML_JOB")
        
        try:
            self.redis_client.set(id, job_details)
        except Exception as e:
            return {"message": "Error saving job details.", "job_id": None}
        
        return {"message": "Job details saved successfully.", "job_id": id}
    
    def start_automl_job(self, body: StartAutoMLJob) -> dict:
        try:
            job_details = self.redis_client.get(body.job_id)
        except Exception as e:
            return {"message": "Error retrieving job details.", "job_id": None}
        
        job_details = eval(job_details)
        
        result = start_automl_train.delay(job_details)
        return {"message": "AutoML task started.", "job_id": result.id}
    
    def retreive_job_status(self, body: str) -> dict:
        job = start_automl_train.AsyncResult(body)
        return {"job_id": job.id, "status": job.status}
    
    def retrieve_job_result(self, body: str) -> dict:
        res = start_automl_train.AsyncResult(body)
        if res.ready():
            return {"job_id": body, "result": res.get()}
        else:
            return {"job_id": body, "result": "Job not ready yet."}