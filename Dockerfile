FROM python:2

RUN apt-get update -y && \
    apt-get install -y python-tk

COPY app /app

RUN pip install -r /app/requirements.txt

RUN export DISPLAY=host.docker.internal:0

RUN mkdir /logs

WORKDIR /logs
