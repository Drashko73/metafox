from pydantic import BaseModel
from metafox_shared.constants.string_constants import *

class CeleryTaskInfo(BaseModel):
    task_id: str
    timestamp_created: str
    timestamp_received: str
    timestamp_started: str
    timestamp_completed: str
    hostname: str
    finished_status: str
    
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.task_id = kw.get('task_id', '')
        self.timestamp_created = kw.get('timestamp_created', '')
        self.timestamp_received = kw.get('timestamp_received', '')
        self.timestamp_started = kw.get('timestamp_started', '')
        self.timestamp_completed = kw.get('timestamp_completed', '')
        self.hostname = kw.get('hostname', '')
        self.finished_status = kw.get('finished_status', '')
    
    def custom_model_dump(self) -> dict:
        return {
            TASK_ID: self.task_id,
            TIMESTAMP_CREATED: self.timestamp_created,
            TIMESTAMP_RECEIVED: self.timestamp_received,
            TIMESTAMP_STARTED: self.timestamp_started,
            TIMESTAMP_COMPLETED: self.timestamp_completed,
            HOSTNAME: self.hostname,
            FINISHED_STATUS: self.finished_status
        }
        
    def __str__(self) -> str:
        return str(self.custom_model_dump())