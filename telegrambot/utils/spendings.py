import aiohttp
from aiogram.types import BufferedInputFile
import io
from .base64 import base_encode
from settings import settings

async def create_spending(user_id: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.post(settings.backend_url + "api/spending", json=data, headers=headers) as response:
            return await response.json()

async def get_spendings(user_id: str, up_date: str, to_date: str) -> BufferedInputFile:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.get(settings.backend_url + f"api/spending/{up_date}/{to_date}", headers=headers) as response:
            result_file_bytes: bytes = await response.read()
            return BufferedInputFile(file=result_file_bytes, filename="отчёт.xls")


async def delete_spendings(user_id: str, spending_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.delete(settings.backend_url + f"api/spending/{spending_id}", headers=headers) as response:
            return True if response.status < 299 else False

async def get_spending_by_id(user_id: str, spending_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.get(settings.backend_url + f"api/spending/{spending_id}", headers=headers) as response:
            return await response.json()


async def put_spending_by_id(user_id: str, spending_id: int, new_spending: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": f"Basic {base_encode(user_id=user_id)}"}
        async with session.put(settings.backend_url + f"api/spending/{spending_id}", headers=headers, json=new_spending) as response:
            return await response.json()