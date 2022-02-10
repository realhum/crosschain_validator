from decimal import Decimal
from logging import exception

from django.conf import settings

from crosschain_backend.consts import TOKEN_ERROR
from base.support_functions.requests import send_get_request
from ..exceptions import TokenNotFound


def _get_token_from_main_backend(
    address: str,
    network_title: str
) -> dict:
    response = send_get_request(
        settings.TOKEN_API.format(
            address=address,
            network_title=network_title
        )
    )

    if not response:
        raise TokenNotFound(
            f'Token with the \"{address}\" address '
            f'in \"{network_title}\" network not found.'
        )

    return response[0]


def _get_actual_token_usd_price(address: str, network_title: str) -> Decimal:
    try:
        return Decimal(
            _get_token_from_main_backend(address, network_title)
            .get('usd_price', '0')
        )
    except Exception as exception_error:
        exception(TOKEN_ERROR.format(exception_error))

    return
