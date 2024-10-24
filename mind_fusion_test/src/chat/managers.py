from sqlalchemy import select, insert
from starlette.websockets import WebSocket
from users.models import User
from logger import logger
from typing import List, Dict
from .models import Message, PrivateMessage
from db import async_session_maker
from telegram.tasks import send_messages


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.private_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.active_connections.append((websocket, email))

        if email not in self.private_connections:
            self.private_connections[email] = []
        self.private_connections[email].append(websocket)

    def disconnect(self, websocket: WebSocket, email: str):
        self.active_connections = [
            (conn, email) for conn, email in self.active_connections if conn != websocket
        ]
        if not self.private_connections[email]:
            del self.private_connections[email]

    async def broadcast_message(self, message: str, email: str):
        await self.add_messages_to_database(message, email)
        for connection, email in self.active_connections:
            text = f"New message from client {email}: {message}"
            await connection.send_text(text)

    async def broadcast_disconnect(self, email: str):
        for connection, email in self.active_connections:
            text = f"Client {email} leaved the chat"
            await connection.send_text(text)

    async def add_messages_to_database(self, message: str, email: str):
        user_id = await self._get_user_id_by_email(email)
        await self._insert_message_to_database(message, user_id)

    @staticmethod
    async def _get_user_id_by_email(email: str) -> int:
        async with async_session_maker() as session:
            stmt = select(User.id).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalar()

    @staticmethod
    async def _insert_message_to_database(message: str, user_id: int):
        async with async_session_maker() as session:
            stmt = insert(Message).values(
                message=message,
                from_user_id=user_id
            )
            await session.execute(stmt)
            await session.commit()

    async def send_private_message(self, message: str, from_email: str, to_email: str):
        await self.add_private_message_to_database(message, from_email, to_email)
        text = f"Private message from {from_email}: {message}"
        if to_email in self.private_connections:
            for connection in self.private_connections[to_email]:
                await connection.send_text(text)
        else:
            recipient_tg_id = await self._get_tg_id_by_email(to_email)
            send_messages(text=text, tg_ids=[recipient_tg_id])

    async def add_private_message_to_database(self, message: str, from_email: str, to_email: str):
        sender_id = await self._get_user_id_by_email(from_email)
        recipient_id = await self._get_user_id_by_email(to_email)
        await self._insert_private_message_to_db(message, sender_id, recipient_id)

    @staticmethod
    async def _insert_private_message_to_db(message: str, sender_id: int, recipient_id: int):
        try:
            async with async_session_maker() as session:
                stmt = insert(PrivateMessage).values(
                    message=message,
                    from_user_id=sender_id,
                    to_user_id=recipient_id
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.info(e)

    @staticmethod
    async def _get_tg_id_by_email(email: str) -> int | None:
        async with async_session_maker() as session:
            stmt = select(User.tg_id).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalar()

    def get_online_users(self) -> List[str]:
        return [email for _, email in self.active_connections]