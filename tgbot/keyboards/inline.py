from typing import Tuple, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.factories import for_city, for_photo


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


amount_photo = InlineKeyboardMarkup(
    row_width=5, inline_keyboard=[
        [
            InlineKeyboardButton(text='Не загружать фото', callback_data=for_photo.new(amount=0))
        ],
        [
            InlineKeyboardButton(text='1', callback_data=for_photo.new(amount=1)),
            InlineKeyboardButton(text='2', callback_data=for_photo.new(amount=2)),
            InlineKeyboardButton(text='3', callback_data=for_photo.new(amount=3)),
            InlineKeyboardButton(text='4', callback_data=for_photo.new(amount=4)),
            InlineKeyboardButton(text='5', callback_data=for_photo.new(amount=5))
        ],
        [
            InlineKeyboardButton(text='6', callback_data=for_photo.new(amount=6)),
            InlineKeyboardButton(text='7', callback_data=for_photo.new(amount=7)),
            InlineKeyboardButton(text='8', callback_data=for_photo.new(amount=8)),
            InlineKeyboardButton(text='9', callback_data=for_photo.new(amount=9)),
            InlineKeyboardButton(text='10', callback_data=for_photo.new(amount=10)),
        ]
    ]
)
