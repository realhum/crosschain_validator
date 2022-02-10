import base58
from decimal import Decimal, ROUND_HALF_UP
from requests import get as request_get
from typing import Union

from django.conf import settings
from rest_framework.status import HTTP_200_OK
from web3 import Web3

from crosschain_backend.consts import (
    COINGECKO_API_URL,
    COINGECKO_NETWORKS_NAME,
    DEFAULT_FIAT_CURRENCY_DECIMALS,
    RUBIC_BACKEND_API_URL,
)


NUM_OF_REQUESTS = 10
TIMEOUT_REQUEST = 3


def round_fiat_decimals(value: Union[Decimal, float]) -> Decimal:
    """
    Rounds input value by rules for fiat currency.

    :param value: value to be rounded
    :type value: Union[Decimal, float]
    :return: rounded value
    :rtype: Decimal
    """
    return Decimal(value).quantize(
        Decimal('1.' + '0' * DEFAULT_FIAT_CURRENCY_DECIMALS),
        ROUND_HALF_UP
    )


def camel_case_split(string: str) -> str:
    """
    Converts camel case string to normal string
    """

    string_list = [string[0]]

    for ch in string[1:]:
        if ch.isupper():
            string_list.append(ch)
        else:
            string_list[-1] += ch

    return ' '.join(string_list)


def get_coingecko_token_data(token_address: str, network: str):
    """
    Makes request to Coingecko API for token data
    """

    response = request_get(COINGECKO_API_URL.format(
        network=COINGECKO_NETWORKS_NAME.get(network, ''),
        token_address=token_address.lower(),
    ))

    if response.status_code == HTTP_200_OK:
        return response.json()


def bytes_to_base58(string: str):
    """
    Converts hexstr to base58
    """

    if not string.startswith('0x'):
        return string

    return base58.b58encode(Web3.toBytes(hexstr=string)).decode('utf-8')


def get_token_data(token_address: str, network: str):
    """
    Makes request to remote server API for token data
    """

    token_data = request_get(RUBIC_BACKEND_API_URL.format(
        main_backend_url=settings.MAIN_BACKEND,
        network=network,
        token_address=token_address,
    )).json()

    return token_data[0]


def get_coingecko_token_usd_price(token_address: str, network: str):
    """
    Returns USD price of token from Coingecko
    """

    token_data = get_coingecko_token_data(token_address, network)

    if not token_data:
        token_data = get_token_data(
            token_address=token_address,
            network=network,
        )

        return token_data.get('usd_price', 0)

    return token_data.get('market_data', {}).get('current_price', {}).get('usd', 0)
