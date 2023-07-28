import logging
from typing import Union, Sequence

from aiogram.dispatcher import FSMContext
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.models.models import User, Request, Result

logger = logging.getLogger(__name__)


async def add_user(async_session: async_sessionmaker, user_id: int) -> None:
    """
    Функция делает запрос к БД, получает всех сохранённых пользователей.
    Если текущего пользователя нет в списке, то сохраняет его в БД.
    """

    async with async_session() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        all_users = user.scalars().all()

        if str(user_id) not in list(map(str, all_users)):
            new_user = User(id=user_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"User '{user_id}' was added to DB")


async def save_search_history(
        async_session: async_sessionmaker,
        user_id: int,
        state: FSMContext,
        all_results: list) -> None:
    """
    Функция сохраняет результат поиска для конкретного пользователя (user_id).
    Создаётся экземпляр класса Request в связке с User (foreign key).
    Создаётся экземпляр класса Result в связке с Request (foreign key).
    """

    states = await state.get_data()

    async with async_session() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        my_user = user.scalars().first()

        new_search_history = Request(
            user_id=my_user.id,
            command=states.get('last_command'),
            city_name=states.get('city_name')
        )
        session.add(new_search_history)
        await session.commit()

        for hotel in all_results:
            new_result = Result(
                request_id=new_search_history.id,
                hotel_id=hotel[0],
                hotel_name=hotel[1],
                result_str=hotel[2]
            )
            session.add(new_result)

        await session.commit()
        logger.info(f"History from '{user_id}' was added to DB")


async def get_history(async_session: async_sessionmaker, user_id: int) -> Union[Sequence, None]:
    """
    Функция делает запрос к БД и возвращает историю запросов конкретного пользователя либо None.
    """

    async with async_session() as session:
        try:
            requests = await session.execute(select(Request).where(Request.user_id == user_id))
            return requests.scalars().all()
        except Exception as ex:
            logger.error(f"FAIL 'get_history': {ex}")
            return None


async def clear_history(async_session: async_sessionmaker, user_id: int) -> bool:
    """
    Функция удаляет историю конкретного пользователя из БД.
    """

    async with async_session() as session:
        try:
            await session.execute(delete(Request).where(Request.user_id == user_id))
            await session.commit()
            logger.info(f"History from '{user_id}' was removed from DB")
            return True
        except Exception as ex:
            logger.error(f"FAIL 'clear_history': {ex}")
            return False


async def get_search_result(async_session: async_sessionmaker, history_id: str) -> Union[Sequence, None]:
    """
    Функция делает запрос к БД и возвращает результат конкретного запроса либо None.
    """

    async with async_session() as session:
        try:
            results = await session.execute(select(Result).where(Result.request_id == int(history_id)))
            return results.scalars().all()
        except Exception as ex:
            logger.error(f"FAIL 'get_search_result': {ex}")
            return None
