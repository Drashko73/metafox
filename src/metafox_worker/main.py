from celery import Celery
from celery.signals import worker_init, worker_shutdown
from metafox_shared.constants.string_constants import *
from metafox_worker.dependencies import get_data_store

app = Celery(
    METAFOX_STR
)

app.config_from_object('metafox_worker.celeryconfig')
app.conf.broker_connection_retry_on_startup = True  # Prevent warning message

db_client_instance = None

@worker_init.connect
def init_worker(**kwargs):
    global db_client_instance
    db_client_instance = get_data_store()
    
@worker_shutdown.connect
def shutdown_worker(**kwargs):
    global db_client_instance
    if db_client_instance is not None:
        db_client_instance.close()
    else:
        print("Cannot close. Database connection not established.")

if __name__ == "__main__":
    app.start()