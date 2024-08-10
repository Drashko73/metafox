from fastapi import APIRouter, Response

from metafox_shared.models.tpot_job import TPOTAutoMLJob
from metafox_shared.dal.redis.redis_client import RedisClient
from metafox_api.tpot.controllers.automl_job_controller import AutoMLJobController

router = APIRouter()
data_store = RedisClient()
job_controller = AutoMLJobController(data_store)

@router.post(
    path="/automl/job/create", 
    tags=["MetaFOX API tpot"],
    summary="Post method for creating an AutoML job",
    description="Create an AutoML job",
    deprecated=False,
    response_description="Id of the stored AutoML job and a message"
)
async def create_automl_job(body: TPOTAutoMLJob) -> Response:
    return job_controller.create_automl_job(body)

@router.post(
    path="/automl/job/{automl_job_id}/start", 
    tags=["MetaFOX API tpot"],
    summary="Post method for starting an AutoML job",
    description="Start an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and a message"
)
async def start_automl_job(automl_job_id: str) -> Response:
    return job_controller.start_automl_job(automl_job_id)

@router.post(
    path="/automl/job/{automl_job_id}/stop",
    tags=["MetaFOX API tpot"],
    summary="Post method for stopping an AutoML job",
    description="Stop an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and a message"
)
async def stop_automl_job(automl_job_id: str) -> Response:
    return job_controller.stop_automl_job(automl_job_id)

@router.get(
    path="/automl/job/{automl_job_id}/status", 
    tags=["MetaFOX API tpot"],
    summary="Get method for retrieving the status of an AutoML job",
    description="Retrieve the status of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its status"
)
async def retrieve_job_status(automl_job_id: str) -> Response:
    return job_controller.retreive_job_status(automl_job_id)


@router.get(
    path="/automl/job/{automl_job_id}/logs", 
    tags=["MetaFOX API tpot"],
    summary="Get method for retrieving the logs of an AutoML job",
    description="Retrieve the logs of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its logs"
)
async def retrieve_job_logs(automl_job_id: str, lines: int) -> Response:
    return job_controller.retrieve_job_logs(automl_job_id, lines)

@router.get(
    path="/automl/job/{automl_job_id}/result", 
    tags=["MetaFOX API tpot"],
    summary="Get method for retrieving the result of an AutoML job",
    description="Retrieve the result of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its result"
)
async def retrieve_job_result(automl_job_id: str) -> Response:
    return job_controller.retrieve_job_result(automl_job_id)