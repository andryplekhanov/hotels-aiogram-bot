from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersStates


async def lowprice(message: Message, state: FSMContext) -> None:
    """
    Функция, реагирующая на команду 'lowprice'.
    Записывает состояние пользователя 'last_command' и предлагает ввести город.
    """

    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'lowprice'
    await message.answer('Введите город')
    await UsersStates.cities.set()


def register_lowprice(dp: Dispatcher):
    dp.register_message_handler(lowprice, commands=['lowprice'], state='*')
