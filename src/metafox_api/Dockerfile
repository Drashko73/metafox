FROM python:3.10.12

WORKDIR /usr/src/metafox_api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/src

CMD ["python", "-m", "metafox_api"]