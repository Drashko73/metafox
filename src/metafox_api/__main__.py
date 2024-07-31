import os

from dotenv import load_dotenv
from fastapi import FastAPI
from metafox_api.constants import *
from metafox_api.tpot.routers import automl_router as tpot_router

load_dotenv()

app = FastAPI(
    title=os.getenv("API_NAME", API_NAME), 
    version=os.getenv("API_VERSION", "1.0.0"),
    description="API for MetaFOX Component",
    docs_url=os.getenv("API_DOCS_URL", API_DOCS_URL),
    redoc_url=os.getenv("API_REDOC_URL", API_REDOC_URL),
)

api_prefix = os.getenv("API_PREFIX", API_PREFIX)
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

app.include_router(tpot_router.router, prefix=f"{api_prefix}/tpot")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=host,
        port=int(port)
    )