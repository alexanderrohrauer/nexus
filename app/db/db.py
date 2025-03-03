from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import models
from app.settings import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.db_connection_string)

async def init():
    await init_beanie(database=client[settings.db], document_models=models)
