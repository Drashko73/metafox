import os
import json
import pickle
import bentoml
from fastapi import Response
from celery import states
from metafox_shared.constants.api_constants import *
from metafox_shared.constants.string_constants import *
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.models.tpot_job import TPOTAutoMLJob
from metafox_api.controllers.base_controller import BaseController
from metafox_shared.models.celery_task import CeleryTaskInfo
from metafox_shared.utilis import get_current_date
class TPOTController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def create_automl_job(self, body: TPOTAutoMLJob) -> Response:
        body.timestamp_created = get_current_date()
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
        
        celery_task = CeleryTaskInfo(
            task_id=NOT_STARTED,
            timestamp_received="",
            timestamp_started="",
            timestamp_completed="",
            hostname='',
            finished_status=''
        )
        
        try:
            self.data_store.set(CELERY_KEY_PREFIX + id, celery_task.__str__())    # Set celery task id to NOT_STARTED
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
                media_type="text/plain"
            )
            
        return Response(
            status_code=200, 
            content=json.dumps({"message": "AutoML job created.", "automl_job_id": id}), 
            media_type="application/json"
        )
    
    def start_automl_job(self, automl_job_id: str) -> Response:
        
        task_id = self._get_task_id(automl_job_id)
        
        if task_id is None:
            return Response(
                status_code=404, 
                content="Could not find required data for the AutoML job.", 
                media_type="text/plain"
            )
        
        if task_id != NOT_STARTED:
            return Response(
                status_code=400, 
                content="AutoML job already started.", 
                media_type="text/plain"
            )
        
        job_details = self._get_automl_job_details(automl_job_id)
        if job_details is None:
            return Response(
                status_code=404, 
                content="AutoML job not found.", 
                media_type="text/plain"
            )
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [{"details": job_details, "id": automl_job_id}])
        
        celery_task = CeleryTaskInfo(
            task_id=result.id,
            timestamp_received="",
            timestamp_started="",
            timestamp_completed="",
            hostname='',
            finished_status=''
        )
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + automl_job_id, celery_task.__str__())  # Update celery task id status to the task id
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
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
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        self.celery.control.terminate(task_id=status[TASK_ID], signal="SIGQUIT")
        
        return Response(
            status_code=200,
            content="AutoML job stopped.",
            media_type="text/plain"
        )
        
    def save_model_to_bentoml(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": res.traceback}),
                    media_type="application/json"
                )
            
            pipeline_bytes = res.get()["model"]
            response = self._save_pipeline_to_bentoml(pipeline_bytes, automl_job_id)
            
            if response != OK:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": response}),
                    media_type="application/json"
                )
            
            return Response(
                status_code=200,
                content="Model saved.",
                media_type="text/plain"
            )
        
        return Response(
            status_code=200,
            content="AutoML job not completed.",
            media_type="text/plain"
        )
    
    def retrieve_job_details(self, automl_job_id: str) -> Response:
        
        job_details = self._get_automl_job_details(automl_job_id)
        
        if job_details is None:    
            return Response(
                status_code=404,
                content="AutoML job not found.",
                media_type="text/plain"
            )
        
        return Response(
            status_code=200,
            content=json.dumps({"automl_job_id": automl_job_id, "details": job_details}),
            media_type="application/json"
        )
    
    def retreive_job_status(self, automl_job_id: str, lines: int) -> Response:
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
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        job = self.celery.AsyncResult(status[TASK_ID])
        
        if job.state == states.FAILURE:
            return Response(
                status_code=200,
                content=json.dumps({"status": job.state, "logs": "", "traceback": job.traceback}),
                media_type="application/json"
            )
        
        logs = "".join(job.info["logs"][-lines:]) if job.info and "logs" in job.info else ""
        
        return Response(
            status_code=200,
            content=json.dumps({"status": job.state, "logs": logs}),
            media_type="application/json"
        )
    
    def retrieve_job_result(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404, 
                content="Required AutoML job details not found.", 
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200, 
                content="AutoML job not started.", 
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
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
        
    def export_model_bentoml(self, automl_job_id: str) -> Response:
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": res.traceback}),
                    media_type="application/json"
                )
            
            pipeline_bytes = res.get()["model"]
            response = self._save_pipeline_to_bentoml(pipeline_bytes, automl_job_id)
            
            if response != OK:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": response}),
                    media_type="application/json"
                )
            
            # Return the saved model file saved in metafox_api/bento_models
            filepath = "metafox_api/bento_models/" + automl_job_id + ".bentomodel"
            
            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    return Response(
                        status_code=200,
                        content=file.read(),
                        media_type="application/octet-stream",
                        headers={"Content-Disposition": f"attachment; filename={automl_job_id}.bentomodel"}
                    )
            else:
                return Response(
                    status_code=404,
                    content="Model not found. Make sure to call the save_model_bentoml endpoint first.",
                    media_type="text/plain"
                )
        
        return Response(
            status_code=200,
            content="AutoML job not completed.",
            media_type="text/plain"
        ) 
        
    def _save_pipeline_to_bentoml(self, pipeline_bytes: bytes, job_id: int) -> str:
        
        # Check if sklearn module is not imported and import it
        if "sklearn" not in globals():
            import sklearn
        
        pipeline = pickle.loads(pipeline_bytes)
        
        # Check if the directory exists, if not create it
        if not os.path.exists("metafox_api/bento_models/"):
            os.makedirs("metafox_api/bento_models/")
            
        bento_path = "metafox_api/bento_models/" + str(job_id)
        bento_tag = bentoml.Tag(
            name=str(job_id),
            version="1.0.0"
        )
        
        try:
            bentoml.sklearn.save_model(
                name=bento_tag,
                model=pipeline
            )
        except Exception as e:
            return str(e)
        
        try:
            bentoml.models.export_model(
                tag=bento_tag,
                path=bento_path,
            )
        except Exception as e:
            return str(e)
        
        return OK