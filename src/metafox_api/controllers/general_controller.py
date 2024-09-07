import json

from fastapi import Response
from metafox_shared.dal.idatastore import IDataStore
from metafox_api.controllers.base_controller import BaseController
from metafox_shared.constants.api_constants import CELERY_KEY_PREFIX


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
    
    def prune_automl_jobs(self) -> str:
        return Response(
            status_code=200,
            content="TODO: Implement pruning of completed AutoML jobs.",
            media_type="text/plain"
        )