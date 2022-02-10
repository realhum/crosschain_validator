# Pull base image
FROM redis:latest

# Set environment varibles
ENV WORK_DIR=/usr/local/etc/redis/

RUN apt-get update && apt-get upgrade -y && apt-get install -y vim nano

# Set work directory
WORKDIR $WORK_DIR

# Copy confing files
COPY docker/redis $WORK_DIR
