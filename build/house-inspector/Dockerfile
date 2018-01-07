FROM ubuntu:rolling

LABEL maintainer j.ignacio.gil@gmail.com

# Install python and virtual env
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv curl libcurl4-gnutls-dev libgnutls28-dev && \
  rm -rf /var/lib/apt/lists/*

# Define working directory.
WORKDIR /app

# Copy requirements file
ADD src/crawler/requirements.txt /app

RUN pip install -r requirements.txt

# Copy sources of the project
ADD src/crawler/python .
ADD src/crawler/config config

ENV CONFIG_FILE_PATH config/config.yml
ENV CONFIG_LOGGING_PATH config/logging.conf

# Start process
CMD [ "python", "/app/main.py" ]