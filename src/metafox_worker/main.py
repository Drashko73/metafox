from celery import Celery
from celery.signals import worker_init, worker_shutdown
from metafox_shared.constants.string_constants import *
from metafox_worker.dependencies import get_mongo_client

app = Celery(
    METAFOX_STR
)

app.config_from_object('metafox_worker.celeryconfig')
app.conf.broker_connection_retry_on_startup = True  # Prevent warning message

mongo_client_instance = None

@worker_init.connect
def init_worker(**kwargs):
    global mongo_client_instance
    mongo_client_instance = get_mongo_client()
    
@worker_shutdown.connect
def shutdown_worker(**kwargs):
    global mongo_client_instance
    if mongo_client_instance is not None:
        mongo_client_instance.close()

if __name__ == "__main__":
    app.start()