from typing import List
from db import get_async_session
from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.websockets import WebSocket, WebSocketDisconnect
from .schemas import MessageModel
from .models import Message
from .managers import ConnectionManager
from .utils import get_offline_users_tg_id
from telegram.tasks import send_messages
from logger import logger


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> List[MessageModel]:
    logger.info("Fetching messages")
    query = select(Message).options(joinedload(Message.from_user)).order_by(Message.id.desc()).limit(5)
    messages = await session.execute(query)
    results = messages.scalars().all()
    return results


@router.websocket("/ws/{client_email}")
async def websocket_endpoint(
        websocket: WebSocket,
        client_email: str,
):
    await manager.connect(websocket, client_email)
    logger.info(f"{client_email} has connected to chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast_message(data, email=client_email)
            logger.info(f"{client_email} has wrote to chat: {data}")
            active_connections = manager.get_online_users()
            offline_users_tg_ids = await get_offline_users_tg_id(active_connections)
            logger.info(f"Send telegram message to {offline_users_tg_ids}")
            text = f"{client_email} has wrote to chat: {data}"
            send_messages(text=text, tg_ids=offline_users_tg_ids)

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_email)
        logger.info(f"{client_email} disconnected")
        await manager.broadcast_disconnect(client_email)
