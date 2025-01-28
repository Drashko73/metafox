from fastapi import APIRouter, Depends, Response, Path
from fastapi_pagination import Page

from metafox_api.controllers.general_controller import GeneralController
from metafox_api.dependencies import get_general_controller

router = APIRouter()

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
async def retrieve_all_jobs(controller: GeneralController = Depends(get_general_controller)) -> Page[dict]:
    return controller.retrieve_all_jobs()

@router.delete(
    path="/job/prune",
    tags=["general-operations"],
    summary="Delete method for pruning completed AutoML jobs",
    description="Prune completed AutoML jobs",
    deprecated=False,
    response_description="Message"
)
async def prune_automl_jobs(controller: GeneralController = Depends(get_general_controller)) -> Response:
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
    automl_job_id: str = Path(..., description='AutoML job ID'),
    controller: GeneralController = Depends(get_general_controller)
) -> Response:
    return controller.delete_automl_job(automl_job_id)