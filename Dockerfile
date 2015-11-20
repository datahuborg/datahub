FROM ubuntu:14.04
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
        thrift-compiler \
        python-pip \
        python-dev \
        libpq-dev \
        libpq5 && \
        apt-get clean
RUN mkdir /datahub
WORKDIR /datahub
ADD requirements.txt /datahub/
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONPATH "/datahub/src:/datahub/src/gen-py:/datahub/src/apps"
ADD . /datahub/
RUN /bin/bash -c "source src/setup.sh"

# Should use an entrypoint script to run this command
RUN python src/manage.py collectstatic --noinput
# Volumes must be declared after changes to their contents or docker ignores
# those changes.
VOLUME /var/log/gunicorn
VOLUME /static