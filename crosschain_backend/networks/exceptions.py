class ProviderNotFound(Exception):
    pass


class ProviderNotLoad(Exception):
    pass


class ProviderNotConnected(Exception):
    pass


class NetworkNotFound(Exception):
    pass


class NetworkMultipleObjectsReturned(Exception):
    pass


class TransactionNotFound(Exception):
    pass


class TransactionMultipleObjectsReturned(Exception):
    pass


class TransactionNotSigned(Exception):
    pass


class TransactionReverted(Exception):
    pass


class TransactionError(Exception):
    pass


class HashNotSigned(Exception):
    pass


class CustomRpcProviderExceedListRange(Exception):
    pass
