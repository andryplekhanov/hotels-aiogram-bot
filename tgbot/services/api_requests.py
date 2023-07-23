from typing import Dict, Union

import requests
from requests.models import Response


async def request_to_api(
        url: str,
        method: str,
        querystring: Dict,
        headers: Union[Dict, None] = None
) -> Union[Response, None]:
    """
    Функция осуществляет запрос к api. Если ответ == 200: возвращает результат, иначе None.
    """

    try:
        if method == 'GET':
            response = requests.get(url=url, params=querystring, headers=headers)
        else:
            response = requests.post(url, json=querystring, headers=headers)
        if response.status_code == requests.codes.ok:
            return response
        return None
    except Exception:
        return None
