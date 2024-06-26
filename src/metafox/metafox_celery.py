from celery import Celery

app = Celery(
    'metafox'
)

app.config_from_object('metafox.celeryconfig')

if __name__ == "__main__":
    app.start()