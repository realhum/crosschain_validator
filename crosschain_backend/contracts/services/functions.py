from logging import info
from typing import Union

from borsh_construct import U64
from django.conf import settings
from eth_account.messages import encode_defunct
from eth_utils import add_0x_prefix, remove_0x_prefix
from solana.publickey import PublicKey
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.types import (
    HexBytes,
    TxParams,
    Wei,
)

from crosschain_backend.consts import (
    CONTRACT_ERROR,
    NETWORK_NAMES,
    SIGNER_INFO,
)
from networks.models import Transaction, CustomRpcProvider
from networks.types import HASH_LIKE
from ..exceptions import (
    ContractDoesNotExistsInOtherBlockChain,
    ContractPaused,
    ContractTransactionAlreadyProcessed,
    ContractTransactionAlreadyReverted,
)
from ..models import Contract

CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS = settings.CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS


def _get_params_to_transfer_to_other_blockchain(
    rpc_provider: CustomRpcProvider,
    event: AttributeDict,
    tx_hash: str = '',
) -> AttributeDict:
    """
    Returns params which will be used for trade in target network

    :param
    """

    # AttributeDict(
    #     {
    #         'RBCAmountIn': <transit_token_amount_in:int>,
    #         'amountSpent': <amount_spent:int>,
    #     }
    # ),
    # 'event': <event_name:str>,
    # 'logIndex': <log_index:int>,
    # 'transactionIndex': <txn_index:int>,
    # 'transactionHash': HexBytes(
    #     <txn_hash:str>
    # ),
    # 'address': <user_address:str>,
    # 'blockHash': HexBytes(
    #     <block_hash:str>
    # ),
    # 'blockNumber': <block_number:int>

    if not isinstance(event, AttributeDict):
        event['args'] = AttributeDict(event['args'])
        event = AttributeDict(event)

    original_txn_hash = event.transactionHash

    if tx_hash:
        original_txn = Transaction.get_transaction(
            network_id=rpc_provider.network.id,
            txn_hash=tx_hash,
        )
    else:
        original_txn = Transaction.get_transaction(
            network_id=rpc_provider.network.id,
            txn_hash=original_txn_hash,
        )

    blockchain_id = original_txn.data.get('params')[0]
    amount_spent = original_txn.event_data \
        .get('args') \
        .get('amountSpent')
    # ex "rbc_amount_in"
    transit_token_amount_in = original_txn.event_data \
        .get('args') \
        .get('RBCAmountIn')
    token_out_min = original_txn.data.get('params')[5]

    # if blockchain_id == 8:
    #     new_address = original_txn.event_data.get('args').get('newAddress')
    #     second_path = original_txn.event_data.get('args').get('path')
    # else:
    new_address = original_txn.data.get('params')[6]
    second_path = original_txn.data.get('params')[3]

    swap_to_crypto = original_txn.data.get('params')[7]
    swap_exact_for = original_txn.data.get('params')[8]
    contract_function = original_txn.data.get('params')[-1]

    return AttributeDict(
        {
            'original_txn_hash': original_txn_hash,
            'blockchain_id': blockchain_id,
            'token_out_min': token_out_min,
            'second_path': second_path,
            'new_address': new_address,
            'transit_token_amount_in': transit_token_amount_in,
            'amount_spent': amount_spent,
            'swap_to_crypto': swap_to_crypto,
            'swap_exact_for': swap_exact_for,
            'contract_function': contract_function,
        }
    )


def _sign_hash(hash: HASH_LIKE):
    if not isinstance(hash, str):
        hash = hash.hex()

    signed_hash = Web3().eth.account.sign_message(
        encode_defunct(hexstr=hash),
        settings.VALIDATOR_PRIVATE_KEY,
    )

    info(
        SIGNER_INFO.format(
            f'Hash \"{hash}\" was signed.'
            f' Signature: \"{signed_hash.signature.hex()}\".'
        )
    )

    return signed_hash.signature.hex()


def _check_exists_contract_in_other_blockchain(
    contract: Contract,
    blockchain_id: int,
    original_txn_hash: HASH_LIKE,
    hashed_params: HexBytes,
):
    contract_status = contract.exists_contract_in_other_blockchain(
        blockchain_id
    )

    if not contract_status:
        raise ContractDoesNotExistsInOtherBlockChain(
            CONTRACT_ERROR.format(
                f'Contract with the \"{contract.address}\" does not exists.'
            ),
            {
                'contract': contract,
                'original_txn_hash': original_txn_hash,
                'hashed_params': hashed_params,
            }
        )

    return True


