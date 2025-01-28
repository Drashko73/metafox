import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from metafox_api.auth import get_user_info
from metafox_api.routers import tpot_router
from metafox_api.routers import general_router
from metafox_shared.constants.api_constants import *

load_dotenv()

def custom_openapi():
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

app = FastAPI(
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.openapi = custom_openapi

api_prefix = "/metafox"
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

app.include_router(
    router=general_router.router,
    prefix=f"{api_prefix}/general",
    dependencies=[Depends(get_user_info)] if os.getenv("API_AUTH_ENABLED", "False") == "True" else []
)

app.include_router(
    router=tpot_router.router, 
    prefix=f"{api_prefix}/tpot",
    dependencies=[Depends(get_user_info)] if os.getenv("API_AUTH_ENABLED", "False") == "True" else []
)

add_pagination(app)

origins = os.getenv("API_ORIGINS", "*").split(",")
allow_credentials = os.getenv("API_ALLOW_CREDENTIALS", "True") == "True"
allow_methods = os.getenv("API_ALLOW_METHODS", "*").split(",")
allow_headers = os.getenv("API_ALLOW_HEADERS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers
)

if __name__ == "__main__":
    import uvicorn
    from fastapi.openapi.utils import get_openapi
    
    uvicorn.run(
        app,
        host=host,
        port=int(port)
    )