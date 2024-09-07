import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from metafox_api.auth import get_user_info
from metafox_api.routers import tpot_router
from metafox_api.routers import general_router
from metafox_shared.constants.api_constants import *

load_dotenv()

app = FastAPI(
    title=os.getenv("API_NAME", API_NAME), 
    version=os.getenv("API_VERSION", API_DEFAULT_VERSION),
    description="API for MetaFOX Component",
    docs_url=os.getenv("API_DOCS_URL", API_DOCS_URL),
    redoc_url=os.getenv("API_REDOC_URL", API_REDOC_URL),
)

api_prefix = os.getenv("API_PREFIX", API_PREFIX)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=host,
        port=int(port)
    )