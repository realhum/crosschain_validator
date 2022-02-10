from logging import exception, info

from django.conf import settings
from web3.datastructures import AttributeDict

from crosschain_backend.consts import (
    SCANNER_INFO,
    TRADE_ERROR,
    UNEXPECTED_ERROR,
)
from networks.models import CustomRpcProvider
from notifications.services.functions import (
    send_error_notification,
)
from validators.models import ValidatorSwap
from ..functions import (
    _get_signature,
    _get_params_to_transfer_to_other_blockchain,
    _transform_params,
)
from ...exceptions import (
    ContractTransactionAlreadyProcessed,
    ContractTransactionAlreadyReverted,
)
from ...models import Contract

CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS = settings.CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS


def create_signature_transfer_tokens_handler(
    rpc_provider: CustomRpcProvider,
    contract: Contract,
    event: AttributeDict,
):
    validator_swap = ValidatorSwap.create_swap(
        rpc_provider,
        contract,
        event.transactionHash,
        event,
    )

    if validator_swap.signature:
        info(
            f"Signature for hash \"{event.transactionHash}\" already in DB. "
            f"Skiped..."
        )

        return

    params = _get_params_to_transfer_to_other_blockchain(
        rpc_provider=rpc_provider,
        event=event,
    )

    info(SCANNER_INFO.format(f'\nSOURCE PARAMS: \"{params}\".'))

    if (
        contract.blockchain_id in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS and
        params.blockchain_id not in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS
    ) or (
        contract.blockchain_id not in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS and
        params.blockchain_id in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS
    ):
        params = _transform_params(params=params, from_contract=contract)

    info(SCANNER_INFO.format(f'\nUPDATED PARAMS: \"{params}\".'))

    try:
        validator_swap.signature = _get_signature(
            params.original_txn_hash,
            params.blockchain_id,
            params.new_address,
            params.transit_token_amount_in,
        )
        validator_swap.status = ValidatorSwap.STATUS_SIGNATURE_CREATED
        validator_swap.save(update_fields=('signature', 'status',))
    except (
        ContractTransactionAlreadyProcessed,
        ContractTransactionAlreadyReverted,
    ) as exception_error:
        exception(TRADE_ERROR.format(exception_error))
    except Exception as exception_error:
        exception(UNEXPECTED_ERROR.format(exception_error))

        send_error_notification(
            exception_error=exception_error,
            tx_hash=params.original_txn_hash,
        )

        return


VALIDATOR_HANDLERS = {
    'TransferTokensToOtherBlockchainUser': create_signature_transfer_tokens_handler,
    'TransferCryptoToOtherBlockchainUser': create_signature_transfer_tokens_handler,
}
