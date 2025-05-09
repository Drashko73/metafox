from fastapi import APIRouter, Response, Path, Query, Depends

from metafox_shared.constants.api_constants import LOG_LINES
from metafox_api.models.tpot_job import TPOTAutoMLJob
from metafox_api.controllers.tpot_controller import TPOTController
from metafox_api.dependencies import get_tpot_controller

router = APIRouter()

# ==============================
# TPOT AutoML Job Configuration
# ==============================

@router.post(
    path="/automl/job/create", 
    tags=["tpot-automl-job-configuration"],
    summary="Post method for creating an AutoML job",
    description="Create an AutoML job",
    deprecated=False,
    response_description="Id of the stored AutoML job and a message"
)
async def create_automl_job(
    body: TPOTAutoMLJob,
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.create_automl_job(body)

@router.put(
    path="/automl/job/{automl_job_id}/update",
    tags=["tpot-automl-job-configuration"],
    summary="Put method for updating an AutoML job",
    description="Update an AutoML job by providing a complete new configuration. This will completely overwrite the existing configuration.",
    deprecated=False,
    response_description="Id of the AutoML job with a message and job details"
)
async def update_automl_job(
    body: TPOTAutoMLJob,
    automl_job_id: str = Path(..., description="AutoML job Id"),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.update_automl_job(automl_job_id, body)

@router.get(
    path="/automl/job/{automl_job_id}/details",
    tags=["tpot-automl-job-configuration"],
    summary="Get method for retrieving the details of an AutoML job",
    description="Retrieve the details of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its details"
)
async def retrieve_job_details(
    automl_job_id: str = Path(..., description="AutoML job Id"),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.retrieve_job_details(automl_job_id)

# ==============================
# TPOT AutoML Job Operations
# ==============================

@router.post(
    path="/automl/job/{automl_job_id}/start", 
    tags=["tpot-automl-job-operations"],
    summary="Post method for starting an AutoML job",
    description="Start an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and a message"
)
async def start_automl_job(
    automl_job_id: str = Path(..., description="AutoML job Id"),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.start_automl_job(automl_job_id)

@router.post(
    path="/automl/job/{automl_job_id}/stop",
    tags=["tpot-automl-job-operations"],
    summary="Post method for stopping an AutoML job",
    description="Stop an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and a message"
)
async def stop_automl_job(
    automl_job_id: str = Path(..., description="AutoML job Id"),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.stop_automl_job(automl_job_id)

@router.get(
    path="/automl/job/{automl_job_id}/status", 
    tags=["tpot-automl-job-operations"],
    summary="Get method for retrieving the status of an AutoML job",
    description="Retrieve the status of an AutoML job",
    deprecated=False,
    response_description="Id of the AutoML job and its status"
)
async def retrieve_job_status(
    automl_job_id: str = Path(..., description="AutoML job Id"),
    lines: int = Query(LOG_LINES, description="Number of lines to retrieve", ge=0),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.retreive_job_status(automl_job_id, lines)

# @router.get(
#     path="/automl/job/{automl_job_id}/result", 
#     tags=["tpot-automl-job-operations"],
#     summary="Get method for retrieving the result of an AutoML job",
#     description="Retrieve the result of an AutoML job",
#     deprecated=True,
#     response_description="Id of the AutoML job and its result"
# )
# async def retrieve_job_result(
#     automl_job_id: str = Path(..., description="AutoML job Id")
# ) -> Response:
#     return tpot_controller.retrieve_job_result(automl_job_id)

# ==============================
# TPOT to BentoML
# ==============================

# @router.post(
#     path="/automl/job/{automl_job_id}/save_model_bentoml",
#     tags=["tpot-to-bentoml"],
#     summary="Post method for saving a model using BentoML",
#     description="Save a model using BentoML",
#     deprecated=True,
#     response_description="Id of the AutoML job and a message"
# )
# async def save_model_bentoml(
#     automl_job_id: str = Path(..., description="AutoML job Id")
# ) -> Response:
#     return tpot_controller.save_model_to_bentoml(automl_job_id)

@router.get(
    path="/automl/job/{automl_job_id}/export_model_bentoml",
    tags=["tpot-to-bentoml"],
    summary="Get method for exporting a model using BentoML",
    description="Export a model using BentoML",
    deprecated=False,
    response_description="File containing the exported model",
)
async def export_model_bentoml(
    automl_job_id: str = Path(..., description="AutoML job Id"),
    controller: TPOTController = Depends(get_tpot_controller)
) -> Response:
    return controller.export_model_bentoml(automl_job_id)