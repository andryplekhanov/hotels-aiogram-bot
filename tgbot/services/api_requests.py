from typing import Dict, Union
import logging
import requests
from requests.models import Response

logger = logging.getLogger(__name__)


async def request_to_api(
        url: str,
        method: str,
        querystring: Dict,
        headers: Union[Dict, None] = None
) -> Union[Response, None]:
    """
    Функция осуществляет запрос к api. Если ответ == 200: возвращает результат, иначе None.
    """

    logger.info(f"Starting request to API (method: {method}; url: {url})")
    try:
        if method == 'GET':
            response = requests.get(url=url, params=querystring, headers=headers)
        else:
            response = requests.post(url, json=querystring, headers=headers)
        if response.status_code == requests.codes.ok:
            logger.info("request OK")
            return response
        logger.error("Bad request")
        return None
    except Exception as ex:
        logger.error("Bad request:", ex)
        return None
