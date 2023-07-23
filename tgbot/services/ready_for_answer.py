from tgbot.config import Config
from tgbot.services.get_hotels import parse_hotels


async def get_prereply_str(states: dict) -> str:
    sort_order = 'дешёвых' if states.get('last_command') == 'lowprice' else 'дорогих'
    prereply_str = f"✅ Ок, ищем: <b>топ {states['amount_hotels']}</b> " \
                   f"самых {sort_order} отелей в городе <b>{states['city_name']}</b>\n" \
                   f"{f'Нужно загрузить фото' if states['amount_photo'] else f'Фото не нужны'}" \
                   f" — <b>{states['amount_photo']}</b> штук\n" \
                   f"Длительность поездки: <b>{states['amount_nights']} ноч.</b> " \
                   f"(с {states['start_date']} по {states['end_date']})."
    return prereply_str


async def low_high_price_answer(states: dict, config: Config) -> str:
    hotels = await parse_hotels(states, config)
    reply_str = 'empty'
    return reply_str
