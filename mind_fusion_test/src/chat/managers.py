from sqlalchemy import select, insert
from starlette.websockets import WebSocket
from users.models import User
from users.schemas import UserRead
from typing import List
from .models import Message
from db import async_session_maker


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.active_connections.append((websocket, email))

    def disconnect(self, websocket: WebSocket, email: str):
        self.active_connections = [
            (conn, email) for conn, email in self.active_connections if conn != websocket
        ]

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

    def get_online_users(self) -> List[str]:
        return [email for _, email in self.active_connections]