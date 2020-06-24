FROM python:3.7-alpine

WORKDIR /app
COPY app.py /app

RUN pip install --no-cache-dir 'Flask' 'gunicorn' 'requests-gcp'

CMD gunicorn --log-level info app:app
