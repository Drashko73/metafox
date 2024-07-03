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

# List of modules every worker should import
imports = [
    'metafox.tasks.start_training'
]

# Task settings
task_serializer = os.getenv(
    key='TASK_SERIALIZER',
    default='json'
)

# Task result settings
result_serializer = os.getenv(
    key='RESULT_SERIALIZER',
    default='json'
)


# Set the number of concurrent tasks a worker can execute
worker_concurrency = int(os.getenv(
    key='WORKER_CONCURRENCY',
    default=os.cpu_count() # Default to the number of CPUs
))