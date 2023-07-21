from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import Config
from tgbot.keyboards.inline import print_cities
from tgbot.misc.states import UsersStates
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


def register_polling(dp: Dispatcher):
    dp.register_message_handler(get_cities_group, state=UsersStates.cities),
