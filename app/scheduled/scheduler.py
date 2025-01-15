from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.settings import get_settings

settings = get_settings()

jobstores = {
    # TODO configure
    "default": MongoDBJobStore(settings.db, "jobs")
}
# TODO implement UTC one day
scheduler = AsyncIOScheduler(jobstores=jobstores)
