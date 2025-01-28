from fastapi import APIRouter, Response, Query, Path
from fastapi_pagination import Page

from metafox_shared.dal.mongo.mongo_client import MongoClient
from metafox_api.controllers.general_controller import GeneralController

router = APIRouter()
data_store = MongoClient()
controller = GeneralController(data_store)

# ==============================
# MetaFOX API
# ==============================

@router.get(
    path="/jobs",
    tags=["general-operations"],
    summary="Get method for retrieving all AutoML jobs",
    description="Retrieve all AutoML jobs",
    deprecated=False,
    response_description="List of AutoML jobs"
)
async def retrieve_all_jobs() -> Page[dict]:
    return controller.retrieve_all_jobs()

@router.delete(
    path="/job/prune",
    tags=["general-operations"],
    summary="Delete method for pruning completed AutoML jobs",
    description="Prune completed AutoML jobs",
    deprecated=False,
    response_description="Message"
)
async def prune_automl_jobs() -> Response:
    return controller.prune_automl_jobs()

@router.delete(
    path="/job/{automl_job_id}",
    tags=["general-operations"],
    summary="Delete method for deleting a specific AutoML job",
    description="Delete a specific AutoML job",
    deprecated=False,
    response_description="Message"
)
async def delete_automl_job(
    automl_job_id: str = Path(..., description='AutoML job ID')
) -> Response:
    return controller.delete_automl_job(automl_job_id)