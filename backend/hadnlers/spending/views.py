from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import db_helper, Spending

router = APIRouter(prefix="/api/spending", tags=["spending"])
