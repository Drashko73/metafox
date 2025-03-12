import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_AUTH_ENABLED = os.getenv("API_AUTH_ENABLED", "False") == "True"
    API_ORIGINS = os.getenv("API_ORIGINS", "*").split(",")
    API_ALLOW_CREDENTIALS = os.getenv("API_ALLOW_CREDENTIALS", "True") == "True"
    API_ALLOW_METHODS = os.getenv("API_ALLOW_METHODS", "*").split(",")
    API_ALLOW_HEADERS = os.getenv("API_ALLOW_HEADERS", "*").split(",")
    
    # Keycloak Configuration
    KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME", "")
    KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
    KEYCLOAK_AUTHORIZATION_URL = os.getenv("KEYCLOAK_AUTHORIZATION_URL", "")
    KEYCLOAK_TOKEN_URL = os.getenv("KEYCLOAK_TOKEN_URL", "")
    KEYCLOAK_REFRESH_URL = os.getenv("KEYCLOAK_REFRESH_URL", "")
    
    # Celery Configuration
    CELERY_BROKER_URL = os.getenv("BROKER_URL", "pyamqp://guest@localhost:5672//")
    CELERY_RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_WORKER_CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", os.cpu_count()))
    
    # MongoDB Configuration
    MONGO_DATABASE = os.getenv("MONGO_DB", "metafox")
    MONGO_TASKMETA_COLLECTION = os.getenv("MONGO_COLLECTION_TASK_META", "taskmeta")
    MONGO_AUTOMLJOBDETAILS_COLLECTION = os.getenv("MONGO_COLLECTION_AUTOML_JOB_DETAILS", "automl_job_details")
    MONGO_TASKINFO_COLLECTION = os.getenv("MONGO_COLLECTION_TASK_INFO", "task_info")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    
    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    
    # Other Configuration
    DB_TYPE = os.getenv("DB_TYPE", "mongo")