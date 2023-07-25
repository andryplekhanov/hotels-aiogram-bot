from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import show_prev_next_callback
from tgbot.misc.factories import for_photo


async def flipping_pages_back(call: CallbackQuery, state: FSMContext):
    """
    Функция-пагинатор для перелистывания НАЗАД страниц с результатом поиска
    """

    try:
        async with state.proxy() as data:
            current_page = data.get('current_page')

            if current_page == 0:
                current_page = len(data.get('result')) - 1
            else:
                current_page = current_page - 1
            data['current_page'] = current_page

        async with state.proxy() as data:
            await call.message.edit_text(
                data.get('result')[data.get('current_page')][1],
                reply_markup=show_prev_next_callback(data.get('current_page'),
                                                     data.get('result')[data.get('current_page')][0])
            )
    except Exception:
        pass


async def flipping_pages_forward(call: CallbackQuery, state: FSMContext):
    """
    Функция-пагинатор для перелистывания ВПЕРЕД страниц с результатом поиска
    """

    try:
        async with state.proxy() as data:
            current_page = data.get('current_page')
            if current_page == len(data.get('result')) - 1:
                current_page = 0
            else:
                current_page = current_page + 1
            data['current_page'] = current_page

        async with state.proxy() as data:
            await call.message.edit_text(
                data.get('result')[data.get('current_page')][1],
                reply_markup=show_prev_next_callback(data.get('current_page'),
                                                     data.get('result')[data.get('current_page')][0])
            )
    except Exception:
        pass


async def get_photos(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    """
    Функция, ожидающая нажатие кнопки "Загрузить фото отеля".
    Вызывает парсер фотографий к конкретному отелю. ID отеля находится в callback_data.
    Выводит медиагруппу фото.
    """

    hotel_id = callback_data.get('hotel_id')
    # TODO
    await call.message.answer(hotel_id)


def register_result(dp: Dispatcher):
    dp.register_callback_query_handler(get_photos, for_photo.filter(), state="*"),
    dp.register_callback_query_handler(flipping_pages_back, text='back', state="*")
    dp.register_callback_query_handler(flipping_pages_forward, text='forward', state="*")
