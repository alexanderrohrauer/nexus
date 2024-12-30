import json
import re
from abc import abstractmethod
from datetime import datetime
from typing import Optional, Any
from uuid import UUID

import pymongo
from pydantic import BaseModel


def transform_filter_field(field: dict):
    if field["field"].endswith("imported_at") or field["field"].endswith("publication_date"):
        return datetime.fromisoformat(field["value"])
    if field["operator"] == "$regex":
        return re.compile(field["value"], flags=re.IGNORECASE)
    if field["field"].endswith("uuid"):
        return list(map(lambda option: UUID(option["value"]), field["value"]))
    return field["value"]


class SearchAndFilterParams:
    def __init__(self,
                 search: Optional[str] = None,
                 q: str = "[]",
                 sort: Optional[str] = None,
                 limit: int = 20,
                 offset: int = 0):
        self.q = q
        self.sort = sort
        self.search = search
        self.limit = limit
        self.offset = offset

    @abstractmethod
    def get_search_beanie_operator(self):
        raise NotImplemented("get_search_beanie_operator() not implemented")

    def get_filter(self):
        query = json.loads(self.q)
        boolean_builder = [
            {criterion["field"]: {criterion["operator"]: transform_filter_field(criterion)}}
            for criterion in query
        ]
        if self.search is not None:
            boolean_builder.append(self.get_search_beanie_operator())
        return {
            "$and": boolean_builder
        } if len(boolean_builder) > 0 else {}

    def get_sort(self):
        result = []
        if self.sort is not None:
            for sort in self.sort.split(","):
                sort = sort.strip()
                if sort != "":
                    if sort.startswith("+") or sort.startswith("-"):
                        prefix, field = sort[0], sort[1:]
                        result.append((field, pymongo.ASCENDING if prefix == "+" else pymongo.DESCENDING))
                    else:
                        result.append((sort, pymongo.ASCENDING))
        return result


class ResponseModel(BaseModel):
    @classmethod
    def from_model(cls, model: Any):
        raise NotImplemented()

    @classmethod
    def from_model_list(cls, models: list):
        return [cls.from_model(m) for m in models]
