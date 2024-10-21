from tasks import celery
from .manager import TelegramManager
import asyncio
from typing import List


@celery.task
def send_messages(text: str, tg_ids: List[int]):
    manager = TelegramManager()
    asyncio.run_coroutine_threadsafe(manager.send_messages_list(text, tg_ids), asyncio.get_event_loop())
