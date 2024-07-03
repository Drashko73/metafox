
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from celery.result import AsyncResult

from metafox.metafox_celery import app as celery_app
from metafox.tasks.start_training import start_automl_train
from metafox.schemas.start_automl_request import StartAutoMLRequest
from metafox.schemas.configure_model import ConfigureModel

load_dotenv()

app = FastAPI(
    title=os.getenv("API_NAME", "MetaFOX API"), 
    version=os.getenv("API_VERSION", "1.0.0"),
    description="API for MetaFOX Component",
    docs_url=os.getenv("API_DOCS_URL", "/metafox/docs"),
    redoc_url=os.getenv("API_REDOC_URL", "/metafox/redoc"),
)

api_prefix = os.getenv("API_PREFIX", "/metafox")
versioning = os.getenv("API_VERSIONING_PREFIX", "/v1")
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

#
# FastAPI routes
# Endpoint: /api_prefix/versioning/automl/start
# Method: POST
# Description: Start the AutoML task
# Request Body: StartAutoMLRequest
# Response: JSON object with task_id and message
#
@app.post(f"{api_prefix}/{versioning}/automl/start", response_model=StartAutoMLRequest)
async def start_automl_task(body: ConfigureModel):
    result = start_automl_train.delay(body.model_dump())
    return {"task_id": result.id, "message": "AutoML task started."}

#
# FastAPI routes
# Endpoint: /api_prefix/versioning/automl/task/{task_id}/status
# Method: GET
# Description: Get the status of the AutoML task
# Request Parameter: task_id
# Response: JSON object with task_id and status
#
@app.get(f"{api_prefix}/{versioning}/automl/task/{{task_id}}/status")
async def get_task_status(task_id: str):
    task = start_automl_train.AsyncResult(task_id)
    return {"task_id": task.id, "status": task.status}

#
# FastAPI routes
# Endpoint: /api_prefix/versioning/automl/task/{task_id}/result
# Method: GET
# Description: Get the result of the AutoML task
# Request Parameter: task_id
# Response: JSON object with task_id and result
#
@app.get(f"{api_prefix}/{versioning}/automl/task/{{task_id}}/result")
async def get_task_result(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    if res.ready():
        return {"task_id": task_id, "result": res.get()}
    else:
        return {"task_id": task_id, "result": "Task not ready yet."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=host, 
        port=port
    )