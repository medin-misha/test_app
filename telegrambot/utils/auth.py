import aiohttp
from typing import Dict
from settings import settings
from .base64 import base_encode


async def registration(user_id: int) -> int:
    async with aiohttp.ClientSession() as session:
        data: Dict[str, str] = {
            "chat_id": str(user_id),
        }
        async with session.post(
            url=settings.backend_url + "api/users", json=data
        ) as response:
            return response.status
