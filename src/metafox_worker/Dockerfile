FROM python:3.10.12

WORKDIR /usr/src/metafox_worker

COPY . .

RUN pip install -r requirements.txt

ENV BROKER_URL pyamqp://host.docker.internal:5672//
ENV RESULT_BACKEND redis://host.docker.internal:6379/0
ENV TASK_SERIALIZER json
ENV RESULT_SERIALIZER json
ENV WORKER_CONCURRENCY 12

ENV PYTHONPATH=/usr/src

CMD ["celery", "-A", "metafox_worker.main", "worker"]