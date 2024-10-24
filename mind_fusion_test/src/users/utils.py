from fastapi import Request, Depends
from fastapi_users.jwt import decode_jwt
from db import get_async_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .auth import SECRET_KEY
from .schemas import UserRead


async def get_token(
        request: Request
):
    token = request.cookies.get('fastapiusersauth')
    return token


async def get_user_from_token(
        token: str,
        session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    payload = decode_jwt(token, secret=SECRET_KEY, audience=["fastapi-users:auth"], algorithms=["HS256"])
    user_id = payload.get("sub")
    user = await get_user_from_db(user_id, session)
    return user


async def get_user_from_db(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    stmt = select(User).where(User.id == int(user_id))
    result = await session.execute(stmt)
    return result.scalar()


async def get_users_emails(session: AsyncSession = Depends(get_async_session)):
    stmt = select(User.email)
    result = await session.execute(stmt)
    return result.scalars().all()