import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Broker settings
broker_url = os.getenv(
    key='BROKER_URL',
    default='pyamqp://guest@localhost:5672//'
)

# Backend settings
result_backend = os.getenv(
    key='RESULT_BACKEND',
    default='redis://localhost:6379/0'
)

mongodb_backend_settings = {
    'database': os.getenv("MONGO_DB", "metafox"),
    'taskmeta_collection': os.getenv("MONGO_COLLECTION_TASK_META", "taskmeta")
}

# List of modules every worker should import
imports = [
    'metafox_worker.tasks.start_training'
]

# Task settings
task_serializer = 'json'

# Task result settings
result_serializer = 'json'

result_expires = None

# Set the number of concurrent tasks a worker can execute
worker_concurrency = int(os.getenv(
    key='WORKER_CONCURRENCY',
    default=os.cpu_count() # Default to the number of CPUs
))