def _check_contract_is_paused(
    contract: Contract,
    original_txn_hash: HASH_LIKE,
    hashed_params: HexBytes,
):
    contract_status = contract.is_paused

    if not contract_status:
        return True

    raise ContractPaused(
        CONTRACT_ERROR.format(
            f'Contract with the \"{contract.address}\" address is paused.'
        ),
        {
            'contract': contract,
            'original_txn_hash': original_txn_hash,
            'hashed_params': hashed_params,
        }
    )


def _check_is_processed_transaction(
    contract: Contract,
    original_txn_hash: HASH_LIKE,
    hashed_params: HexBytes = '',
):
    contract_status = contract.is_processed_transaction(original_txn_hash)

    if isinstance(original_txn_hash, (bytes, HexBytes)):
        original_txn_hash = original_txn_hash.hex()

    exception_error_messsage = (
        f'Transaction with the \"{original_txn_hash}\" original'
        ' hash is already {action} '
        f'at the \"{contract.address}\" contract address.'
    )

    if not contract_status:
        return contract_status
    elif contract_status == 1:
        raise ContractTransactionAlreadyProcessed(
            exception_error_messsage.format(action='processed'),
            {
                'contract': contract,
                'original_txn_hash': original_txn_hash,
                'hashed_params': hashed_params,
            }
        )
    elif contract_status == 2:
        raise ContractTransactionAlreadyReverted(
            exception_error_messsage.format(action='reverted'),
            {
                'contract': contract,
                'original_txn_hash': original_txn_hash,
                'hashed_params': hashed_params,
            }
        )


def _transform_params(params: AttributeDict, from_contract: Contract):
    to_contract = Contract.get_contract_by_blockchain_id(
        blockchain_id=params.blockchain_id,
    )

    new_params = dict(params)

    # TODO: Костыль с пересчетом decimals транзитных токенов.
    if to_contract.blockchain_id in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS:
        new_params['transit_token_amount_in'] = int(
            new_params['transit_token_amount_in'] / 10 ** 12
        )
    elif from_contract.blockchain_id in CONTRACT_BLOCKCHAIN_IDS_TOKEN_WITH_SIX_DECIMALS:
        new_params['transit_token_amount_in'] = int(
            new_params['transit_token_amount_in'] * 10 ** 12
        )

    return AttributeDict(new_params)


def get_hash_packed_solana(
    new_address,
    rbc_amount_in,
    original_txn_hash,
    blockchain_id,
) -> str:
    if not isinstance(original_txn_hash, str):
        original_txn_hash = original_txn_hash.hex()

    keccak_hex = Web3.solidityKeccak(
        ['bytes32', 'bytes8', 'bytes32', 'bytes8'],
        [
            bytes(PublicKey(new_address)),
            U64.build(rbc_amount_in),
            Web3.toBytes(hexstr=original_txn_hash),
            U64.build(blockchain_id)
        ]
    ).hex()

    return keccak_hex


def _get_signature(
    original_txn_hash: HASH_LIKE,
    blockchain_id: int,
    new_address: str,
    transit_token_amount_in: Union[int, Wei],
):
    if not all((transit_token_amount_in,)):
        raise Exception(
            f'Field \"transit_token_amount_in\" ({transit_token_amount_in=}) '
            'not be equal by 0.'
        )

    contract = Contract.get_contract_by_blockchain_id(blockchain_id)

    if contract.network.title == NETWORK_NAMES.get('solana'):
        hashed_params = get_hash_packed_solana(
            new_address=new_address,
            rbc_amount_in=transit_token_amount_in,
            original_txn_hash=original_txn_hash,
            blockchain_id=blockchain_id,
        )
    else:
        hashed_params = contract.get_hash_packed(
            new_address,
            transit_token_amount_in,
            original_txn_hash,
            blockchain_id,
        )

        _check_is_processed_transaction(
            contract,
            original_txn_hash,
            hashed_params,
        )

    return remove_0x_prefix(
        _sign_hash(
            hash=hashed_params,
        )
    )
