import os
from dotenv import load_dotenv

from metafox_shared.constants.string_constants import *

# Load environment variables
load_dotenv()

# Broker settings
broker_url = os.getenv(
    key=BROKER_URL_CAPITALIZED,
    default='pyamqp://guest@localhost:5672//'
)

# Backend settings
result_backend = os.getenv(
    key=RESULT_BACKEND_CAPITALIZED,
    default='redis://localhost:6379/0'
)

# List of modules every worker should import
imports = [
    'metafox_worker.tasks.start_training'
]

# Task settings
task_serializer = os.getenv(
    key=TASK_SERIALIZER_CAPITALIZED,
    default='json'
)

# Task result settings
result_serializer = os.getenv(
    key=RESULT_SERIALIZER_CAPITALIZED,
    default='json'
)

result_expires = os.getenv(
    key='RESULT_EXPIRES',
    default=0 # Never expire
)

# Set the number of concurrent tasks a worker can execute
worker_concurrency = int(os.getenv(
    key=WORKER_CONCURRENCY_CAPITALIZED,
    default=os.cpu_count() # Default to the number of CPUs
))