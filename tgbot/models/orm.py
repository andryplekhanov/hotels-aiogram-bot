import logging

from sqlalchemy import select

from tgbot.models.models import User, Request, Result

logger = logging.getLogger(__name__)


async def add_user(async_session, user_id):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        all_users = user.scalars().all()

        if str(user_id) not in list(map(str, all_users)):
            new_user = User(id=user_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"User '{user_id}' was added to DB")


async def save_search_history(async_session, user_id, state, all_results):
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


async def get_history(async_session, user_id):
    async with async_session() as session:
        try:
            requests = await session.execute(select(Request).where(Request.user_id == user_id))
            return requests.scalars().all()
        except Exception as ex:
            logger.error(f"FAIL 'get_history': {ex}")
            return None


async def get_search_result(async_session, history_id):
    async with async_session() as session:
        try:
            results = await session.execute(select(Result).where(Result.request_id == int(history_id)))
            return results.scalars().all()
        except Exception as ex:
            logger.error(f"FAIL 'get_search_result': {ex}")
            return None
