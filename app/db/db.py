from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import models

client = AsyncIOMotorClient("mongodb://localhost:27017")


async def init():
    await init_beanie(database=client["nexus_dev"], document_models=models)
