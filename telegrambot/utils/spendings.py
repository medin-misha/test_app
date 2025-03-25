import aiohttp
from .base64 import base_encode
from settings import settings

async def create_spending(user_id: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.post(settings.backend_url + "api/spending", json=data, headers=headers) as response:
            print(response.status)
            print(await response.text())
            return await response.json()