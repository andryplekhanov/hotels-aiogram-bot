import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import Config
from tgbot.keyboards.inline import show_prev_next_callback
from tgbot.services.get_hotels import parse_hotels, get_hotel_info_str

logger = logging.getLogger(__name__)


async def get_prereply_str(state: FSMContext) -> str:
    states = await state.get_data()
    sort_order = 'дешёвых' if states.get('last_command') == 'lowprice' else 'дорогих'

    if states.get('last_command') in ['highprice', 'lowprice']:
        prereply_str = f"✅ Ок, ищу: <b>топ {states['amount_hotels']}</b> " \
                       f"самых {sort_order} отелей в городе <b>{states['city_name']}</b>\n" \
                       f"Длительность поездки: <b>{states['amount_nights']} ноч.</b> " \
                       f"(с {states['start_date'].strftime('%d.%m.%Y')} по {states['end_date'].strftime('%d.%m.%Y')})."
    else:
        prereply_str = f"✅ Ок, ищем: <b>топ {states['amount_hotels']}</b> отелей в городе " \
                       f"<b>{states['city_name']}</b>\n" \
                       f"В ценовом диапазоне <b>от {states['start_price']}$ до {states['end_price']}$</b>\n" \
                       f"Максимальная удаленность от центра: <b>{states['end_distance']} Км</b>\n" \
                       f"Количество гостей: <b>{states['amount_adults']} взрослых</b>\n" \
                       f"Длительность поездки: <b>{states['amount_nights']} ноч.</b> " \
                       f"(с {states['start_date'].strftime('%d.%m.%Y')} по {states['end_date'].strftime('%d.%m.%Y')})."
    return prereply_str


async def print_answer(message: Message, config: Config, state: FSMContext) -> None:
    logger.info("Start 'print_answer'")
    states = await state.get_data()
    hotels = await parse_hotels(states, config)

    if hotels:
        logger.info("SUCCESS: got hotels")
        await print_nophoto_answer(message, state, hotels)
    else:
        logger.info("FAIL: can't get hotels")
        await message.answer("⚠️ Ничего не найдено по вашему запросу. Попробуйте ещё раз.")


async def print_nophoto_answer(message: Message, state: FSMContext, hotels: dict) -> None:
    h_info_list = []
    for h_id, h_info in hotels.items():
        hotel_name = h_info['name']
        result_str = await get_hotel_info_str(h_info, state)
        h_info_list.append((h_id, hotel_name, result_str))

    async with state.proxy() as data:
        data['result'] = h_info_list
        current_page = 0
        data['current_page'] = current_page
        await message.answer(data.get('result')[current_page][2],
                             reply_markup=show_prev_next_callback(
                                 current_page=data.get('current_page'),
                                 hotel_id=data.get('result')[current_page][0],
                                 hotel_name=data.get('result')[current_page][1]
                             )
        )
