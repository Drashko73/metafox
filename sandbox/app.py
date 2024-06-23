
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

@app.post("/automl/start")
async def start_automl_task(request_data : StartAutoMLRequest):
    task = start_automl.delay(request_data.link_to_data, request_data.target)
    return {"task_id": str(task.id), "message": "AutoML task started."}

@app.get("/automl/result/{task_id}")
async def get_automl_result(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        raise HTTPException(status_code=404, detail="Task not found")
    elif task_result.state != "SUCCESS":
        return {"task_id": task_id, "status": task_result.state}
    else:
        return {"task_id": task_id, "status": task_result.state, "result": task_result.get()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)