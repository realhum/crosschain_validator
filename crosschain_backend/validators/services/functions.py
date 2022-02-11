from logging import exception, info
from django.db import transaction

from django.db.utils import OperationalError

from ..models import ValidatorSwap


def process_swap(swap_id):
    """
    Process validator swap depends on it's status
    """

    info('check swap')
    try:
        with transaction.atomic():
            swap = ValidatorSwap.displayed_objects.select_for_update(
                nowait=True
            ) \
                .filter(id=swap_id) \
                .first()

    except OperationalError:
        exception('swap model locked')

        return

    if swap.status == ValidatorSwap.STATUS_SIGNATURE_CREATED:
        swap.send_signature_to_relayer()

    return
