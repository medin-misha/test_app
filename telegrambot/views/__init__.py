__all__ = ("main_router", "spending_router")

from aiogram import Router
from .base import start_router
from .spendings import spending_router

main_router = Router(name="main_router")

main_router.include_routers(start_router, spending_router)
