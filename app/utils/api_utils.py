import json
from typing import Optional

import pymongo


class SearchAndFilterParams:
    def __init__(self, search: Optional[str] = None, q: Optional[str] = None, sort: Optional[str] = None):
        self.q = q
        self.sort = sort
        self.search = search

    def get_filter(self):
        return json.loads(self.q) if self.q is not None else []

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
