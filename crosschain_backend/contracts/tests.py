from web3.datastructures import AttributeDict

from base.tests import BaseTestCase
from contracts.services.functions import _get_signature
from contracts.services.scanners.handlers import create_signature_transfer_tokens_handler
from networks.models import CustomRpcProvider, Network
from validators.models import ValidatorSwap
from .models import Contract


class ContractTestCase(BaseTestCase):
    hash_packed = '4c752a5fbbf4987b78226a0310db6a46d6643b500c90da34e59e61bbbcd4150e'
    signature = '11e90d07562b9ed33d422306fbf8817cb733adb29a34187c5d5dcca973e643ea6b5453003f8274a38d57df463b6dc872169e446de374e9a020add6e5e35dbcff1b'
    transaction_hash = "0xb735a892bc6504976c8d1953d56fa5122546c9bbb3e8770d4083430363285999"
    wallet_address = '0xb697fe3246eebac106015ed78cff7342ee823b6c'
    token_amount = 31682537311
    blockchain_id = 2
    event_data = AttributeDict({
        "args": AttributeDict({
            "RBCAmountIn": 31682537311623909227789,
            "amountSpent": 68400000000000000000
        }),
        "event": "TransferCryptoToOtherBlockchainUser",
        "address": "0x70e8C8139d1ceF162D5ba3B286380EB5913098c4",
        "logIndex": 250,
        "blockHash": "0x8137cff1d513e3f65945222a0e95422e33b052d7e1028ae22906406f49825faa",
        "blockNumber": 14536882,
        "transactionHash": "0xb735a892bc6504976c8d1953d56fa5122546c9bbb3e8770d4083430363285999",
        "transactionIndex": 71,
    })

    def test_get_contract_by_blockchain_id(self):
        contract_address = '0x70e8C8139d1ceF162D5ba3B286380EB5913098c4'

        contract = Contract.get_contract_by_blockchain_id(1)

        self.assertEqual(
            contract.address,
            contract_address,
            'get_contract_by_blockchain_id return incorrect contract',
        )

    def test_hash_packed(self):
        contract = Contract.get_contract_by_blockchain_id(1)

        self.assertEqual(
            contract.get_hash_packed(
                address=self.wallet_address,
                token_amount_with_fee=self.token_amount,
                original_txn_hash=self.transaction_hash,
                blockchain_id=self.blockchain_id,
            ).hex(),
            self.hash_packed,
            'get_hash_packed method returned incorrect hash',
        )

    def test_get_signature(self):
        self.assertEqual(
            _get_signature(
                original_txn_hash=self.transaction_hash,
                blockchain_id=self.blockchain_id,
                new_address=self.wallet_address,
                transit_token_amount_in=self.token_amount,
            ),
            self.signature,
            '_get_signature function returned incorrect signature',
        )

    def test_create_signature(self):
        rpc_provider = CustomRpcProvider(
            Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )
        )
        contract = Contract.get_contract_by_blockchain_id(1)

        create_signature_transfer_tokens_handler(
            rpc_provider=rpc_provider,
            contract=contract,
            event=self.event_data,
        )

        validator_swap = ValidatorSwap.displayed_objects.get(
            transaction__hash__iexact=self.transaction_hash,
        )

        self.assertEqual(
            validator_swap.signature,
            self.signature,
        )
