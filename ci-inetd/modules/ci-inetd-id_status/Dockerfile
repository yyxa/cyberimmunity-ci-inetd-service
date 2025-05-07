FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y librdkafka-dev gcc
RUN addgroup --system service_user && adduser --system --group service_user

COPY config/requirements.txt config/requirements.txt
RUN python -m venv venv
RUN venv/bin/python -m pip install -U pip
RUN venv/bin/pip install -r config/requirements.txt

COPY . .

RUN chown -R service_user /src

USER service_user