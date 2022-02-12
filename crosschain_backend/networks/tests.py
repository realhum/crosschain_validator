from web3 import Web3

from base.tests import BaseTestCase
from contracts.models import Contract
from .models import Network, Transaction, CustomRpcProvider


class BaseNetworkTestCase(BaseTestCase):
    transaction_hash = "0xb735a892bc6504976c8d1953d56fa5122546c9bbb3e8770d4083430363285999"


class CustomRpcProviderTestCase(BaseNetworkTestCase):
    def test_get_transaction(self):
        custom_rpc_provider = CustomRpcProvider(
            Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )
        )
        rpc_provider = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

        self.assertEqual(
            custom_rpc_provider.get_transaction(
                txn_hash=self.transaction_hash,
            ),
            rpc_provider.eth.get_transaction(self.transaction_hash),
            "get_transaction doesn't return correct web3 transaction data",
        )


class TransactionTestCase(BaseNetworkTestCase):
    def test_add_transaction(self):
        network = Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )

        Transaction.add_transaction(
            network_id=network.id,
            txn_hash=self.transaction_hash,
        )

        transaction = Transaction.displayed_objects.get(
            hash__iexact=self.transaction_hash,
        )

        self.assertEqual(
            transaction.hash,
            self.transaction_hash,
            "add_transaction method saves incorrect transaction"
        )
