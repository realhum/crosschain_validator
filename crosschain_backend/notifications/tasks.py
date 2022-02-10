import logging

from crosschain_backend.celery import app
from .models import ErrorNotifier


@app.task()
def send_error_notification_task(error_name, error_args, tx_hash):
    try:
        notifier = ErrorNotifier(
            error_name=error_name,
            error_args=error_args,
            tx_hash=tx_hash
        )
        notifier.send_telegram_message()
    except Exception as error:
        logging.error(str(error))
