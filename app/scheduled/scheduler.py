from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.settings import get_settings

settings = get_settings()

jobstores = {
    "default": MongoDBJobStore(settings.db, "jobs", host=settings.db_connection_string)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)
