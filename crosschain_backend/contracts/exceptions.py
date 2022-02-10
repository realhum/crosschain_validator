class ContractNotFound(Exception):
    pass


class ContractMultipleObjectsReturned(Exception):
    pass


class ContractDoesNotExistsInOtherBlockChain(Exception):
    pass


class ContractPaused(Exception):
    pass


class ContractTransactionAlreadyProcessed(Exception):
    pass


class ContractTransactionAlreadyReverted(Exception):
    pass
