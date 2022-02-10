from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def _get_response(data_to_response, status_to_response=HTTP_200_OK):
    """
    Возвращает объект Response.
    ---
    Принимаемые параметры:
    - data_to_response : string | dict
    - status_to_response : int, по-умолчанию - 200
    """
    return Response(
        data=data_to_response,
        status=status_to_response,
    )
