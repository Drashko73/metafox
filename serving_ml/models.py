from typing import Any, Dict, List
from pydantic import BaseModel

class ChurnModelResponse(BaseModel):
    task_id: str
    model_path: str  

class TrainingData(BaseModel):
    data: List[Dict[str, float]]
    Exited: List[float]
    
class Task(BaseModel):
    task_id: str
    status: str

