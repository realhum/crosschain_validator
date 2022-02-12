import os

import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'crosschain_backend.settings.base'
)
django.setup()

from crosschain_backend.consts import FULL_ABI


if __name__ == "__main__":
    from networks.models import Network, Transaction
    from contracts.models import Contract
    from validators.models import ValidatorSwap

    ValidatorSwap.objects.all().delete()
    Transaction.objects.all().delete()

    Contract.objects.filter(type=Contract.TYPE_CROSSCHAIN_ROUTING).delete()
    Contract.objects.all().delete()
    Network.objects.all().delete()

    networks = [
        {
            'name': 'ethereum',
            'rpc_url_list': [
                "https://api.mycryptoapi.com/eth",
                "https://rpc.flashbots.net/",
                "https://eth-mainnet.gateway.pokt.network/v1/5f3453978e354ab992c4da79",
            ],
        },
        {
            'name': 'binance-smart-chain',
            'rpc_url_list': [
                "https://bsc-dataseed.binance.org/",
            ],
        },
        {
            'name': 'polygon',
            'rpc_url_list': [
                "https://polygon-rpc.com",
            ],
        },
        {
            'name': 'avalanche',
            'rpc_url_list': [
                "https://api.avax.network/ext/bc/C/rpc",
            ],
        },
        {
            'name': 'moonriver',
            'rpc_url_list': [
                "https://rpc.moonriver.moonbeam.network",
                "https://pub.elara.patract.io/moonriver",
            ],
        },
        {
            'name': 'fantom',
            'rpc_url_list': ["https://rpc.ftm.tools"],
        },
        {
            'name': 'harmony',
            'rpc_url_list': ['https://api.harmony.one',
                             'https://s1.api.harmony.one',
                             'https://s2.api.harmony.one',
                             'https://s3.api.harmony.one',
                             'https://harmony-0-rpc.gateway.pokt.network',
                             ],
        },
        {
            'name': 'solana',
            'rpc_url_list': ["https://api.mainnet-beta.solana.com"],
        },
        {
            'name': 'arbitrum',
            'rpc_url_list': ["https://arb1.arbitrum.io/rpc",
                             "https://rpc.ankr.com/arbitrum"],
        },
        {
            'name': 'aurora',
            'rpc_url_list': ["https://mainnet.aurora.dev"],
        },
    ]

    for network in networks:
        Network.displayed_objects.get_or_create(
            rpc_url_list=network['rpc_url_list'], title=network['name'])

    contracts_list = [
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_BSC_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0x70e8C8139d1ceF162D5ba3B286380EB5913098c4',
            'network': 'binance-smart-chain',
            'hash_of_creation': '0x9902f3cf707ce064d17b4c2368c8f6b2551a70943f7c3429321842e9d2c55dcf',
            'blockchain_number': 1,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_ETH_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0xD8b19613723215EF8CC80fC35A1428f8E8826940',
            'network': 'ethereum',
            'hash_of_creation': '0xcb99d1cc4ee13668087c2f8fcbe3c1f0b6a1e9bc682026fd03ffad5bda882843',
            'blockchain_number': 2,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_POL_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0xeC52A30E4bFe2D6B0ba1D0dbf78f265c0a119286',
            'network': 'polygon',
            'hash_of_creation': '0x3a072246384a9c47a123203503a255ee1f7ecbbaefc3edabaeb3979e9662df91',
            'blockchain_number': 3,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_AVAX_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0x541eC7c03F330605a2176fCD9c255596a30C00dB',
            'network': 'avalanche',
            'hash_of_creation': '0x6190e909513d5f40ac78eb4aafe2adeeb71042b24e6f55f55a84ba8e43ad8967',
            'blockchain_number': 4,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_FTM_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0xd23B4dA264A756F427e13C72AB6cA5A6C95E4608',
            'network': 'fantom',
            'hash_of_creation': '0x69f2f46f5a1474f0f95b786ce1f4d5db980a04098b4b58ceb146cf90adfb829a',
            'blockchain_number': 5,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_MOVR_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0xD8b19613723215EF8CC80fC35A1428f8E8826940',
            'network': 'moonriver',
            'hash_of_creation': '0xb6eaa6a4f0bc0b785ed4a75623bf1519957c0d9f96c699514e0086fdcac53869',
            'blockchain_number': 6,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_HARMONY_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0x5681012ccc3ec5bafefac21ce4280ad7fe22bbf2',
            'network': 'harmony',
            'hash_of_creation': '0x8e3a5957876ab4d35c9f1bc111c36307acb856d78314325fe9b2394c1733f85b',
            'blockchain_number': 7,
            'abi': FULL_ABI,
        },
        {
            'title': 'SOLANA_PROD',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': 'r2TGRLHRtQ2Uj1CR7TCBYKgRxJi5M8FRjcqZnyQzYDB',
            'network': 'solana',
            'hash_of_creation': '',
            'blockchain_number': 8,
            'abi': '',
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_ARBITRUM_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0x5f3c8d58a01aad4f875d55e2835d82e12f99723c',
            'network': 'arbitrum',
            'hash_of_creation': '0x2d4ffba38a162f9bc292543ca3c0612b7128526a4421a645e38b32c125fd01df',
            'blockchain_number': 10,
            'abi': FULL_ABI,
        },
        {
            'title': 'RUBIC_SWAP_CONTRACT_IN_AURORA_PROD_READY',
            'type': Contract.TYPE_CROSSCHAIN_ROUTING,
            'address': '0x55be05ecc1c417b16163b000cb71dce8526a5d06',
            'network': 'aurora',
            'hash_of_creation': '0x8a476dc394069afebce8503ca1e6cd84dca9ba5e26484b5121267b5557aa9f9c',
            'blockchain_number': 11,
            'abi': FULL_ABI,
        },
    ]

    for contract_data in contracts_list:
        contract = Contract.objects.update_or_create(
            type=contract_data['type'],
            title=contract_data['title'],
            address=contract_data['address'],
            abi=contract_data['abi'],
            network=Network.displayed_objects.get(
                title__iexact=contract_data['network'],
            ),
            hash_of_creation=contract_data['hash_of_creation'],
            blockchain_number=contract_data['blockchain_number'],
        )
