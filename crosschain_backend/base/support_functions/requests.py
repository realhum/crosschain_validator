from logging import exception
from requests import get as request_get

from rest_framework.status import HTTP_200_OK


def send_get_request(url, params=None):
    """
        Return HTTP GET decoded JSON response as dict.
    """
    response = request_get(url, params=params)

    if response.status_code != HTTP_200_OK:
        exception(response)

        return ''

    return response.json()
