import re

from beanie.odm.operators.find.evaluation import RegEx

from app.models import Researcher
from app.utils.api_utils import SearchAndFilterParams


class ResearcherSearchParams(SearchAndFilterParams):
    def get_search_beanie_operator(self):
        return RegEx(Researcher.full_name, re.compile(self.search, flags=re.IGNORECASE))
