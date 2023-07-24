import logging

from tgbot.config import Config
from tgbot.services.get_hotels import parse_hotels, get_hotel_info_str
from aiogram.types import Message

logger = logging.getLogger(__name__)


async def get_prereply_str(states: dict) -> str:
    sort_order = 'дешёвых' if states.get('last_command') == 'lowprice' else 'дорогих'
    prereply_str = f"✅ Ок, ищу: <b>топ {states['amount_hotels']}</b> " \
                   f"самых {sort_order} отелей в городе <b>{states['city_name']}</b>\n" \
                   f"{f'Нужно загрузить фото' if states['amount_photo'] else f'Фото не нужны'}" \
                   f" — <b>{states['amount_photo']}</b> штук\n" \
                   f"Количество гостей: <b>{states['amount_adults']} взрослых</b>\n" \
                   f"Длительность поездки: <b>{states['amount_nights']} ноч.</b> " \
                   f"(с {states['start_date'].strftime('%d.%m.%Y')} по {states['end_date'].strftime('%d.%m.%Y')})."
    return prereply_str


async def low_high_price_answer(message: Message, states: dict, config: Config) -> None:
    logger.info("Start 'low_high_price_answer'")
    hotels = await parse_hotels(states, config)

    if hotels:
        logger.info("got hotels")
        for h_id, h_info in hotels.items():
            result_str = await get_hotel_info_str(h_info, states)
            await message.answer(result_str, parse_mode='html')
    else:
        logger.info("can't get hotels")
        await message.answer("⚠️ Ничего не найдено по вашему запросу. Попробуйте ещё раз.")
