from logging import exception

from django.conf import settings
from web3.types import HexBytes

from ..tasks import (
    send_error_notification_task,
)


def send_error_notification(exception_error: Exception, tx_hash: HexBytes):
    """
    Sends error notification to telegram, etc.

    :param exception_error: Exception object
    :type exception_error: Exception
    :param tx_hash: transaction's hash
    :type tx_hash: str
    """
    try:
        error_args = exception_error.args[-1]

        if not isinstance(error_args, dict):
            error_args = {
                'message': error_args,
            }

        contract = error_args.get('contract')

        if contract:
            error_args.update({
                'contract': contract.title
            })

        if settings.BACKEND_SETTINGS_TYPE == 'validator':
            error_args.update({
                'backend type': settings.VALIDATOR_NAME
            })
        else:
            error_args.update({
                'backend type': 'RELAYER'
            })

        # Convert Exception args byte values to UTF-8
        for key, value in error_args.items():
            if isinstance(value, (bytes, HexBytes)):
                error_args.update({key: value.hex()})

        if isinstance(tx_hash, (bytes, HexBytes)):
            tx_hash = tx_hash.hex()

        send_error_notification_task.delay(
            error_name=exception_error.__class__.__name__,
            error_args=error_args,
            tx_hash=tx_hash,
        )
    except Exception as exc_error:
        exception(exc_error.__str__())
