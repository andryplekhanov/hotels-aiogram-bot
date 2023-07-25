from datetime import timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from tgbot.config import Config
from tgbot.keyboards.inline import print_cities, amount_hotels
from tgbot.misc.factories import for_city, for_hotels
from tgbot.misc.states import UsersStates
from tgbot.services.get_cities import parse_cities_group
from tgbot.services.ready_for_answer import print_answer, get_prereply_str


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
        Предлагает ввести количество отелей через инлайн-клавиатуру.
        """
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['city_id'] = callback_data.get('city_id')
        data['city_name'] = callback_data.get('city_name')

    await call.message.answer('Сколько отелей найти?', reply_markup=amount_hotels)
    await UsersStates.amount_hotels.set()
    await call.message.delete()


async def get_amount_hotels(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    """
    Функция, ожидающая ввод количества отелей.
    Записывает состояние пользователя 'amount_hotels'.
    Показывает клавиатуру с выбором количества фотографий.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    hotels_number = callback_data.get('amount')
    async with state.proxy() as data:
        data['amount_hotels'] = hotels_number
    await state.reset_state(with_data=False)
    await call.message.answer('Введите дату заезда', reply_markup=await DialogCalendar().start_calendar())


async def process_startdate_calendar(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Функция, ожидающая ввод даты заезда.
    Записывает состояние пользователя 'start_date'.
    Запрашивает пользователя количество ночей.
    """

    selected, sdate = await DialogCalendar().process_selection(call, callback_data)
    if selected:
        # await call.message.answer(f'{sdate.strftime("%d.%m.%Y")}')
        async with state.proxy() as data:
            data['start_date'] = sdate
        await UsersStates.amount_nights.set()
        await call.message.answer('Введите количество ночей')


async def get_amount_nights(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод количества ночей.
    Записывает состояние пользователя 'amount_nights' и 'end_date'.
    Если была команда 'highprice' или 'lowprice', завершает опрос и вызывает функцию подготовки ответа.
    Иначе, продолжает опрос и запрашивает количество гостей.
    """

    answer = message.text
    try:
        nights_num = int(answer)
        if nights_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['amount_nights'] = nights_num
                data['end_date'] = data.get('start_date') + timedelta(nights_num)
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")

    states = await state.get_data()

    if states.get('last_command') in ['highprice', 'lowprice']:
        prereply_str = await get_prereply_str(state)
        await message.answer(prereply_str)
        await print_answer(message, config, state)
        await message.answer(f"Введите ещё какую-нибудь команду!\nНапример: <b>/help</b>", parse_mode="html")
    else:
        await UsersStates.amount_adults.set()
        await message.answer("Введите количество взрослых гостей на 1 номер:")


async def get_amount_adults(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод количества взрослых.
    Записывает состояние пользователя 'amount_adults' и предлагает ввести минимальную цену за ночь.
    """

    answer = message.text
    try:
        adults_num = int(answer)
        if adults_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['amount_adults'] = adults_num
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")

    await UsersStates.start_price.set()
    await message.answer('Введите минимальную цену за ночь $:')


async def get_start_price(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод количества $.
    Записывает состояние пользователя 'start_price' и предлагает ввести максимальную цену за ночь.
    """

    answer = message.text
    try:
        price_num = int(answer)
        if price_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['start_price'] = price_num
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")

    await UsersStates.end_price.set()
    await message.answer("Введите максимальную цену за ночь $:")


async def get_end_price(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод количества $.
    Записывает состояние пользователя 'end_price' и предлагает ввести максимальное расстояние до цента.
    """

    answer = message.text
    try:
        price_num = int(answer)
        if price_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['end_price'] = price_num
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")

    await UsersStates.end_distance.set()
    await message.answer("Введите максимальное расстояние до цента в км:")


async def get_end_distance(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод максимального расстояния до центра.
    Записывает состояние пользователя 'end_distance', завершает опрос и
    вызывает функцию для подготовки ответа на запрос пользователя.
    """

    answer = message.text
    try:
        distance_num = int(answer)
        if distance_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['end_distance'] = distance_num
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")

    prereply_str = await get_prereply_str(state)
    await message.answer(prereply_str)
    await print_answer(message, config, state)
    await message.answer(f"Введите ещё какую-нибудь команду!\nНапример: <b>/help</b>", parse_mode="html")


def register_polling(dp: Dispatcher):
    dp.register_message_handler(get_cities_group, state=UsersStates.cities),
    dp.register_message_handler(get_amount_nights, state=UsersStates.amount_nights),
    dp.register_message_handler(get_amount_adults, state=UsersStates.amount_adults),
    dp.register_message_handler(get_start_price, state=UsersStates.start_price),
    dp.register_message_handler(get_end_price, state=UsersStates.end_price),
    dp.register_message_handler(get_end_distance, state=UsersStates.end_distance),
    dp.register_callback_query_handler(clarify_city, for_city.filter(), state="*"),
    dp.register_callback_query_handler(get_amount_hotels, for_hotels.filter(), state="*"),
    dp.register_callback_query_handler(process_startdate_calendar, dialog_cal_callback.filter()),
