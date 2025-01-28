import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from metafox_shared.constants.api_constants import API_DEFAULT_VERSION

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="MetaFOX API",
        version=os.getenv("API_VERSION", API_DEFAULT_VERSION),
        openapi_version="3.1.0",
        summary="MetaFOX - Advanced Automated Machine Learning Service",
        description="""MetaFOX is an advanced automated machine learning (AutoML) service that provides a comprehensive set of tools for feature selection, hyperparameter optimization, and model selection. It is designed to be user-friendly and easy to use, with a focus on providing a high level of automation and customization. MetaFOX uses popular open-source libraries and is designed to be extensible and flexible, allowing users to easily integrate it into their existing workflows.
        """,
        servers=[
            {
                "url": f"http://localhost:{os.getenv('API_PORT', 8000)}",
                "description": "Local Development Server"
            },
            {
                "url": f"http://147.91.204.120:{os.getenv('API_PORT', 8000)}",
                "description": "CERAMO Server"
            },
            {
                "url": f"http://147.91.204.112:{os.getenv('API_PORT', 8000)}",
                "description": "CERAMO Raspberry Pi Server"
            }
        ],
        routes=app.routes,
        contact={
            "name": "MetaFOX Repository",
            "url": "https://gitlab.pmf.kg.ac.rs/ceramo/metafox/-/tree/develop"
        }
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema