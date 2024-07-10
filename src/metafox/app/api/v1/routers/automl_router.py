from fastapi import APIRouter

from metafox.schemas.automl_job import AutoMLJob
from metafox.schemas.requests.start_automl_job import StartAutoMLJob
from metafox.app.api.v1.controllers.automl_job_controller import AutoMLJobController

router = APIRouter()
job_controller = AutoMLJobController()

@router.post(
    path="/automl/job/create", 
    tags=["MetaFOX API v1"],
    summary="Post method for creating an AutoML job",
    description="Create an AutoML job",
    deprecated=False,
    response_description="Id of the stored AutoML job and a message"
)
async def create_automl_job(body: AutoMLJob) -> dict:
    return job_controller.create_automl_job(body)

@router.post(
    path="/automl/job/start", 
    tags=["MetaFOX API v1"],
    summary="Post method for starting an AutoML job",
    description="Start an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and a message"
)
async def start_automl_job(body: StartAutoMLJob) -> dict:
    return job_controller.start_automl_job(body)

@router.get(
    path="/automl/job/{job_id}/status", 
    tags=["MetaFOX API v1"],
    summary="Get method for retrieving the status of an AutoML job",
    description="Retrieve the status of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its status"
)
async def retrieve_job_status(job_id: str) -> dict:
    return job_controller.retreive_job_status(job_id)

@router.get(
    path="/automl/job/{job_id}/result", 
    tags=["MetaFOX API v1"],
    summary="Get method for retrieving the result of an AutoML job",
    description="Retrieve the result of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its result"
)
async def retrieve_job_result(job_id: str) -> dict:
    return job_controller.retrieve_job_result(job_id)