
from fastapi import FastAPI, HTTPException, BackgroundTasks
from celery import Celery
from pydantic import BaseModel

from celery import Celery
from celery.result import AsyncResult
from worker import  start_automl

app = FastAPI()

# Pydantic model for request data
class StartAutoMLRequest(BaseModel):
    link_to_data: str
    target: str

# Pydantic model for response data
class AutoMLResponse(BaseModel):
    task_id: str
    status: str
    result: dict = None

@app.post("/automl/start")
async def start_automl_task(request_data : StartAutoMLRequest):
    task = start_automl.delay(request_data.link_to_data, request_data.target)
    return {"task_id": str(task.id), "message": "AutoML task started."}

celery_app = Celery()
celery_app.config_from_object('celeryconfig')

@app.get("/automl/result/{task_id}", response_model=AutoMLResponse)
async def get_automl_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "PENDING":
        raise HTTPException(status_code=404, detail="Task not found")
    elif task_result.state != "SUCCESS":
        return {"task_id": task_id, "status": task_result.state}
    else:
        result = task_result.get()
        if isinstance(result, dict) and 'model' in result:
            return {"task_id": task_id, "status": task_result.state, "result": result['model']}
        else:
            raise HTTPException(status_code=404, detail="Model not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)