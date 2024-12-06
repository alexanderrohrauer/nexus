from app.external_services import openalex_service
from app.scheduled.models import ImportJobId, Cursor
from app.services import openalex_dataprocess_service, works_service
from app.utils.job_utils import increase_cursor


async def openalex_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run openalex job with {n_batches} and {keywords} and {cursor}")
    page = cursor["batch_id"] + 1
    page_size = cursor["batch_size"]
    topic_ids = await openalex_service.fetch_topic_ids(keywords)
    # TODO batch from here, do upsert...
    for i in range(n_batches):
        works = await openalex_service.fetch_works(topic_ids, page, page_size)
        works = openalex_dataprocess_service.restructure_works(works)
        # TODO do cleansing and calculate SNM key here
        await works_service.insert_many(works)

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
