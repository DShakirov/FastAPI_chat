from db import async_session_maker
from typing import List
from users.models import User
from sqlalchemy import select


async def get_offline_users_tg_id(active_users: List[str]):
    async with async_session_maker() as session:
        stmt = select(User.tg_id).where(~User.email.in_(active_users))
        results = await session.execute(stmt)
    return results.scalars().all()
