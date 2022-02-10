from typing import Union

from eth_typing import ChecksumAddress
from web3.types import HexBytes


ADDRESS_LIKE = Union[str, ChecksumAddress]
HASH_LIKE = Union[str, HexBytes]
