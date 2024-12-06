from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass

from app.models.import_config import ImportCursor
from app.scheduled.models import ImportJobId


@dataclass
class ImportJob:
    job_id: ImportJobId
    cursor: ImportCursor
    enabled: bool


@dataclass
class ImportTask:
    cron_expr: str
    n_batches: int
    keywords: list[str]
    jobs: list[ImportJob]


class UpdateImportTaskRequest(BaseModel):
    cron_expr: str
    n_batches: int = Field(gt=0, lt=501)
    keywords: list[str]
    jobs: list[ImportJobId]


class CreateImportTaskRequest(BaseModel):
    cron_expr: str
    n_batches: int = Field(gt=0, lt=501)
    keywords: list[str]


class ResetCursorsRequest(BaseModel):
    jobs: list[ImportJobId]
