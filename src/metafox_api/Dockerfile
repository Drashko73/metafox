FROM python:3.10.12

WORKDIR /usr/src/metafox_api

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV API_NAME MetaFOX
ENV API_VERSION 1.0.0
ENV API_VERSIONING_PREFIX v1
ENV API_HOST localhost
ENV API_PORT 8001
ENV API_PREFIX /metafox/api
ENV API_DOCS_URL /metafox/docs
ENV API_REDOC_URL /metafox/redoc

ENV REDIS_HOST localhost
ENV REDIS_PORT 6379
ENV REDIS_DB 0

ENV PYTHONPATH=/usr/src

CMD ["python", "-m", "metafox_api"]