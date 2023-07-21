from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Топ самых дешёвых отелей в городе"),
    ('highprice', "Топ самых дорогих отелей в городе"),
    ('bestdeal', "Настраиваемый поиск отелей"),
    ('history', "История поиска"),
)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[BotCommand(*i) for i in DEFAULT_COMMANDS],
        scope=BotCommandScopeDefault()
    )


async def get_default_commands():
    return '\n'.join([f'<b>/{command}</b> - {desc}' for command, desc in DEFAULT_COMMANDS])
