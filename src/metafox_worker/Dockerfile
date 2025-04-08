FROM python:3.10.12

WORKDIR /usr/src/metafox_worker

COPY src/metafox_worker/ .

COPY src/metafox_shared/ /usr/src/metafox_shared

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/src

CMD ["celery", "-A", "metafox_worker.main", "worker", "-n", "metafox-worker@%h"]