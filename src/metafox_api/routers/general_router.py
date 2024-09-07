from fastapi import APIRouter, Response

from metafox_shared.dal.redis.redis_client import RedisClient
from metafox_api.controllers.general_controller import GeneralController

router = APIRouter()
data_store = RedisClient()
controller = GeneralController(data_store)

@router.get(
    path="/jobs",
    tags=["MetaFOX API"],
    summary="Get method for retrieving all AutoML jobs",
    description="Retrieve all AutoML jobs",
    deprecated=False,
    response_description="List of AutoML jobs"
)
async def retrieve_all_jobs() -> Response:
    return controller.retrieve_all_jobs()

@router.delete(
    path="/job/prune",
    tags=["MetaFOX API"],
    summary="Delete method for pruning completed AutoML jobs",
    description="Prune completed AutoML jobs",
    deprecated=False,
    response_description="Message"
)
async def prune_automl_jobs() -> Response:
    return controller.prune_automl_jobs()