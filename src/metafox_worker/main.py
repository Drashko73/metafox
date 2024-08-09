from celery import Celery

app = Celery(
    'metafox'
)

app.config_from_object('metafox_worker.celeryconfig')
app.conf.broker_connection_retry_on_startup = True  # Prevent warning message

if __name__ == "__main__":
    app.start()