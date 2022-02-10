from os import environ

from django import setup as django_setup

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'crosschain_backend.settings.base',
)
django_setup()


if __name__ == '__main__':
    from contracts.services.scanners.functions import start_scanners

    start_scanners(
        scanners={
            'binance-smart-chain': {
                'network': 'binance-smart-chain',
                'contract_address': '0x70e8c8139d1cef162d5ba3b286380eb5913098c4',
                'start_block': 14_931_351,
            },
            'ethereum': {
                'network': 'ethereum',
                'contract_address': '0xd8b19613723215ef8cc80fc35a1428f8e8826940',
                'start_block': 14_132_862,
            },
            'polygon': {
                'network': 'polygon',
                'contract_address': '0xec52a30e4bfe2d6b0ba1d0dbf78f265c0a119286',
                'start_block': 24_497_508,
            },
            'avalanche': {
                'network': 'avalanche',
                'contract_address': '0x541ec7c03f330605a2176fcd9c255596a30c00db',
                'start_block': 10_427_945,
            },
            'fantom': {
                'network': 'fantom',
                'contract_address': '0xd23b4da264a756f427e13c72ab6ca5a6c95e4608',
                'start_block': 29_878_246,
            },
            'moonriver': {
                'network': 'moonriver',
                'contract_address': '0xd8b19613723215ef8cc80fc35a1428f8e8826940',
                'start_block': 1_428_381,
            },
            'harmony': {
                'network': 'harmony',
                'contract_address': '0x5681012ccc3ec5bafefac21ce4280ad7fe22bbf2',
                'start_block': 22_519_691,
            },
            'arbitrum': {
                'network': 'arbitrum',
                'contract_address': '0x5f3c8d58a01aad4f875d55e2835d82e12f99723c',
                'start_block': 5_381_092,
            },
            'aurora': {
                'network': 'aurora',
                'contract_address': '0x55be05ecc1c417b16163b000cb71dce8526a5d06',
                'start_block': 58_819_603,
            },
        }
    )
