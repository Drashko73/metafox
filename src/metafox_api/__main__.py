from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from metafox_api.auth import get_user_info
from metafox_api.routers.general_router import router as general_router
from metafox_api.routers.tpot_router import router as tpot_router
from metafox_api.dependencies import get_data_store
from metafox_shared.config import Config

db_client_instance = get_data_store()
from metafox_api.openapi import custom_openapi

app = FastAPI(
    docs_url="/swagger",
    redoc_url="/redoc",
    on_startup=[lambda: print("MetaFox API started.")],
    on_shutdown=[lambda: db_client_instance.close() if db_client_instance is not None 
                 else print("Cannot close. Database connection not established.")]
)

app.openapi = lambda: custom_openapi(app)

api_prefix = "/metafox"
host = "0.0.0.0"
port = 8000

app.include_router(
    router=general_router,
    prefix=f"{api_prefix}/general",
    dependencies=[Depends(get_user_info)] if Config.API_AUTH_ENABLED == True else []
)

app.include_router(
    router=tpot_router, 
    prefix=f"{api_prefix}/tpot",
    dependencies=[Depends(get_user_info)] if Config.API_AUTH_ENABLED == True else []
)

add_pagination(app)

origins = Config.API_ORIGINS
allow_credentials = Config.API_ALLOW_CREDENTIALS
allow_methods = Config.API_ALLOW_METHODS
allow_headers = Config.API_ALLOW_HEADERS

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
        port=port
    )