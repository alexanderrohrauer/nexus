from typing_extensions import TypedDict


class Cursor(TypedDict):
    batch_id: int
    batch_size: int


def openalex_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run openalex job with {n_batches} and {keywords}")


def orcid_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run orcid job with {n_batches} and {keywords}")


def dblp_import_job(n_batches: int, keywords: list[str], cursor: Cursor, cron_expr: str):
    print(f"run dblp job with {n_batches} and {keywords}")
