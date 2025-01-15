from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import models
from app.settings import get_settings

client = AsyncIOMotorClient("mongodb://localhost:27017")

settings = get_settings()

async def init():
    await init_beanie(database=client[settings.db], document_models=models)
