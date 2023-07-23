from typing import Union, List

from tgbot.config import Config
from tgbot.services.api_requests import request_to_api


async def parse_hotels(states: dict, config: Config) -> Union[dict[str, List[dict]], None]:
    """
    Функция делает запрос в request_to_api и десериализирует результат. Если запрос получен и десериализация прошла -
    возвращает обработанный результат в виде словаря, иначе None.
    """

    sort = 'PRICE_HIGH_TO_LOW' if states.get('last_command') == 'highprice' else 'PRICE_LOW_TO_HIGH'

    url = config.misc.url_list
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": states.get('city_id')},
        "checkInDate": {
            "day": int(states.get('start_date').strftime("%d")),
            "month": int(states.get('start_date').strftime("%m")),
            "year": int(states.get('start_date').strftime("%Y"))
        },
        "checkOutDate": {
            "day": int(states.get('end_date').strftime("%d")),
            "month": int(states.get('end_date').strftime("%m")),
            "year": int(states.get('end_date').strftime("%Y"))
        },
        "rooms": [
            {
                "adults": 2
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": int(states.get('amount_hotels')),
        "sort": sort
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.misc.api_key,
        "X-RapidAPI-Host": config.misc.api_host
    }

    response = await request_to_api(url, headers=headers, querystring=payload, method='POST')

    if response:
        print(response.json())
    else:
        print('none')