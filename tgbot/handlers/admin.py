from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(message: Message) -> None:
    """
    Функция, реагирующая на команду 'start' от администратора.
    Администраторы указываются в .env файле (ADMINS).
    """
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
