import json
import logging

from aiogram import types
from typing import Union, List

from tgbot.config import Config
from tgbot.services.api_requests import request_to_api

logger = logging.getLogger(__name__)


async def parse_photos(hotel_id: str, states: dict, config: Config) -> Union[types.MediaGroup, None]:
    """
    Функция делает запрос в request_to_api и десериализирует результат. Если запрос получен и десериализация прошла -
    возвращает обработанный результат в виде медиагруппы, иначе None.
    """

    logger.info("Start photo parsing")

    url = config.misc.url_detail

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id
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
        photos_list = all_info.get('data', None).get('propertyInfo', None).get('propertyGallery', None).get('images', None)
        result = await process_photos(photos_list)
    except Exception as ex:
        logger.info(f"FAIL: can't deserialize photo: {ex}")
        result = None
    return result

    
async def process_photos(photos_list: List[dict]) -> Union[types.MediaGroup, None]:
    """
    Функция получает список словарей - результат парсинга фоток, выбирает нужную информацию, обрабатывает и складывает
    в медиагрупу.
    """

    logger.info("Start photo processing")

    media = types.MediaGroup()
    for photo_info in photos_list:
        if len(media.to_python()) >= 10:
            break
        try:
            photo = photo_info.get('image', {}).get('url', None)
            media.attach_photo(photo)
        except Exception as ex:
            logger.info("No photo", ex)
            continue
    if media:
        logger.info("SUCCESS: got photo")
        return media
    return None
