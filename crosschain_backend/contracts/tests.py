from django.test import TestCase

from add_contracts import FULL_ABI
from networks.models import Network
from .models import Contract


class ContractTestCase(TestCase):
    def setUp(self):
        bsc_network = Network.displayed_objects.create(
            title='binance-smart-chain',
            rpc_url_list=[
                "https://bsc-dataseed.binance.org/",
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

    def test_get_contract_by_blockchain_id(self):
        contract_address = '0x70e8C8139d1ceF162D5ba3B286380EB5913098c4'

        contract = Contract.get_contract_by_blockchain_id(1)

        self.assertEqual(
            contract.address,
            contract_address,
            "get_contract_by_blockchain_id return incorrect contract",
        )
