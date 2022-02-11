from logging import exception

from django.db import transaction

from crosschain_backend.celery import app as celery_app
from .models import ValidatorSwap
from .services.functions import process_swap


@celery_app.task
@transaction.atomic
def process_swap_task(swap_id):
    try:
        process_swap(swap_id)
    except Exception as exception_error:
        exception(exception_error)


@celery_app.task
def update_swaps_task():
    """
    Process swaps which signatures wasn't send
    """

    try:
        for swap in ValidatorSwap.displayed_objects.exclude(
                status__in=(
                    ValidatorSwap.STATUS_SUCCESS,
                    ValidatorSwap.STATUS_SIGNATURE_SEND,
                ),
        ):
            process_swap_task.delay(swap.id)
    except Exception as exception_error:
        exception(exception_error)
