FROM python:3.10-slim-buster

COPY ./ ./app

WORKDIR /app

RUN apt update && apt upgrade -y

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
