from multiprocessing import Pool

from .base import Scanner
from .handlers import VALIDATOR_HANDLERS


def get_scanner(
    name: str,
    network_title: str,
    contract_address: str,
    start_block: int = None,
):
    return Scanner(
        name=name,
        network=network_title,
        contract=contract_address,
        events=(
            'TransferTokensToOtherBlockchainUser',
            'TransferCryptoToOtherBlockchainUser',
            # 'TransferFromOtherBlockchain',
        ),
        event_handlers=VALIDATOR_HANDLERS,
        start_block=start_block,
    )


def start_scanners(scanners: dict):
    """
    Starts scanner instances in proccess pool.

    ---

    :scanners: dict
    {
        '<scanner_name aka network_title>': {
            'network': '<network_title>',
            'contract_address': 'contract_address',
            'start_block': int,
        },
        ...
    }
    """
    with Pool(processes=len(scanners)) as pool:
        for scanner, value in scanners.items():
            scanner_instance = get_scanner(
                name=f'{scanner}-scanner',
                network_title=value.get('network'),
                contract_address=value.get('contract_address'),
                start_block=value.get('start_block'),
            )

            pool.apply_async(scanner_instance.start())
