from django.test import TestCase

from contracts.models import Contract
from networks.models import Network, CustomRpcProvider
from .models import ValidatorSwap


class ValidatorTestCase(TestCase):
    def test_get_contract_by_blockchain_id(self):
        contract_address = '0x70e8C8139d1ceF162D5ba3B286380EB5913098c4'

        contract = Contract.get_contract_by_blockchain_id(1)

        self.assertEqual(
            contract.address,
            contract_address,
            "get_contract_by_blockchain_id return incorrect contract",
        )

    def test_validator_swap_create(self):
        rpc_provider = CustomRpcProvider(
            Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )
        )
        contract = Contract.get_contract_by_blockchain_id(1)
        transaction_hash = "0xb735a892bc6504976c8d1953d56fa5122546c9bbb3e8770d4083430363285999"
        event_data = {
            "args": {
                "RBCAmountIn": 31682537311623909227789,
                "amountSpent": 68400000000000000000
            },
            "event": "TransferCryptoToOtherBlockchainUser",
            "address": "0x70e8C8139d1ceF162D5ba3B286380EB5913098c4",
            "logIndex": 250,
            "blockHash": "0x8137cff1d513e3f65945222a0e95422e33b052d7e1028ae22906406f49825faa",
            "blockNumber": 14536882,
            "transactionHash": "0xb735a892bc6504976c8d1953d56fa5122546c9bbb3e8770d4083430363285999",
            "transactionIndex": 71,
        }

        ValidatorSwap.create_swap(
            rpc_provider=rpc_provider,
            contract=contract,
            txn_hash=transaction_hash,
            event=event_data,
        )

        validator_swap = ValidatorSwap.displayed_objects.get(
            transaction__hash__iexact=transaction_hash,
        )

        self.assertEqual(
            validator_swap.transaction.event_data['transactionHash'],
            transaction_hash,
            "create_swap doesn't saved ValidatorSwap correctly",
        )
