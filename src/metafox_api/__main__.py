import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from metafox_api.auth import get_user_info
from metafox_api.routers.general_router import router as general_router
from metafox_api.routers.tpot_router import router as tpot_router
from metafox_api.dependencies import get_mongo_client

mongo_client_instance = get_mongo_client()
from metafox_api.openapi import custom_openapi

app = FastAPI(
    docs_url="/swagger",
    redoc_url="/redoc",
    on_startup=[lambda: print("MetaFox API started.")],
    on_shutdown=[lambda: mongo_client_instance.close() if mongo_client_instance is not None 
                 else print("MongoDB connection not established.")]
)

app.openapi = lambda: custom_openapi(app)

api_prefix = "/metafox"
host = os.getenv("API_HOST", "localhost")
port = os.getenv("API_PORT", 8000)

app.include_router(
    router=general_router,
    prefix=f"{api_prefix}/general",
    dependencies=[Depends(get_user_info)] if os.getenv("API_AUTH_ENABLED", "False") == "True" else []
)

app.include_router(
    router=tpot_router, 
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
    uvicorn.run(
        app,
        host=host,
        port=int(port)
    )