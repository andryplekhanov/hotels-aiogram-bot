import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.bestdeal import register_bestdeal
from tgbot.handlers.echo import register_echo
from tgbot.handlers.highprice import register_highprice
from tgbot.handlers.search_history import register_history
from tgbot.handlers.lowprice import register_lowprice
from tgbot.handlers.polling import register_polling
from tgbot.handlers.result import register_result
from tgbot.handlers.start import register_start
from tgbot.handlers.help import register_help
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.models.models import Base
from tgbot.models.utils import make_connection_string
from tgbot.services.default_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_start(dp)
    register_help(dp)
    register_lowprice(dp)
    register_highprice(dp)
    register_bestdeal(dp)
    register_polling(dp)
    register_result(dp)
    register_history(dp)

    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(make_connection_string(config=config), future=True, echo=False)

    # Creating DB connections pool
    db_pool = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot["db"] = db_pool

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_default_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
