from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersStates


async def bestdeal(message: Message, state: FSMContext) -> None :
    """
    Функция, реагирующая на команду 'bestdeal'.
    Записывает состояние пользователя 'last_command' и предлагает ввести город.
    """

    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'bestdeal'
    await message.answer('Введите город')
    await UsersStates.cities.set()


def register_bestdeal(dp: Dispatcher):
    dp.register_message_handler(bestdeal, commands=['bestdeal'], state='*')
