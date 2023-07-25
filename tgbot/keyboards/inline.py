from typing import Tuple, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_city, for_photo, for_hotels


def print_cities(cities_list: List[Tuple]) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - выбор подходящего по названию города, из которых пользователь выбирает нужный ему.
    """

    keyboard = InlineKeyboardMarkup()
    for data in cities_list:
        city_name = data[0][:19]
        keyboard.add(InlineKeyboardButton(text=f'{city_name} ({data[1]})',
                                          callback_data=for_city.new(city_id=data[2], city_name=city_name)
                                          ))
    return keyboard


# Клавиатура с выбором количества отелей
amount_hotels = InlineKeyboardMarkup(
    row_width=5, inline_keyboard=[
        [
            InlineKeyboardButton(text=str(num), callback_data=for_hotels.new(amount=num)) for num in range(1, 6)
        ],
        [
            InlineKeyboardButton(text=str(num), callback_data=for_hotels.new(amount=num)) for num in range(6, 11)
        ],
    ]
)


def show_prev_next_callback(current_page: int, hotel_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками "Вперёд" и "Назад".
    :return: клавиатура InlineKeyboardMarkup.
    """

    current_page = str(current_page + 1)
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Загрузить фото отеля', callback_data=for_photo.new(hotel_id=hotel_id))
        ],
        [
            InlineKeyboardButton(text=f'<<<', callback_data='back'),
            InlineKeyboardButton(text=f'{current_page}', callback_data='current_page'),
            InlineKeyboardButton(text=f'>>>', callback_data='forward')
        ]
    ])
    return keyboard
