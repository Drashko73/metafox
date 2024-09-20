import json

from fastapi import Response
from metafox_shared.dal.idatastore import IDataStore
from metafox_api.controllers.base_controller import BaseController
from metafox_shared.constants.api_constants import CELERY_KEY_PREFIX, NOT_STARTED, CELERY_METAS_KEY_PREFIX


class GeneralController(BaseController):
    
    def __init__(self, data_store: IDataStore) -> None:
        super().__init__(data_store)
        
    def retrieve_all_jobs(self) -> Response:
        keys = self.data_store.get_all_keys()
        response = {}
        
        for key in keys:
            celery_task_id = self.data_store.get(CELERY_KEY_PREFIX + key)
            response[key] = "TODO: Implement timestamp retrieval."
        
        return Response(
            status_code=200,
            content=json.dumps(response),
            media_type="application/json"
        )
    
    def prune_automl_jobs(self) -> Response:

        job_ids, task_ids = self._get_started_jobs()
        
        deleted_jobs = 0
        for task_id in task_ids:
            
            # Check if the task is still running
            is_ready = self.celery.AsyncResult(task_id).ready()
            
            if is_ready:
                self.data_store.delete(CELERY_METAS_KEY_PREFIX + task_id)
                self.data_store.delete(CELERY_KEY_PREFIX + job_ids[task_ids.index(task_id)])
                self.data_store.delete(job_ids[task_ids.index(task_id)])
                
                deleted_jobs += 1

        return Response(
            status_code=200,
            content="Pruned total of " + str(deleted_jobs) + " AutoML jobs.",
            media_type="text/plain" ### TODO: Possibly change to JSON response with number of deleted jobs
        )
        
    def delete_automl_job(self, job_id: str) -> Response:
        task_id = self._get_task_id(job_id)
        
        if task_id is None:
            return Response(
                status_code=404,
                content="AutoML job not found.",
                media_type="text/plain"
            )
            
        if task_id == NOT_STARTED:
            return Response(
                status_code=400,
                content="Cannot delete AutoML job that has not started.",
                media_type="text/plain"
            )
        
        # Check if the task is still running
        is_ready = self.celery.AsyncResult(task_id).ready()
        
        if not is_ready:
            return Response(
                status_code=400,
                content="Cannot delete AutoML job that is still running.",
                media_type="text/plain"
            )
        
        self.data_store.delete(CELERY_METAS_KEY_PREFIX + task_id)
        self.data_store.delete(CELERY_KEY_PREFIX + job_id)
        self.data_store.delete(job_id)
        
        return Response(
            status_code=200,
            content="AutoML job deleted.",
            media_type="text/plain"
        )
        
    def _get_started_jobs(self) -> tuple:
        keys, task_ids = self.data_store.get_keys_by_pattern(CELERY_KEY_PREFIX + "*")
        started_job_ids = []
        started_task_ids = []
        
        for task_id in task_ids:
            if task_id != NOT_STARTED:
                started_task_ids.append(task_id)
                started_job_ids.append(keys[task_ids.index(task_id)].replace(CELERY_KEY_PREFIX, ""))
        
        return (started_job_ids, started_task_ids)