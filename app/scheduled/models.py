from enum import Enum

from typing_extensions import TypedDict


class Cursor(TypedDict):
    batch_id: int
    batch_size: int


class ImportJobId(Enum):
    OPENALEX_IMPORT_JOB = "openalex_import_job"
    ORCID_IMPORT_JOB = "orcid_import_job"
    DBLP_IMPORT_JOB = "dblp_import_job"

