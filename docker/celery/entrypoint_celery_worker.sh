#! /bin/bash

exec celery --app crosschain_backend worker --loglevel=DEBUG -E --logfile=celery.log
