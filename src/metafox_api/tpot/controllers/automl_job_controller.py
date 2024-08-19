import json
from fastapi import Response
from celery import states
from metafox_shared.constants.api_constants import *
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.models.tpot_job import TPOTAutoMLJob
from metafox_api.tpot.controllers.base_controller import BaseController

class AutoMLJobController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: TPOTAutoMLJob) -> Response:
        job_details = body.__str__()
                
        id = self.data_store.generate_unique_job_key()
        
        try:
            self.data_store.set(id, job_details)
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
                media_type="text/plain"
            )
        
        try:
            self.data_store.set(CELERY_KEY_PREFIX + id, NOT_STARTED)    # Set celery task id to NOT_STARTED
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving celery task id.", 
                media_type="text/plain"
            )
            
        return Response(
            status_code=200, 
            content=json.dumps({"message": "AutoML job created.", "automl_job_id": id}), 
            media_type="application/json"
        )
    
    def start_automl_job(self, automl_job_id: str) -> Response:
        
        try:
            task_id = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
            
            if task_id != NOT_STARTED:
                return Response(
                    status_code=400, 
                    content="AutoML job already started.", 
                    media_type="text/plain"
                )
            
        except Exception as e:
            pass
        
        try:
            job_details = self.data_store.get(automl_job_id)
        except Exception as e:
            return Response(
                status_code=404, 
                content="AutoML job not found.", 
                media_type="text/plain"
            )
        
        job_details = eval(job_details) # Convert string to dictionary
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [{"details": job_details, "id": automl_job_id}])
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + automl_job_id, result.id)  # Update celery task id status to the task id
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving celery task id.", 
                media_type="text/plain"
            )
        
        return Response(
            status_code=200, 
            content="AutoML job started.", 
            media_type="text/plain"
        )
    
    def stop_automl_job(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Celery task id not found.",
                media_type="text/plain"
            )
        
        if status == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started. Celery task id not set.",
                media_type="text/plain"
            )
        
        self.celery.control.revoke(status, terminate=True)
        
        return Response(
            status_code=200,
            content="AutoML job stopped.",
            media_type="text/plain"
        )
    
    def retreive_job_status(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Celery task id not found.",
                media_type="text/plain"
            )
        
        if status == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started. Celery task id not set.",
                media_type="text/plain"
            )
        
        job = self.celery.AsyncResult(status)
        
        logs = "".join(job.info["logs"][-LOG_LINES:]) if job.info and "logs" in job.info else ""
        
        if job.state == states.FAILURE:
            return Response(
                status_code=200,
                content=json.dumps({"status": job.state, "logs": logs, "traceback": job.traceback}),
                media_type="application/json"
            )
        
        return Response(
            status_code=200,
            content=json.dumps({"status": job.state, "logs": logs}),
            media_type="application/json"
        )
        
    def retrieve_job_logs(self, automl_job_id: str, lines: int) -> Response:
        if lines < 0:
            return Response(
                status_code=400, 
                content="Number of lines must be greater than or equal to 0.", 
                media_type="text/plain"
            )
        
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404, 
                content="Celery task id not found.", 
                media_type="text/plain"
            )
        
        if status == NOT_STARTED:
            return Response(
                status_code=200, 
                content="AutoML job not started. Celery task id not set.", 
                media_type="text/plain"
            )
            
        job = self.celery.AsyncResult(status)
        
        logs = "".join(job.info["logs"][-lines:]) if job.info and "logs" in job.info else ""
        
        return Response(
            status_code=200, 
            content=logs,
            media_type="text/plain"
        )
    
    def retrieve_job_result(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404, 
                content="Celery task id not found.", 
                media_type="text/plain"
            )
        
        if status == NOT_STARTED:
            return Response(
                status_code=200, 
                content="AutoML job not started. Celery task id not set.", 
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status)
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": res.traceback}),
                    media_type="application/json"
                )
            
            return Response(
                status_code=200, 
                content=json.dumps({"result": res.get()}),
                media_type="application/json"
            )
        
        return Response(
            status_code=200, 
            content="AutoML job not completed.", 
            media_type="text/plain"
        )