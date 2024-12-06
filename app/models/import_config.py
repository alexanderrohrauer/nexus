from pydantic import BaseModel, Field


class ImportCursor(BaseModel):
    batch_id: int = Field(gt=-1, default=0)
    batch_size: int = Field(gt=-1, lt=501, default=20)


class ImportArguments(BaseModel):
    keywords: list[str]
    n_batches: int = Field(gt=0, lt=501)
    cursor: ImportCursor = Field(default_factory=ImportCursor)
