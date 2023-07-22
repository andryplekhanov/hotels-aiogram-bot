from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from tgbot.config import Config
from tgbot.keyboards.inline import print_cities, amount_photo, amount_hotels
from tgbot.misc.states import UsersStates
from tgbot.services.factories import for_city, for_photo, for_hotels
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
    await call.message.answer('Желаете загрузить фото отелей?', reply_markup=amount_photo)


async def get_amount_photos(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    """
    Функция, ожидающая ввод количества фотографий.
    Записывает состояние пользователя 'amount_photo'.
    Показывает клавиатуру с выбором даты заезда.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    amount_photos = callback_data.get('amount')
    async with state.proxy() as data:
        data['amount_photo'] = amount_photos
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
        await call.message.answer(f'{sdate.strftime("%d.%m.%Y")}')
        async with state.proxy() as data:
            data['start_date'] = sdate
        await UsersStates.amount_nights.set()
        await call.message.answer('Введите количество ночей')


async def get_amount_nights(message: Message, config: Config, state: FSMContext):
    """
    Функция, ожидающая ввод количества ночей.
    Записывает состояние пользователя 'amount_nights'.
    ДОПИСАТЬ ТЕКСТ
    """

    answer = message.text
    try:
        nights_num = int(answer)
        if nights_num <= 0:
            raise ValueError
        else:
            async with state.proxy() as data:
                data['amount_nights'] = nights_num
            states = await state.get_data()
            print(states)
    except ValueError:
        await message.answer("⚠️ Введите число больше нуля")


def register_polling(dp: Dispatcher):
    dp.register_message_handler(get_cities_group, state=UsersStates.cities),
    dp.register_message_handler(get_amount_nights, state=UsersStates.amount_nights),
    dp.register_callback_query_handler(clarify_city, for_city.filter(), state="*"),
    dp.register_callback_query_handler(get_amount_hotels, for_hotels.filter(), state="*"),
    dp.register_callback_query_handler(get_amount_photos, for_photo.filter(), state="*"),
    dp.register_callback_query_handler(process_startdate_calendar, dialog_cal_callback.filter()),
