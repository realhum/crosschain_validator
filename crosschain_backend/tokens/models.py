from logging import exception, warning
from uuid import UUID

from django.db.models import (
    PROTECT,
    CharField,
    ForeignKey,
    PositiveIntegerField,
)
from django.db.utils import IntegrityError
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from base.models import AbstractBaseModel
from base.support_functions.base import get_token_data, bytes_to_base58
from contracts.models import Contract
from crosschain_backend.consts import (
    DEFAULT_CRYPTO_ADDRESS,
    DEFAULT_TOKEN_DECIMALS,
    TOKEN_ERROR,
    ETH_LIKE_TYPE,
    SOLANA_LIKE_TYPE,
)
from networks.models import Network
from networks.services.functions import (
    convert_to_checksum_address_format,
    convert_to_ethereum_like_token_address,
)
from networks.types import ADDRESS_LIKE
from .exceptions import (
    TokenMultipleObjectsReturned,
    TokenNotCreated,
)


# Create your models here.
class Token(AbstractBaseModel):
    name = CharField(
        max_length=512,
        verbose_name='Name',
    )
    symbol = CharField(
        max_length=255,
        verbose_name='Symbol',
    )
    address = CharField(
        max_length=255,
        verbose_name='Address',
    )
    decimals = PositiveIntegerField(
        verbose_name='Decimals',
        default=DEFAULT_TOKEN_DECIMALS,
    )
    network = ForeignKey(
        to=Network,
        on_delete=PROTECT,
        related_name='network_tokens',
        verbose_name='Network',
    )

    class Meta:
        db_table = 'tokens'
        ordering = '-_created_at',

    def __str__(self) -> str:
        return f'{self.symbol} at {self.address} (id: {self.id})'

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        self.symbol = self.symbol.lower()
        # self.address = self.address.lower()

        return super().save(*args, **kwargs)

    @classmethod
    def add_token(cls, network_id: UUID, address: ADDRESS_LIKE):
        network = Network.get_network(network_id)
        # TODO: Загружать общий для токенов контракт.
        token_contract = Contract \
            .get_contract_by_address(network_id, DEFAULT_CRYPTO_ADDRESS) \
            .load_contract(address=convert_to_checksum_address_format(address))

        try:
            token_name = token_contract \
                .get_function_by_name('name')().call()
            token_symbol = token_contract \
                .get_function_by_name('symbol')().call()
            token_decimals = token_contract \
                .get_function_by_name('decimals')().call()

            token = cls(
                network=network,
                name=token_name,
                address=address.lower(),
                symbol=token_symbol,
                decimals=token_decimals,
            )

            token.save()
        except (
                BadFunctionCallOutput,
                ContractLogicError,
                ValueError,
                OverflowError,
        ) as exception_error:
            message = (
                f'Token with the \"{address}\" address in'
                f' the \"{network.title}\" network not found.'
                f' Error description: \"{exception_error.__str__()}.\"'
            )

            token_data = get_token_data(
                token_address=address,
                network=network.title,
            )

            token = cls.objects.create(
                name=token_data.get("name"),
                symbol=token_data.get("symbol"),
                address=address,
                decimals=token_data.get("decimals"),
                network=network,
            )
        except IntegrityError as exception_error:
            message = (
                f'Token with the \"{address}\" address in'
                f' the \"{network.title}\" network not created.'
                f' Error description: \"{exception_error}.\"'
            )

            exception(TOKEN_ERROR.format(message))

            raise TokenNotCreated(message)
        except Exception as exception_error:
            message = (
                f'Token with the \"{address}\" address in'
                f' the \"{network.title}\" network not created.'
                f' Error description: \"{exception_error.__str__()}.\"'
            )

            exception(message)

            raise TokenNotCreated(message)

        return token

    @classmethod
    def add_solana_token(
        cls,
        network_id: UUID,
        address: ADDRESS_LIKE,
    ):
        network = Network.get_network(network_id)

        try:
            token_data = get_token_data(
                token_address=address,
                network=network.title,
            )

            token = cls.objects.create(
                name=token_data.get("name"),
                symbol=token_data.get("symbol"),
                address=address,
                decimals=token_data.get("decimals"),
                network=network,
            )
        except Exception as exception_error:
            message = (
                f'Token with the \"{address}\" address in'
                f' the \"{network.title}\" network not created.'
                f' Error description: \"{exception_error.__str__()}.\"'
            )

            exception(message)

            raise TokenNotCreated(message)

        return token

    @classmethod
    def get_token(
        cls,
        network_id: UUID,
        address: str,
        token_type=ETH_LIKE_TYPE
    ):
        network = Network.get_network(network_id)

        if token_type == ETH_LIKE_TYPE:
            address = convert_to_ethereum_like_token_address(
                token_address=address,
                network_name=network.title,
            )
        elif token_type == SOLANA_LIKE_TYPE:
            address = bytes_to_base58(
                string=address,
            )

        token = cls.objects.filter(
            network__id=network_id,
            address__iexact=address,
        ) \
            .first()

        if not token:
            message = (
                f'Token with the \"{address}\" address in'
                f' the \"{network.title}\" network not found in database.'
            )

            warning(TOKEN_ERROR.format(message))

            if token_type == ETH_LIKE_TYPE:
                token = cls.add_token(network_id, address)
            elif token_type == SOLANA_LIKE_TYPE:
                token = cls.add_solana_token(network_id, address)

        return token
