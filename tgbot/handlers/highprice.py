from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersStates


async def highprice(message: Message, state: FSMContext) -> None:
    """
    Функция, реагирующая на команду 'highprice'.
    Записывает состояние пользователя 'last_command' и предлагает ввести город.
    """

    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'highprice'
    await message.answer('Введите город')
    await UsersStates.cities.set()


def register_highprice(dp: Dispatcher):
    dp.register_message_handler(highprice, commands=['highprice'], state='*')
