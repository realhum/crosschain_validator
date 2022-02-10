# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 POETRY_VIRTUALENVS_CREATE=0 SOURCE_DIR=/crosschain_backend WORK_DIR=/code ENTRYPOINT_SH_NAME=entrypoint_celery_beat.sh

RUN apt-get update && apt-get upgrade -y && apt-get install -y vim nano

# Set work directory
WORKDIR $WORK_DIR

# Upgrade pip and install poetry
RUN python -m pip install --upgrade pip && pip install poetry

# Copy poetry files
# COPY $SOURCE_DIR/poetry.lock $SOURCE_DIR/pyproject.toml /docker/celery/$ENTRYPOINT_SH_NAME $WORK_DIR/
COPY $SOURCE_DIR/poetry.lock $SOURCE_DIR/pyproject.toml $WORK_DIR/

# Install dependencies
RUN poetry install

# Copy project
COPY $SOURCE_DIR/$SOURCE_DIR/ $WORK_DIR/

# Change enytrypoint.sh mod for executing
# RUN chmod +x $ENTRYPOINT_SH_NAME

# ENTRYPOINT [$WORK_DIR/$ENTRYPOINT_SH_NAME]
