import re

from beanie.odm.operators.find.evaluation import RegEx

from app.models import Work
from app.utils.api_utils import SearchAndFilterParams


class WorkSearchParams(SearchAndFilterParams):
    def get_search_beanie_operator(self):
        return RegEx(Work.title, re.compile(self.search, flags=re.IGNORECASE))
