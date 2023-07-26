import logging

from sqlalchemy import select

from tgbot.models.models import User, Request

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


async def save_search_history(async_session, user_id, state):
    states = await state.get_data()

    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == user_id))
        new_search_history = Request(
            user_id=user.id,
            command=states.get('last_command'),
            city_name=states.get('city_name')
        )
        await session.add(new_search_history)
        await session.commit()
        logger.info(f"Request from '{user_id}' was added to DB")
