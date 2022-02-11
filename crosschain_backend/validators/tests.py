from django.test import TestCase

from add_contracts import FULL_ABI
from contracts.models import Contract
from networks.models import Network, CustomRpcProvider
from .models import ValidatorSwap


class ValidatorTestCase(TestCase):
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

    def setUp(self):
        bsc_network = Network.displayed_objects.create(
            title='binance-smart-chain',
            rpc_url_list=[
                "https://bsc-dataseed.binance.org/",
            ],
        )
        eth_network = Network.displayed_objects.create(
            title='ethereum',
            rpc_url_list=[
                "https://api.mycryptoapi.com/eth",
                "https://rpc.flashbots.net/",
                "https://eth-mainnet.gateway.pokt.network/v1/5f3453978e354ab992c4da79",
            ],
        )

        Contract.displayed_objects.create(
            title='RUBIC_SWAP_CONTRACT_IN_BSC_PROD_READY',
            type=Contract.TYPE_CROSSCHAIN_ROUTING,
            address='0x70e8C8139d1ceF162D5ba3B286380EB5913098c4',
            network=bsc_network,
            hash_of_creation='0x9902f3cf707ce064d17b4c2368c8f6b2551a70943f7c3429321842e9d2c55dcf',
            blockchain_number=1,
            abi=FULL_ABI,
        )
        Contract.displayed_objects.create(
            title='RUBIC_SWAP_CONTRACT_IN_ETH_PROD_READY',
            type=Contract.TYPE_CROSSCHAIN_ROUTING,
            address='0xD8b19613723215EF8CC80fC35A1428f8E8826940',
            network=eth_network,
            hash_of_creation='0xcb99d1cc4ee13668087c2f8fcbe3c1f0b6a1e9bc682026fd03ffad5bda882843',
            blockchain_number=2,
            abi=FULL_ABI,
        )

    def test_validator_swap_create(self):
        rpc_provider = CustomRpcProvider(
            Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )
        )
        contract = Contract.get_contract_by_blockchain_id(1)

        ValidatorSwap.create_swap(
            rpc_provider=rpc_provider,
            contract=contract,
            txn_hash=self.transaction_hash,
            event=self.event_data,
        )

        validator_swap = ValidatorSwap.displayed_objects.get(
            transaction__hash__iexact=self.transaction_hash,
        )

        self.assertEqual(
            validator_swap.transaction.event_data['transactionHash'],
            self.transaction_hash,
            "create_swap doesn't saved ValidatorSwap correctly",
        )

    def test_send_signature_to_relayer(self):
        rpc_provider = CustomRpcProvider(
            Network.displayed_objects.get(
                title__iexact='binance-smart-chain',
            )
        )
        contract = Contract.get_contract_by_blockchain_id(1)
        signature = "44e35055e9fc46d382f9cab03d418e88ab84fb86994ee0339390be5b2bc181237a22830e9eb1239be2693a918f9b7892aa6d787959389c2c7c255a2c5a3c15c01b"

        validator_swap =ValidatorSwap.create_swap(
            rpc_provider=rpc_provider,
            contract=contract,
            txn_hash=self.transaction_hash,
            event=self.event_data,
        )

        validator_swap.signature = signature

        validator_swap.send_signature_to_relayer()

        self.assertEqual(
            validator_swap.status,
            ValidatorSwap.STATUS_SIGNATURE_SEND,
            "signature wasn't send",
        )
