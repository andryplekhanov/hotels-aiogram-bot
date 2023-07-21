from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersStates(StatesGroup):
    """
    Класс реализует состояние пользователя внутри сценария.
    Атрибуты заполняются во время опроса пользователя. Очищаются при каждой новой команде.

    Attributes:
        last_command (str): команда, которую ввёл пользователь.
        city (str): город, в котором ищем отели.
        city_id (str): id города, в котором ищем отели.
        cities (Dict): подходящие по названию города, из которых пользователь выбирает нужный ему.
        amount_hotels (int): количество отелей.
        need_photo (bool): нужно ли загружать фото.
        amount_photo (int): количество фото.
        start_date (datetime.date): дата заезда в отель.
        end_date (datetime.date): дата выезда из отеля.
        start_price (int): минимальная цена за ночь.
        end_price (int): максимальная цена за ночь.
        end_distance (float): максимальная дистанция до центра города.
    """
    last_command = State()
    city = State()
    city_id = State()
    cities = State()
    amount_hotels = State()
    need_photo = State()
    amount_photo = State()
    start_date = State()
    end_date = State()
    start_price = State()
    end_price = State()
    end_distance = State()
