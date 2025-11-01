# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install "pip<24.1"
RUN pip install -r requirements.txt

EXPOSE 8000
