from logging import exception, info
from django.db.models.deletion import CASCADE
from requests import post as request_post
from requests.exceptions import RequestException
from uuid import UUID

from django.conf import settings
from django.db.models import (
    CharField,
    ForeignKey,
    OneToOneField,
    PROTECT,
)
from web3.types import HexBytes

from base.models import AbstractBaseModel
from base.support_functions.base import bytes_to_base58
from contracts.models import Contract
from networks.models import Transaction, CustomRpcProvider
from networks.types import HASH_LIKE


class ValidatorSwap(AbstractBaseModel):
    """
    ValidatorSwap model which used for creating and
    sending signatures to relayer.

    - contract - Contract instance on which transaction was found
    - transaction - Transaction instance of found transaction while scanning
    - signature - hashed params signed by Validator private key
    - status - current status of swap
    """

    STATUS_CREATED = 'created'
    STATUS_WAITING_FOR_DATA = 'waiting for data'
    STATUS_SIGNATURE_CREATED = 'signature created'
    STATUS_SIGNATURE_SEND = 'signature send'
    STATUS_SUCCESS = 'success'

    _STATUSES = (
        (STATUS_CREATED, STATUS_CREATED.upper()),
        (STATUS_WAITING_FOR_DATA, STATUS_WAITING_FOR_DATA.upper()),
        (STATUS_SIGNATURE_CREATED, STATUS_SIGNATURE_CREATED.upper()),
        (STATUS_SIGNATURE_SEND, STATUS_SIGNATURE_SEND.upper()),
        (STATUS_SUCCESS, STATUS_SUCCESS.upper()),
    )

    contract = ForeignKey(
        to=Contract,
        on_delete=PROTECT,
        related_name='contract_validator_swaps',
        verbose_name='Contract',
    )
    transaction = OneToOneField(
        to=Transaction,
        on_delete=CASCADE,
        related_name='validator_swap_transaction',
        verbose_name='Transaction',
    )
    signature = CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Signature',
    )
    status = CharField(
        max_length=255,
        choices=_STATUSES,
        default=STATUS_CREATED,
        verbose_name='Status',
    )

    class Meta:
        db_table = 'validator_swaps'
        ordering = '-_created_at',

    def __str__(self) -> str:
        return (
            f'Validator swap with transaction hash \"{self.transaction.hash}\"'
        )

    def send_signature_to_relayer(self):
        """
        Sends created by Validator signature.
        """

        params = {
            'password': settings.PRIVATE_PASSWORD_FOR_SIGNATURE_API,
        }
        payload = {
            'validatorName': settings.VALIDATOR_NAME,
            'signature': self.signature,
            'fromContractNum': self.contract.blockchain_id,
            'fromTxHash': self.transaction.hash,
            'eventName': self.transaction.event_data.get('event', ''),
        }

        try:
            response = request_post(
                url=f"{settings.RELAYER_URL}/api/trades/signatures/",
                params=params,
                json=payload,
            )

            if response.status_code != 200:
                exception("Could not send signature to relayer")

                return

            self.status = self.STATUS_SIGNATURE_SEND

            self.save()

            message = (
                f'Signature \"{self.signature}\" of validator '
                f'\"{settings.VALIDATOR_NAME}\" send to '
                f'{settings.RELAYER_URL}'
            )

            info(message)
        except RequestException as exception_error:
            exception(exception_error)

            pass

    @classmethod
    def get_swap_by_transaction_id(cls, transaction_id: UUID):
        return cls.objects.filter(transaction__id=transaction_id).first()

    @classmethod
    def create_swap(
        cls,
        rpc_provider: CustomRpcProvider,
        contract: Contract,
        txn_hash: HASH_LIKE,
        event: dict,
    ):
        """
        Save ValidatorSwap instance in DataBase

        :param rpc_provider: custom rpc provider of source network
        :param contract: Contract object of source network
        :param txn_hash: hash of the found transaction
        :param event: event data of transaction
        """

        if isinstance(txn_hash, HexBytes):
            txn_hash = txn_hash.hex()

        source_transaction = Transaction.get_transaction(
            network_id=rpc_provider.network.id,
            txn_hash=txn_hash,
        )

        info(source_transaction)

        event_data = contract.get_event(event)
        to_contract = Contract.get_contract_by_blockchain_id(
            blockchain_id=source_transaction.data.get('params')[0],
        )

        if to_contract.network.title == 'solana':
            transaction_params = list(source_transaction.data['params'])

            transaction_params[6] = bytes_to_base58(
                string=transaction_params[6]
            )

            second_path = list(transaction_params[3])

            for i in range(len(second_path)):
                second_path[i] = bytes_to_base58(
                    string=second_path[i],
                )

            transaction_params[3] = second_path

            source_transaction.data['params'] = transaction_params

        source_transaction.event_data = event_data
        source_transaction.save(update_fields=('event_data', 'data'))

        validator_swap = ValidatorSwap.get_swap_by_transaction_id(
            transaction_id=source_transaction.id
        )

        if not validator_swap:
            validator_swap = ValidatorSwap.objects.create(
                contract=contract,
                transaction=source_transaction,
            )

        return validator_swap
