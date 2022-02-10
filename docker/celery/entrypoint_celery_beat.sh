#! /bin/bash

exec celery --app crosschain_backend beat --loglevel=DEBUG -S django
