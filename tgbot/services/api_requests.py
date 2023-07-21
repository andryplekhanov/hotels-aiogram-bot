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
            request = requests.get(url=url, params=querystring, headers=headers)
            if request.status_code == requests.codes.ok:
                return request
            return None
        elif method == 'POST':
            pass  # TODO
    except Exception:
        return None
