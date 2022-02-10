# GENERAL
RPC_TEMPLATE = '{}_RPC'
RUBIC_BACKEND_API_URL = "{main_backend_url}/api/tokens/?network={network}&address={token_address}"
DEFAULT_VALUE = '---'
NETWORK_NAMES = {
    'solana': 'solana',
}
###

# WEB3
MAX_ALLOWANCE = 2 ** 256 - 1
MAX_WEI_DIGITS = len(str(MAX_ALLOWANCE))
ETH_LIKE_ADDRESS_LENGTH = 42
ETH_LIKE_ADDRESS_LENGTH_WITHOUT_0x = 40
ETH_LIKE_HASH_LENGTH = 66
DEFAULT_CRYPTO_ADDRESS = '0x0000000000000000000000000000000000000000'
ALTERNATIVE_DEFAULT_CRYPTO_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
DEFAULT_TOKEN_DECIMALS = 18
DEFAULT_FIAT_CURRENCY_DECIMALS = 7
DEFAULT_PLATFORM_FEE_DIVISOR = 1_000_000
###


# LOG MESSAGE TEMPLATES
INFO = 'INFO.\n--------------------------------------\nMESSAGE: {}\n'
SCANNER_INFO = '\nSCANNER INFO.\n--------------------------------------\nMESSAGE: {}\n'
RPC_PROVIDER_ERROR = '\nPRC PROVIDER ERROR.\n--------------------------------------\nMESSAGE: {}\n'
RPC_PROVIDER_INFO = '\nPRC PROVIDER INFO.\n--------------------------------------\nMESSAGE: {}\n'
NETWORK_ERROR = '\nNETWORK ERROR.\n--------------------------------------\nMESSAGE: {}\n'
CONTRACT_ERROR = '\nCONTRACT ERROR.\n--------------------------------------\nMESSAGE: {}\n'
CONTRACT_INFO = '\nCONTRACT INFO.\n--------------------------------------\nMESSAGE: {}\n'
SIGNER_INFO = '\nSIGNER INFO.\n--------------------------------------\nMESSAGE: {}\n'
SIGNER_ERROR = '\nSIGNER ERROR.\n--------------------------------------\nMESSAGE: {}\n'
TRADE_ERROR = '\nTRADE ERROR.\n--------------------------------------\nMESSAGE: {}\n'
TRADE_INFO = '\nTRADE INFO.\n--------------------------------------\nMESSAGE: {}\n'
TRANSACTION_ERROR = '\nTRANSACTION ERROR.\n--------------------------------------\nMESSAGE: {}\n'
TRANSACTION_WARNING = '\nTRANSACTION WARNING.\n--------------------------------------\nMESSAGE: {}\n'
TRANSACTION_INFO = '\nTRANSACTION INFO.\n--------------------------------------\nMESSAGE: {}\n'
TOKEN_ERROR = '\nTOKEN ERROR.\n--------------------------------------\nMESSAGE: {}\n'
UNEXPECTED_ERROR = '\nUNEXPECTED ERROR.\n--------------------------------------\nMESSAGE: {}\n'
REQUEST_ERROR = '\nREQUEST ERROR.\n--------------------------------------\nMESSAGE: {}'
REQUEST_INFO = '\nREQUEST INFO.\n--------------------------------------\nMESSAGE: {}'
RESPONSE_ERROR = '\nRESPONSE ERROR.\n--------------------------------------\nMESSAGE: {}'
RESPONSE_INFO = '\nRESPONSE INFO.\n--------------------------------------\nMESSAGE: {}'
###

# NOTIFIER MESSAGE TEMPLATES
TYPE_MESSAGE_TEMPLATES = {
    'warning': 'Something happened right now\n',
    'error': 'Error has happened\n',
}
###

# COINGECKO
COINGECKO_NETWORKS_NAME = {
    'ethereum': 'ethereum',
    'binance-smart-chain': 'binance-smart-chain',
    'polygon': 'polygon-pos',
    'avalanche': 'avalanche',
    'moonriver': 'moonriver',
    'fantom': 'fantom',
    'solana': 'solana',
    'harmony': 'harmony-shard-0',
    'arbitrum': 'arbitrum-one',
    'aurora': 'aurora',
}
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/{network}/contract/{token_address}"
###

# TOKENS
ETH_LIKE_TYPE = 'ethlike'
SOLANA_LIKE_TYPE = 'solana'
###
