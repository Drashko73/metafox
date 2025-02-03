from metafox_shared.config import Config

broker_url = Config.CELERY_BROKER_URL

result_backend = Config.CELERY_RESULT_BACKEND

mongodb_backend_settings = {
    'database': Config.MONGO_DATABASE,
    'taskmeta_collection': Config.MONGO_TASKMETA_COLLECTION
}

imports = [
    'metafox_worker.tasks.start_training'
]

task_serializer = 'json'

result_serializer = 'json'

result_expires = None

worker_concurrency = Config.CELERY_WORKER_CONCURRENCY