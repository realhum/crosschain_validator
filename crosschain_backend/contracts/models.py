from logging import exception
from typing import Union
from uuid import UUID

from django.conf import settings
from django.db.models import (
    CharField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
    PROTECT,
    JSONField,
)
from django.utils.functional import cached_property
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.types import HexBytes, Wei

from base.models import AbstractBaseModel
from crosschain_backend.consts import (
    DEFAULT_CRYPTO_ADDRESS,
    CONTRACT_ERROR,
    ETH_LIKE_HASH_LENGTH,
    MAX_WEI_DIGITS,
)
from networks.models import Network, Transaction, CustomRpcProvider
from networks.services.functions import (
    convert_to_checksum_address_format,
    from_hex,
    convert_to_ethereum_like_address,
)
from networks.types import HASH_LIKE
from .exceptions import (
    ContractMultipleObjectsReturned,
    ContractNotFound,
)


# Create your models here.
class Contract(AbstractBaseModel):
    TYPE_CROSSCHAIN_ROUTING = 'crosschain routing'
    TYPE_BRIDGE = 'bridge'
    TYPE_TOKEN = 'token'

    TYPES = (
        (TYPE_CROSSCHAIN_ROUTING, TYPE_CROSSCHAIN_ROUTING.upper()),
        (TYPE_BRIDGE, TYPE_BRIDGE.upper()),
        (TYPE_TOKEN, TYPE_TOKEN.upper()),
    )

    title = CharField(
        max_length=255,
        verbose_name='Title',
        blank=True,
    )
    type = CharField(
        max_length=255,
        verbose_name='Type',
        choices=TYPES,
        default=TYPE_CROSSCHAIN_ROUTING,
    )
    address = CharField(
        max_length=255,
        verbose_name='Address',
        default=DEFAULT_CRYPTO_ADDRESS,
    )
    network = ForeignKey(
        to=Network,
        on_delete=PROTECT,
        related_name='network_contracts',
        verbose_name='Network',
    )
    abi = JSONField(
        verbose_name='ABI',
    )
    hash_of_creation = CharField(
        max_length=ETH_LIKE_HASH_LENGTH,
        verbose_name='Hash of creation',
        blank=True,
    )
    current_gas_price = DecimalField(
        max_digits=MAX_WEI_DIGITS,
        decimal_places=0,
        verbose_name='Actual gas price',
        default=0,
    )
    blockchain_number = PositiveIntegerField(
        verbose_name='Blockchain_number',
        default=0,
    )
    router_contract = ForeignKey(
        "self",
        on_delete=PROTECT,
        related_name='router_contract_contracts',
        verbose_name='Router contract',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'contracts'
        ordering = '-_created_at',

    def __str__(self) -> str:
        if not self.title:
            return (
                f'Contract at {self.address} in {self.network.title}'
                f' (id: {self.id})'
            )
        return (
            f'{self.title} at {self.address} in {self.network.title}'
            f' (id: {self.id})'
        )

    def load_contract(
        self,
        provider: CustomRpcProvider = None,
        address: str = None,
    ):
        if not provider:
            provider = CustomRpcProvider(self.network)
        if not address:
            address = self.address

        # return provider.eth.contract(
        #     address=provider.toChecksumAddress(address),
        #     abi=self.abi,
        # )

        return provider.get_contract(
            address=address,
            abi=self.abi,
        )

    def contract_function_call(
        self,
        contract_function_name,
        params,
        contract_address='',
    ):
        custom_rpc_provider = CustomRpcProvider(self.network)

        return custom_rpc_provider.contract_function_call(
            contract=self,
            contract_function_name=contract_function_name,
            params=params,
            contract_address=contract_address,
        )

    def is_processed_transaction(
        self,
        hash: HASH_LIKE,
        contract: Web3 = None,
    ) -> bool:
        return self.contract_function_call(
            contract_function_name='processedTransactions',
            params=(
                hash,
            ),
        )

    def get_other_blockchain_available_by_num(
        self,
        blockchain_id: int,
        contract: Web3 = None,
    ) -> bool:
        return self.contract_function_call(
            contract_function_name='getOtherBlockchainAvailableByNum',
            params=(
                blockchain_id,
            ),
        )

    def get_hash_packed(
        self,
        address: str,
        token_amount_with_fee: int,
        original_txn_hash: HASH_LIKE,
        blockchain_id: int,
        contract: Web3 = None,
    ) -> HexBytes:
        return self.contract_function_call(
            contract_function_name='getHashPacked',
            params=(
                convert_to_checksum_address_format(address),
                token_amount_with_fee,
                original_txn_hash,
                blockchain_id,
            ),
        )

    def get_transit_token_address(
        self,
        blockchain_id: int,
        contract: Web3 = None,
    ) -> int:
        return self.contract_function_call(
            contract_function_name='RubicAddresses',
            params=(
                blockchain_id,
            ),
        )

    def change_transaction_status(
        self,
        original_txn_hash: HASH_LIKE,
        status_code: int,
        hashed_params: str,
        contract: Web3 = None,
    ):
        if not contract:
            contract = self.load_contract()

        return contract.functions.changeTxStatus(
            originalTxHash=original_txn_hash,
            statusCode=status_code,
            hashedParams=hashed_params
        )

    def decode_function_input(
        self,
        txn_data_input: dict,
        provider: CustomRpcProvider = None
    ):
        if not provider:
            provider = CustomRpcProvider(self.network)

        txn_data_decoded_input = self \
            .load_contract(provider) \
            .decode_function_input(txn_data_input)[-1]

        for txn_data_value in txn_data_decoded_input:
            value = txn_data_decoded_input.get(txn_data_value)

            if isinstance(value, tuple):
                result = list()

                for item in value:
                    if isinstance(item, (list, tuple,)):
                        result.append(
                            tuple(
                                convert_to_ethereum_like_address(from_hex(_))
                                if isinstance(_, (bytes, HexBytes,))
                                else _
                                for _ in item
                            )
                        )

                        continue

                    result.append(
                        convert_to_ethereum_like_address(from_hex(item))
                        if isinstance(item, (bytes, HexBytes,))
                        else item
                    )

                txn_data_decoded_input.update({txn_data_value: tuple(result)})
            ###

            if isinstance(value, (bytes, HexBytes)):
                value = from_hex(value)
                txn_data_decoded_input.update({txn_data_value: value})

        return txn_data_decoded_input

    @staticmethod
    def decode_contract_function():
        pass

    def exists_contract_in_other_blockchain(
        self,
        blockchain_id: int,
        contract: Web3 = None,
    ) -> bool:
        if not contract:
            contract = self.load_contract()

        return self.contract_function_call(
            contract_function_name='existingOtherBlockchain',
            params=(
                blockchain_id,
            ),
        )

    def set_crypto_fee_of_blockchain(
        self,
        blockchain_id: int,
        crypto_fee: Union[int, Wei]
    ):
        return self.load_contract().functions.setCryptoFeeOfBlockchain(
            blockchain_id,
            crypto_fee,
        )

    def get_blockchain_crypto_fee(
        self,
        blockchain_id: int
    ):
        return self.contract_function_call(
            contract_function_name='blockchainCryptoFee',
            params=(
                blockchain_id,
            ),
        )

    def get_blockchain_number(self) -> int:
        return self.contract_function_call(
            contract_function_name='numOfThisBlockchain',
            params=(),
        )

    def add_router_contract(self):
        router_address = self.router_address

        router_contract = Contract.displayed_objects.filter(
            address__iexact=router_address,
            network=self.network,
        ).first()

        if not router_contract:
            router_contract = Contract(
                title='',
                type=self.TYPE_BRIDGE,
                address=router_address,
                network=self.network,
                abi={},
                hash_of_creation='',
            )
            router_contract.save()

        self.router_contract = router_contract

        self.save()

        return router_contract

    @cached_property
    def is_paused(self) -> bool:
        return self.contract_function_call(
            contract_function_name='paused',
            params=(),
        )

    @cached_property
    def block_number_of_creation(self):
        if not self.hash_of_creation:
            return

        hash_of_creation = Transaction.get_transaction_by_hash(
            CustomRpcProvider(self.network),
            self.hash_of_creation
        )

        if hash_of_creation.to is None:
            return hash_of_creation.blockNumber
        else:
            raise Exception(
                f'This no transaction \'{self.hash_of_creation}\' hash of '
                'creation contract.'
            )

    @cached_property
    def last_proccessed_block(self):
        last_tx = self.network.network_transactions.filter(
            block_number__gte=0,
        ).latest('_created_at')

        if not last_tx:
            return

        return last_tx.block_number

    @cached_property
    def confirmation_block_count(self) -> int:
        return self.contract_function_call(
            contract_function_name='minConfirmationBlocks',
            params=(),
        )

    @cached_property
    def blockchain_id(self) -> int:
        if self.blockchain_number:
            return self.blockchain_number
        # return self.get_blockchain_number()

    @cached_property
    def max_gas_price(self) -> int:
        return self.contract_function_call(
            contract_function_name='maxGasPrice',
            params=(),
        )

    @cached_property
    def min_token_amount(self) -> int:
        return self.contract_function_call(
            contract_function_name='minTokenAmount',
            params=(),
        )

    @cached_property
    def confirmation_signatures_count(self) -> int:
        return self.contract_function_call(
            contract_function_name='minConfirmationSignatures',
            params=(),
        )

    @cached_property
    def router_address(self) -> str:
        return self.contract_function_call(
            contract_function_name='blockchainRouter',
            params=(),
        )

    @cached_property
    def fee_amount_of_blockchain(self) -> int:
        return self.contract_function_call(
            contract_function_name='feeAmountOfBlockchain',
            params=(
                self.blockchain_id,
            ),
        )

    @cached_property
    def actual_gas_price(self):
        if self.current_gas_price < self.min_gas_price:
            return self.min_gas_price

        return self.current_gas_price

    @classmethod
    def get_contract(cls, contract_id: UUID):
        try:
            contract = cls.objects.get(
                id=contract_id,
            )
        except cls.DoesNotExist:
            message = (
                f'Contract with the \"{contract_id}\" id '
                f'not found in database.'
            )

            exception(CONTRACT_ERROR.format(message))

            raise ContractNotFound(message)
        except cls.MultipleObjectsReturned:
            message = (
                f'Several objects of contracts have been received'
                f' with the \"{contract_id}\" id from database.'
            )

            exception(CONTRACT_ERROR.format(message))

            raise ContractMultipleObjectsReturned(message)

        return contract

    @classmethod
    def get_contract_by_address(cls, network_id: UUID, address: str):
        try:
            contract = Contract.objects.get(
                network_id=network_id,
                address__iexact=address,
            )
        except Contract.DoesNotExist:
            message = (
                f'Contract with the \"{address}\" address in'
                f' the \"{network_id}\" network not found in database.'
            )

            exception(CONTRACT_ERROR.format(message))

            raise ContractNotFound(message)
        except Contract.MultipleObjectsReturned:
            message = (
                f'Several objects of contracts have been received'
                f' with the \"{address}\" address in the \"{network_id}\"'
                ' network from database.'
            )

            exception(CONTRACT_ERROR.format(message))

            raise ContractMultipleObjectsReturned(message)

        return contract

    @classmethod
    def get_contract_by_blockchain_id(cls, blockchain_id: int):
        for contract in cls.objects.filter(type=cls.TYPE_CROSSCHAIN_ROUTING):
            if contract.blockchain_id == blockchain_id:
                return contract

    @classmethod
    def load_contract_by_blockchain_id(cls, blockchain_id: int):
        for contract in cls.objects.filter(type=cls.TYPE_CROSSCHAIN_ROUTING):
            if contract.blockchain_number == blockchain_id:
                return contract.load_contract()

    @classmethod
    def get_decode_function_txn_input(
        cls,
        contract_blockchain_id: int,
        txn_data_input: dict,
    ):
        contract = cls.get_contract_by_blockchain_id(
            blockchain_id=contract_blockchain_id,
        )

        return contract.decode_function_input(txn_data_input=txn_data_input)

    @staticmethod
    def get_event(event: dict):
        event = dict(event)

        for _, item, in enumerate(event):
            item_value = event.get(item)

            if isinstance(item_value, AttributeDict):
                item_value = dict(item_value)
                event.update({item: item_value})

                continue

            if isinstance(item_value, (bytes, HexBytes)):
                item_value = from_hex(item_value)
                event.update({item: item_value})

        return event
