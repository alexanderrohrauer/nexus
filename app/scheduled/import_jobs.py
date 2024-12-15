import asyncio
import logging

from app.external_services import openalex_service, dblp_service
from app.scheduled.models import ImportJobId, Cursor
from app.services import openalex_dataprocess_service, works_service, researchers_service, institutions_service, \
    dblp_dataprocess_service
from app.utils.job_utils import increase_cursor

lock = asyncio.Lock()

logger = logging.getLogger("uvicorn.error")


async def openalex_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run openalex job with {n_batches} and {keywords} and {cursor}")
    # topic_ids = await openalex_service.fetch_topics(keywords)
    # TODO here stop fetching when no results are returned (or latest items are already inserted)
    page = cursor["batch_id"] + 1
    page_size = cursor["batch_size"]
    for i in range(n_batches):
        works = await openalex_service.fetch_works(keywords, page, page_size)
        authors = await openalex_service.fetch_authors_for_works(works)
        institutions = await openalex_service.fetch_institutions_for_authors(authors)
        institutions = openalex_dataprocess_service.restructure_institutions(institutions)
        async with lock:
            await institutions_service.upsert_many(institutions)
        researchers = openalex_dataprocess_service.restructure_authors(authors, institutions)
        async with lock:
            await researchers_service.upsert_many_openalex(researchers)
        works = openalex_dataprocess_service.restructure_works(works, researchers)
        # TODO do cleansing
        async with lock:
            await works_service.insert_and_link(works)
        page = page + 1

    logger.info("OpenAlex import finished")
    increase_cursor(ImportJobId.OPENALEX_IMPORT_JOB)


def orcid_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run orcid job with {n_batches} and {keywords} and {cursor}")
    # TODO eventually...
    increase_cursor(ImportJobId.ORCID_IMPORT_JOB)


async def dblp_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run dblp job with {n_batches} and {keywords} and {cursor}")
    page = cursor["batch_id"]
    page_size = cursor["batch_size"]
    for i in range(n_batches):
        works = await dblp_service.fetch_works(keywords, page, page_size)
        authors = await dblp_service.fetch_authors_for_works(works)
        researchers = dblp_dataprocess_service.restructure_authors(authors)
        async with lock:
            await researchers_service.upsert_many_dblp(researchers)
        works = dblp_dataprocess_service.restructure_works(works, researchers)
        # TODO do cleansing and calculate SNM key here
        async with lock:
            await works_service.insert_and_link(works)
        page = page + 1

    logger.info("DBLP import finished")
    increase_cursor(ImportJobId.DBLP_IMPORT_JOB)


import_job_map = {
    ImportJobId.OPENALEX_IMPORT_JOB: openalex_import_job,
    ImportJobId.ORCID_IMPORT_JOB: orcid_import_job,
    ImportJobId.DBLP_IMPORT_JOB: dblp_import_job
}
