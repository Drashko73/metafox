FROM python:3.10.12

WORKDIR /usr/src/metafox_api

COPY . .
COPY metafox_shared /usr/src/metafox_shared

RUN pip install -r metafox_api/requirements.txt

EXPOSE 8001

ENV API_NAME MetaFOX
ENV API_VERSION 1.0.0
ENV API_VERSIONING_PREFIX v1
ENV API_HOST 0.0.0.0
ENV API_PORT 8001
ENV API_PREFIX /metafox/api
ENV API_DOCS_URL /metafox/docs
ENV API_REDOC_URL /metafox/redoc

ENV BROKER_URL pyamqp://host.docker.internal:5672//
ENV RESULT_BACKEND redis://host.docker.internal:6379/0
ENV TASK_SERIALIZER json
ENV RESULT_SERIALIZER json
ENV WORKER_CONCURRENCY 12

ENV REDIS_HOST host.docker.internal
ENV REDIS_PORT 6379
ENV REDIS_DB 0

ENV PYTHONPATH=/usr/src

CMD ["python", "-m", "metafox_api"]