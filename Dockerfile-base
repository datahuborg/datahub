FROM ubuntu:14.04
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
        thrift-compiler \
        python-pip \
        python-dev \
        libpq-dev \
        libpq5 \
        libffi-dev && \
        apt-get clean
ADD requirements.txt .
RUN pip install -r requirements.txt
