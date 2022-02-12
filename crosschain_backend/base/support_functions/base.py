import base58
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from web3 import Web3

from crosschain_backend.consts import (
    DEFAULT_FIAT_CURRENCY_DECIMALS,
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


def bytes_to_base58(string: str):
    """
    Converts hexstr to base58
    """

    if not string.startswith('0x'):
        return string

    return base58.b58encode(Web3.toBytes(hexstr=string)).decode('utf-8')
