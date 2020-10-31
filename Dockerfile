FROM python:3.7-alpine

LABEL org.opencontainers.image.source https://github.com/adrianchifor/run-warmup

WORKDIR /app
COPY app.py /app

RUN pip install --no-cache-dir 'Flask' 'gunicorn' 'requests-gcp'

CMD gunicorn --log-level info app:app
