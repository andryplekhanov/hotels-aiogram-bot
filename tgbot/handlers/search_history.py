from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import history_choice, print_history
from tgbot.misc.factories import for_history
from tgbot.models import orm
from tgbot.models.orm import get_search_result
from tgbot.services.ready_for_answer import process_search_result, print_answer


async def history(message: Message, state: FSMContext) -> None:
    """
    Функция, реагирующая на команду 'history'.
    Показывает инлайн-клавиатуру с выбором действия: показать\очистить историю.
    """

    await state.finish()
    await message.delete()
    await message.answer('Выберите действие:', reply_markup=history_choice)


async def show_history(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие инлайн-кнопки 'Показать историю'.
    Делает запрос к БД и получает историю запросов текущего пользователя.
    Если у пользователя есть история запросов, показывает инлайн-клавиатуру с выбором конкретного запроса.
    Иначе показывает сообщение 'История пуста'.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    requests = await orm.get_history(call.message.bot.get('db'), call.from_user.id)
    if requests:
        await call.message.answer('Выберите запрос:', reply_markup=print_history(requests))
    else:
        await call.message.answer('История пуста')


async def clarify_history(call: CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    """
    Функция, реагирующая на нажатие инлайн-кнопки с выбором конкретного запроса.
    Делает запрос к БД и получает результат конкретного запроса.
    После чего обрабатывает полученный результат (process_search_result) и выводит его с пагинацией.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    search_results = await get_search_result(call.message.bot.get('db'), callback_data.get('history_id'))
    processed_result = await process_search_result(state, search_results)
    await print_answer(call.message, state, processed_result)


async def clear_history(call: CallbackQuery) -> None:
    """
    Функция, реагирующая на нажатие инлайн-кнопки 'Очистить историю'.
    Делает запрос к БД и получает результат - булево значение.
    Если результат True - выводит сообщение 'История очищена'.
    Иначе - выводит сообщение 'История пуста'.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    is_clearing_ok = await orm.clear_history(call.message.bot.get('db'), call.from_user.id)
    if is_clearing_ok:
        await call.message.answer('История очищена')
    else:
        await call.message.answer('История пуста')


def register_history(dp: Dispatcher):
    dp.register_message_handler(history, commands=["history"], state="*")
    dp.register_callback_query_handler(show_history, text='show_history', state="*")
    dp.register_callback_query_handler(clear_history, text='clear_history', state="*")
    dp.register_callback_query_handler(clarify_history, for_history.filter(), state="*"),
