FROM ubuntu:rolling

LABEL maintainer j.ignacio.gil@gmail.com

# Install python and virtual env
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

# Define working directory.
WORKDIR /app

# Copy requirements file
ADD src/requirements.txt /app

RUN pip install -r /app/requirements.txt

# Copy sources of the project
ADD src/python /app

# Start process
CMD [ "python", "/app/main.py" ]