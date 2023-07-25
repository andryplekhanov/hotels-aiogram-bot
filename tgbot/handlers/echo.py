from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.services.default_commands import get_default_commands


async def bot_echo(message: types.Message):
    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


async def bot_echo_all(message: types.Message, state: FSMContext):
    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
