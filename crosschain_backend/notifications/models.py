import logging
import requests
from abc import ABC, abstractmethod

from base.support_functions.base import camel_case_split
from crosschain_backend.settings.base import (
    TELEGRAM_BACKEND_URL,
)


class Notifier(ABC):
    """
    Abstract Notifier class with realized methods of sending messages

    :param telegram_url_path: url path for API request to telegram bot
    """

    not_allowed_symbols = (":", "'", "\"",)

    def __init__(self, tx_hash):
        self.tx_hash = tx_hash

    @abstractmethod
    def create_message_body(self) -> dict:
        """
        Abstract method which returns dict in format:
        {
            'message': str
        }
        """

        pass

    def send_telegram_message(self):
        """
        Sends API request with message body to telegram bot
        """

        try:
            data = self.create_message_body()
            requests.post(TELEGRAM_BACKEND_URL, json=data)
        except Exception as e:
            logging.error(str(e))

    @classmethod
    def reformat_message(cls, message):
        if isinstance(message, str):
            for symbol in cls.not_allowed_symbols:
                message = message.replace(symbol, '')

        return message


class ErrorNotifier(Notifier):
    """
    Class for sending error notifications
    """

    error_template = "Error has happened\n" \
                     "{error_name}\n" \
                     "ERROR MESSAGE: {error_text}\n" \
                     "TRANSACTION HASH: {hash}\n"

    def __init__(self, error_name, error_args, tx_hash):
        super().__init__(tx_hash)
        self.error_name = error_name
        self.error_args = error_args

    def create_message_body(self) -> dict:
        """
        Creates error message based on error type
        """

        message = self.error_template.format(
            error_name=camel_case_split(self.error_name).upper(),
            error_text=self.error_args,
            hash=self.tx_hash,
        )

        message = self.reformat_message(message)

        return {
            'message': message
        }
