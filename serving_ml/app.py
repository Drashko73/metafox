from fastapi import FastAPI
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from celery_task_app.tasks import  train_model
from models import Task, TrainingData, ChurnModelResponse

app = FastAPI()

def convert_to_json_serializable(data: TrainingData) -> dict:
    return {
        'data': data.data,
        'Exited': data.Exited
    }

@app.post('/churn/train', response_model=Task, status_code=202)
async def train(data: TrainingData):
    serialized_data = convert_to_json_serializable(data)
    task_id = train_model.delay(serialized_data['data'], serialized_data['Exited'])
    return {'task_id': str(task_id), 'status': 'Processing'}


@app.get('/churn/result/{task_id}', response_model=ChurnModelResponse, status_code=200, 
        responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def churn_result(task_id:str):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return ChurnModelResponse(task_id = result['task_id'], model_path=result['model_path'])