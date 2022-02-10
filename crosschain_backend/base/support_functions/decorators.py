from logging import exception, info
from time import sleep

from crosschain_backend.consts import UNEXPECTED_ERROR
from notifications.models import Notifier
from notifications.services.functions import send_error_notification


def auto_restart(function, timeout=15):
    def wrapper(*args, **kwargs):
        while 1:
            try:
                function(*args)
            except Exception as exception_error:
                exception(UNEXPECTED_ERROR.format(exception_error))
                info_msg = f'Restart after {timeout} seconds...'
                info(info_msg)
                try:
                    message = exception_error.args[0]

                    # Extract message from nested Exception
                    while isinstance(message, Exception):
                        message = message.args[0]
                except Exception:
                    message = ''

                exc_args = {
                    'message': Notifier.reformat_message(message),
                    'restart time': info_msg,
                }

                exception_error.args = [exc_args]

                send_error_notification(
                    exception_error=exception_error,
                    tx_hash='',
                )

                sleep(timeout)

    return wrapper
