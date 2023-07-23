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


# Клавиатура с выбором количества фото
amount_photo = InlineKeyboardMarkup(
    row_width=5, inline_keyboard=[
        [InlineKeyboardButton(text='Не загружать фото', callback_data=for_photo.new(amount=0))],
        [
            InlineKeyboardButton(text=str(num), callback_data=for_photo.new(amount=num)) for num in range(1, 6)
        ],
        [
            InlineKeyboardButton(text=str(num), callback_data=for_photo.new(amount=num)) for num in range(6, 11)
        ],
    ]
)

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
