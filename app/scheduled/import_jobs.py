from pprint import pprint

from app.external_services import openalex_service
from app.scheduled.models import ImportJobId, Cursor
from app.utils.job_utils import increase_cursor


async def openalex_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run openalex job with {n_batches} and {keywords} and {cursor}")
    page = cursor["batch_id"] + 1
    page_size = cursor["batch_size"]
    topic_ids = await openalex_service.fetch_topic_ids(keywords)
    # TODO batch from here
    works = await openalex_service.fetch_works(topic_ids, page, page_size)
    pprint(works)
    increase_cursor(ImportJobId.OPENALEX_IMPORT_JOB)


def orcid_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run orcid job with {n_batches} and {keywords} and {cursor}")
    increase_cursor(ImportJobId.ORCID_IMPORT_JOB)


def dblp_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run dblp job with {n_batches} and {keywords} and {cursor}")
    increase_cursor(ImportJobId.DBLP_IMPORT_JOB)


import_job_map = {
    ImportJobId.OPENALEX_IMPORT_JOB: openalex_import_job,
    ImportJobId.ORCID_IMPORT_JOB: orcid_import_job,
    ImportJobId.DBLP_IMPORT_JOB: dblp_import_job
}
