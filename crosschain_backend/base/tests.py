from django.test import TestCase, override_settings

from crosschain_backend.consts import FULL_ABI
from contracts.models import Contract
from networks.models import Network


@override_settings(VALIDATOR_PRIVATE_KEY="e7f76474dcedbd059dfa63c0bcf1ea2d93af0927d7363e6df8a726477d15fd06")
class BaseTestCase(TestCase):
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
