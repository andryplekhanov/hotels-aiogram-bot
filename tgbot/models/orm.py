import logging

from sqlalchemy import select

from tgbot.models.models import User, Request, Result

logger = logging.getLogger(__name__)


async def add_user(async_session, user_id):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == user_id))
        all_users = user.scalars().all()

        if str(user_id) not in list(map(str, all_users)):
            new_user = User(tg_id=user_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"User '{user_id}' was added to DB")


async def save_search_history(async_session, user_id, state, all_results):
    states = await state.get_data()

    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == user_id))
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
