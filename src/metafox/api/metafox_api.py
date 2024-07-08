
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from celery.result import AsyncResult

from metafox.schemas.configure_model import ConfigureModel
from metafox.schemas.create_automl_job import CreateAutoMLJob

from metafox.worker.metafox_celery import app as celery_app
from metafox.worker.tasks.start_training import start_automl_train

from metafox.common.logger import Logger

from metafox.redis.redis_client import RedisClient

load_dotenv()

app = FastAPI(
    title=os.getenv("API_NAME", "MetaFOX API"), 
    version=os.getenv("API_VERSION", "1.0.0"),
    description="API for MetaFOX Component",
    docs_url=os.getenv("API_DOCS_URL", "/metafox/docs"),
    redoc_url=os.getenv("API_REDOC_URL", "/metafox/redoc"),
)

api_prefix = os.getenv("API_PREFIX", "/metafox")
versioning = os.getenv("API_VERSIONING_PREFIX", "v1")
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

logger = Logger("API")
redis_client = RedisClient()

@app.post(f"{api_prefix}/{versioning}/automl/job/create")
async def create_automl_job(body: CreateAutoMLJob) -> dict:
    job_details = body.model_dump().__str__()
    logger.info("Saving job details to Redis.")
    
    id = redis_client.generate_unique_job_key("AUTOML_JOB")
    logger.info(f"Generated unique job ID: {id}")
    
    try:
        redis_client.set(id, job_details)
        logger.info("Job details saved successfully.")
    except Exception as e:
        logger.error(f"Error saving job details: {str(e)}")
        return {"message": "Error saving job details.", "job_id": None}
    
    return {"message": "Job details saved successfully.", "job_id": id}


@app.post(f"{api_prefix}/{versioning}/automl/job/start")
async def start_automl_task(body: str) -> dict:
    try:
        job_details = redis_client.get(body)
        logger.info("Retrieved job details from Redis.")
    except Exception as e:
        logger.error(f"Error retrieving job details: {str(e)}")
        return {"message": "Error retrieving job details.", "task_id": None}
    
    # convert job_details to a dictionary
    job_details = eval(job_details)
    
    result = start_automl_train.delay(job_details)
    return {"message": "AutoML task started.", "task_id": result.id}


@app.get(f"{api_prefix}/{versioning}/automl/job/{{job_id}}/status")
async def get_task_status(task_id: str):
    task = start_automl_train.AsyncResult(task_id)
    return {"task_id": task.id, "status": task.status}


@app.get(f"{api_prefix}/{versioning}/automl/job/{{job_id}}/result")
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