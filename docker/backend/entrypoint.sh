#! /bin/bash

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --force

# RUN WSGI
exec gunicorn -c gunicorn.py crosschain_backend.asgi:application -k uvicorn.workers.UvicornWorker --reload
