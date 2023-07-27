import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import history_choice, print_history
from tgbot.misc.factories import for_history
from tgbot.models import orm

logger = logging.getLogger(__name__)


async def history(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите действие:', reply_markup=history_choice)


async def show_history(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    requests = await orm.get_history(call.message.bot.get('db'), call.from_user.id)
    if requests:
        await call.message.answer('Выберите запрос:', reply_markup=print_history(requests))
    else:
        await call.message.answer('История пуста')


async def clarify_history(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    await call.message.answer(f"{callback_data.get('history_id')}")


async def clear_history(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    await call.message.answer('clear_history')


def register_history(dp: Dispatcher):
    dp.register_message_handler(history, commands=["history"], state="*")
    dp.register_callback_query_handler(show_history, text='show_history', state="*")
    dp.register_callback_query_handler(clear_history, text='clear_history', state="*")
    dp.register_callback_query_handler(clarify_history, for_history.filter(), state="*"),
