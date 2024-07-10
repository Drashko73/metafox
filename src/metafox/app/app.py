import os

from dotenv import load_dotenv
from fastapi import FastAPI
from metafox.app.api.v1.routers import automl_router

load_dotenv()

app = FastAPI(
    title=os.getenv("API_NAME", "MetaFOX API"), 
    version=os.getenv("API_VERSION", "1.0.0"),
    description="API for MetaFOX Component",
    docs_url=os.getenv("API_DOCS_URL", "/metafox/docs"),
    redoc_url=os.getenv("API_REDOC_URL", "/metafox/redoc"),
)

api_prefix = os.getenv("API_PREFIX", "/metafox/api")
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

app.include_router(automl_router.router, prefix=f"{api_prefix}/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=host,
        port=int(port)
    )