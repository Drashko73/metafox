

from fastapi import FastAPI
from celery.result import AsyncResult

from metafox.metafox_celery import app as celery_app
from metafox.tasks.start_training import start_automl_train
from metafox.schemas.start_automl_request import StartAutoMLRequest
from metafox.schemas.configure_model import ConfigureModel

app = FastAPI(
    title="MetaFOX API", 
    version="0.1", 
    description="API for MetaFOX Component",
    docs_url="/metafox/docs",
    redoc_url="/metafox/redoc"
)

#
# FastAPI routes
# Endpoint: /metafox/automl/start
# Method: POST
# Description: Start the AutoML task
# Request Body: StartAutoMLRequest
# Response: JSON object with task_id and message
#
@app.post("/metafox/automl/start")
async def start_automl_task(body: ConfigureModel):
    result = start_automl_train.delay(body.model_dump())
    return {"task_id": result.id, "message": "AutoML task started."}

#
# FastAPI routes
# Endpoint: /metafox/automl/task/{task_id}/status
# Method: GET
# Description: Get the status of the AutoML task
# Request Parameter: task_id
# Response: JSON object with task_id and status
#
@app.get("/metafox/automl/task/{task_id}/status")
async def get_task_status(task_id: str):
    task = start_automl_train.AsyncResult(task_id)
    return {"task_id": task.id, "status": task.status}

#
# FastAPI routes
# Endpoint: /metafox/automl/task/{task_id}/result
# Method: GET
# Description: Get the result of the AutoML task
# Request Parameter: task_id
# Response: JSON object with task_id and result
#
@app.get("/metafox/automl/task/{task_id}/result")
async def get_task_result(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    if res.ready():
        return {"task_id": task_id, "result": res.get()}
    else:
        return {"task_id": task_id, "result": "Task not ready yet."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)