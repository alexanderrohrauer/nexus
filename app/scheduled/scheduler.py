from enum import Enum

from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduled import import_jobs

jobstores = {
    # TODO configure
    "default": MongoDBJobStore("nexus_dev", "jobs")
}
# TODO implement UTC one day
scheduler = AsyncIOScheduler(jobstores=jobstores)


class ImportJobId(Enum):
    OPENALEX_IMPORT_JOB = "openalex_import_job"
    ORCID_IMPORT_JOB = "orcid_import_job"
    DBLP_IMPORT_JOB = "dblp_import_job"


import_job_map = {
    ImportJobId.OPENALEX_IMPORT_JOB: import_jobs.openalex_import_job,
    ImportJobId.ORCID_IMPORT_JOB: import_jobs.orcid_import_job,
    ImportJobId.DBLP_IMPORT_JOB: import_jobs.dblp_import_job
}
