from celery import Celery
from metafox_shared.constants.string_constants import *

app = Celery(
    METAFOX_STR
)

app.config_from_object('metafox_worker.celeryconfig')
app.conf.broker_connection_retry_on_startup = True  # Prevent warning message

if __name__ == "__main__":
    app.start()