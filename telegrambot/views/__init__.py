__all__ = ("main_router",)

from aiogram import Router
from .base import start_router

main_router = Router(name="main_router")

main_router.include_routers(
    start_router
)