from datetime import date

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_bot_calendar import DetailedTelegramCalendar
from tgbot.config import Config
from tgbot.keyboards.inline import print_cities
from tgbot.misc.states import UsersStates
from tgbot.services.factories import for_city
from tgbot.services.get_cities import parse_cities_group


async def get_cities_group(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод города.
    Показывает клавиатуру с выбором конкретного города для уточнения.
    """

    answer = message.text
    cities_list = await parse_cities_group(city=answer, config=config)
    if cities_list:
        await message.answer("Пожалуйста, уточните:", reply_markup=print_cities(cities_list))
    else:
        await message.answer("⚠️ Не нахожу такой город. Введите ещё раз.")


async def clarify_city(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    """
        Функция, реагирующая на нажатие кнопки с выбором конкретного города.
        Записывает состояния пользователя 'city_id' и 'city_name' выбранного города.
        Предлагает ввести количество отелей.
        """
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['city_id'] = callback_data.get('city_id')
        data['city_name'] = callback_data.get('city_name')

    await call.message.answer('Сколько отелей найти?')
    await UsersStates.amount_hotels.set()
    await call.message.delete()


async def get_amount_hotels(message: Message, config: Config, state: FSMContext):
    try:
        amount_hotels = int(message.text)
        if 1 <= amount_hotels <= 10:
            async with state.proxy() as data:
                data['amount_hotels'] = amount_hotels
            await message.answer('Желаете загрузить фото отелей? Введите число:\n'
                                 '0 - нет\n'
                                 '10 - загрузить 10 фото.')
            await UsersStates.amount_photo.set()
        else:
            raise ValueError
    except ValueError:
        await message.answer('Введите число от 1 до 10')


async def get_amount_photos(message: Message, config: Config, state: FSMContext):
    try:
        amount_photo = int(message.text)
        if 0 <= amount_photo <= 10:
            async with state.proxy() as data:
                data['amount_photo'] = amount_photo
            calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
            await message.answer('Введите дату заезда', reply_markup=calendar)
        else:
            raise ValueError
    except ValueError:
        await message.answer('Введите число от 1 до 10')


def register_polling(dp: Dispatcher):
    dp.register_message_handler(get_cities_group, state=UsersStates.cities),
    dp.register_callback_query_handler(clarify_city, for_city.filter(), state="*"),
    dp.register_message_handler(get_amount_hotels, state=UsersStates.amount_hotels),
    dp.register_message_handler(get_amount_photos, state=UsersStates.amount_photo),
