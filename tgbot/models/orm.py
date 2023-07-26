import logging

from sqlalchemy import select

from tgbot.models.models import User

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
