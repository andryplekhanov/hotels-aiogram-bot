import json
import logging
from typing import Union, List

from tgbot.config import Config
from tgbot.services.api_requests import request_to_api

logger = logging.getLogger(__name__)


async def parse_hotels(states: dict, config: Config) -> Union[dict, None]:
    """
    Функция делает запрос в request_to_api и десериализирует результат. Если запрос получен и десериализация прошла -
    возвращает обработанный результат в виде словаря, иначе None.
    """

    logger.info("Start hotel parsing")

    sort = 'PRICE_LOW_TO_HIGH'
    results_size = int(states.get('amount_hotels'))
    amount_adults = 1
    start_price, end_price = '', ''

    if states.get('last_command') == 'highprice':
        results_size = 1000
    elif states.get('last_command') == 'bestdeal':
        amount_adults = int(states.get('amount_adults'))
        sort = 'DISTANCE'
        start_price = int(states.get('start_price'))
        end_price = int(states.get('end_price'))

    url = config.misc.url_list
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": states.get('city_id')},
        "checkInDate": {
            "day": states.get('start_date').day,
            "month": states.get('start_date').month,
            "year": states.get('start_date').year
        },
        "checkOutDate": {
            "day": states.get('end_date').day,
            "month": states.get('end_date').month,
            "year": states.get('end_date').year
        },
        "rooms": [
            {
                "adults": amount_adults
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": results_size,
        "sort": sort,
        "filters": {"price": {
            "max": end_price,
            "min": start_price
        }}
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
        logger.info("Start deserialize response json")
        all_info = json.loads(response.text)
        hotels_info_list = all_info.get('data', None).get('propertySearch', None).get('properties', None)
        result = await process_hotels_info(hotels_info_list, states)
    except Exception as ex:
        logger.info(f"Can't deserialize: {ex}")
        result = None
    return result

    
async def process_hotels_info(hotels_info_list: List[dict], states: dict) -> dict[str, dict]:
    """
    Функция получает список словарей - результат парсинга отелей, выбирает нужную информацию, обрабатывает и складывает
    в словарь hotels_info_dict
    """

    logger.info("Start hotels_info processing")

    if states.get('last_command') == 'highprice':  # Если была команда 'highprice', то список отелей берем с конца
        hotels_info_list = hotels_info_list[::-1][:int(states.get('amount_hotels'))]

    hotels_info_dict = dict()
    for hotel in hotels_info_list:
        hotel_id = hotel.get('id', None)
        if not hotel_id:
            continue
        hotel_name = hotel.get('name', 'Нет названия')
        price_per_night = hotel.get('price', {}).get('lead', {}).get('amount', 0)
        total_price = round(price_per_night * states.get('amount_nights'), 2)
        distance_city_center = hotel.get('destinationInfo', {}).get('distanceFromDestination', {}).get('value', 0)
        score = hotel.get('reviews', {}).get('score', 0)
        neighbourhood = hotel.get('neighborhood')
        neighbourhood = neighbourhood.get('name', 'Нет данных') if neighbourhood is not None else 'Нет данных'

        hotels_info_dict[hotel_id] = {
            'name': hotel_name,
            'neighbourhood': neighbourhood,
            'price_per_night': price_per_night,
            'total_price': total_price,
            'distance_city_center': distance_city_center,
            'score': score,
        }
    return hotels_info_dict


async def get_hotel_info_str(hotel_data: dict, states: dict) -> str:
    """
    Функция преобразует данные по отелю из словаря в строку с html.
    Используется для вывода информации через сообщение.
    """

    result = f"<b>🏩 Отель:</b> {hotel_data['name']}\n" \
             f"<b>📍 Район:</b> {hotel_data['neighbourhood']}\n" \
             f"<b>🚕 Расстояние до центра:</b> {hotel_data['distance_city_center']} Км\n" \
             f"<b>💰 Цена за 1 ночь: </b> от {round(hotel_data['price_per_night'], 2)}$\n" \
             f"<b>💰💰 Примерная стоимость за {states.get('amount_nights')} ноч.:</b> {hotel_data['total_price']}$\n" \
             f"<b>⭐️ Рейтинг:</b> {hotel_data['score']}"
    return result
