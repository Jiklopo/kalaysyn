FROM python:3.10-alpine

COPY ./ ./app

WORKDIR /app

RUN apk -U upgrade

RUN apk add build-base

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
