from functools import wraps
from logging import exception
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    ReadTimeout,
    SSLError,
)

from eth_typing import ChecksumAddress
from eth_utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from web3.types import HexStr

from crosschain_backend.consts import (
    ALTERNATIVE_DEFAULT_CRYPTO_ADDRESS,
    DEFAULT_CRYPTO_ADDRESS,
    ETH_LIKE_ADDRESS_LENGTH,
    ETH_LIKE_ADDRESS_LENGTH_WITHOUT_0x,
    NETWORK_ERROR,
    NETWORK_NAMES,
)
from networks.types import ADDRESS_LIKE
from ..exceptions import ProviderNotConnected


def check_address_is_checksum_format(address: str) -> bool:
    return Web3.isChecksumAddress(address)


def convert_to_checksum_address_format(
    address: ADDRESS_LIKE
) -> ChecksumAddress:
    if not check_address_is_checksum_format(address):
        return Web3.toChecksumAddress(address)

    return address


def from_hex(value) -> HexStr:
    return add_0x_prefix(value.hex())


def convert_to_ethereum_like_address(address: str) -> str:
    if len(address) != ETH_LIKE_ADDRESS_LENGTH:
        BYTES_TO_REMOVE = '00' * 12

        if BYTES_TO_REMOVE in address:
            address = add_0x_prefix(
                remove_0x_prefix(address).replace(BYTES_TO_REMOVE, '')
            )

    return address


def convert_to_ethereum_like_token_address(
    token_address: str,
    network_name: str
) -> HexStr:
    """
    Removes any additional data from the beginning of eth like token address
    """

    if network_name != NETWORK_NAMES.get('solana') and \
            len(token_address) != ETH_LIKE_ADDRESS_LENGTH:
        token_address = add_0x_prefix(token_address[-ETH_LIKE_ADDRESS_LENGTH_WITHOUT_0x:])

        return token_address
    else:
        if token_address.lower() == ALTERNATIVE_DEFAULT_CRYPTO_ADDRESS.lower():
            token_address = DEFAULT_CRYPTO_ADDRESS

        return HexStr(token_address)


def reset_connection(function):
    """
    Decorator for handling connection error to RPC provider and switching
    to the next url for success connection
    """

    @wraps(function)
    def wrapped(*args, **kwargs):
        try:
            result = function(*args, **kwargs)

            return result
        except (
                BadFunctionCallOutput,
                ProviderNotConnected,
                ReadTimeout,
                HTTPError,
                ConnectionError,
                SSLError,
                AssertionError,
                ValueError,
        ) as exception_error:
            exception(NETWORK_ERROR.format(exception_error))

            args = list(args)
            custom_rpc_provider = args[0]

            rpc_url_list = custom_rpc_provider.network.rpc_url_list

            if custom_rpc_provider.url_number + 1 >= len(rpc_url_list):
                custom_rpc_provider.url_number = 0

                raise Exception(f"All nodes are not working right now in "
                                f"{custom_rpc_provider.network.title} network")

            # Switch to the next rpc provider and try again
            custom_rpc_provider.url_number += 1

            args[0] = custom_rpc_provider

            return wrapped(*args, **kwargs)

    return wrapped
