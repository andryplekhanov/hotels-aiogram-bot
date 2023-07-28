from typing import Tuple, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_city, for_photo, for_hotels, for_history


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


def print_history(requests_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - выбор подходящего запроса из истории.
    """

    keyboard = InlineKeyboardMarkup()
    for data in requests_list:
        date = data.date.strftime("%d.%m.%Y в %H:%M")
        keyboard.add(InlineKeyboardButton(text=f'{date} - {data.command} - {data.city_name}',
                                          callback_data=for_history.new(history_id=data.id)
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


# Клавиатура с выбором действия с историей поиска
history_choice = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Показать историю', callback_data='show_history')
        ],
        [
            InlineKeyboardButton(text='Очистить историю', callback_data='clear_history')
        ],
    ]
)


def show_prev_next_callback(current_page: int, hotel_id: str, hotel_name: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками "Вперёд" и "Назад".
    :return: клавиатура InlineKeyboardMarkup.
    """

    current_page = str(current_page + 1)
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Загрузить фото отеля',
                                 callback_data=for_photo.new(hotel_id=hotel_id, hotel_name=hotel_name))
        ],
        [
            InlineKeyboardButton(text=f'<<<', callback_data='back'),
            InlineKeyboardButton(text=f'{current_page}', callback_data='current_page'),
            InlineKeyboardButton(text=f'>>>', callback_data='forward')
        ]
    ])
    return keyboard
