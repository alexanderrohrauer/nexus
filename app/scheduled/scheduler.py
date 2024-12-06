from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

jobstores = {
    # TODO configure
    "default": MongoDBJobStore("nexus_dev", "jobs")
}
# TODO implement UTC one day
scheduler = AsyncIOScheduler(jobstores=jobstores)
