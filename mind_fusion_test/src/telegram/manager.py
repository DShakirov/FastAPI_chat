from typing import List

from aiogram import Bot
from settings import settings


class TelegramManager:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.bot = Bot(self.token)

    async def send_messages_list(self, text: str, tg_ids: List[int]):
        for tg_id in tg_ids:
            await self.bot.send_message(tg_id, text)

