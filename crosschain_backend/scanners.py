from os import environ

from django import setup as django_setup

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'crosschain_backend.settings.{}'.format(
        environ.get('BACKEND_SETTINGS_MODE')
    )
)
django_setup()


if __name__ == '__main__':
    from contracts.services.scanners.functions import start_scanners

    start_scanners(
        scanners={
            'ethereum': {
                'network': 'ethereum',
                'contract_address': '',
                'start_block': None,
            },
            'binance-smart-chain': {
                'network': 'binance-smart-chain',
                'contract_address': '',
                'start_block': None,
            },
            'polygon': {
                'network': 'polygon',
                'contract_address': '',
                'start_block': None,
            },
            'avalanche': {
                'network': 'avalanche',
                'contract_address': '',
                'start_block': None,
            },
            'moonriver': {
                'network': 'moonriver',
                'contract_address': '',
                'start_block': None,
            },
            'fantom': {
                'network': 'fantom',
                'contract_address': '',
                'start_block': None,
            },
            'harmony': {
                'network': 'harmony',
                'contract_address': '',
                'start_block': None,
            },
            'arbitrum': {
                'network': 'arbitrum',
                'contract_address': '',
                'start_block': None,
            },
            'aurora': {
                'network': 'aurora',
                'contract_address': '',
                'start_block': None,
            },
        }
    )
