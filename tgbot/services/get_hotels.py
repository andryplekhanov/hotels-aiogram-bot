import json
from typing import Union, List

from tgbot.config import Config
from tgbot.services.api_requests import request_to_api


async def parse_hotels(states: dict, config: Config) -> Union[dict, None]:
    """
    Функция делает запрос в request_to_api и десериализирует результат. Если запрос получен и десериализация прошла -
    возвращает обработанный результат в виде словаря, иначе None.
    """

    sort = 'PRICE_LOW_TO_HIGH'
    results_size = int(states.get('amount_hotels'))

    if states.get('last_command') == 'highprice':
        results_size = 1000

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
                "adults": states.get('amount_adults')
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": results_size,
        "sort": sort
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.misc.api_key,
        "X-RapidAPI-Host": config.misc.api_host
    }

    response = await request_to_api(url, headers=headers, querystring=payload, method='POST')
    if not response:
        return None
    try:
        all_info = json.loads(response.text)
        hotels_info_list = all_info.get('data', None).get('propertySearch', None).get('properties', None)
        result = await process_hotels_info(hotels_info_list, states)
    except Exception:
        result = None
    return result

    
async def process_hotels_info(hotels_info_list: List[dict], states: dict) -> dict[str, dict]:
    """
    Функция получает список словарей - результат парсинга отелей, выбирает нужную информацию, обрабатывает и складывает
    в словарь hotels_info_dict
    """

    if states.get('last_command') == 'highprice':  # Если была команда 'highprice', то список отелей берем с конца
        hotels_info_list = hotels_info_list[::-1][:int(states.get('amount_hotels'))]

    hotels_info_dict = dict()
    for hotel in hotels_info_list:
        hotel_id = hotel.get('id', None)
        if not hotel_id:
            continue
        hotel_name = hotel.get('name', 'No name')
        price_per_night = hotel.get('price', {}).get('lead', {}).get('amount', 0)
        total_price = round(price_per_night * states.get('amount_nights'), 2)
        distance_city_center = hotel.get('destinationInfo', {}).get('distanceFromDestination', {}).get('value', 0)
        score = hotel.get('reviews', {}).get('score', 0)
        hotels_info_dict[hotel_id] = {
            'name': hotel_name,
            'price_per_night': price_per_night,
            'total_price': total_price,
            'distance_city_center': distance_city_center,
            'score': score,
        }
    return hotels_info_dict
