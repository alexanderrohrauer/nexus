import re

from beanie.odm.operators.find.evaluation import RegEx

from app.models import Institution
from app.utils.api_utils import SearchAndFilterParams


class InstitutionSearchParams(SearchAndFilterParams):
    def get_search_beanie_operator(self):
        # TODO implement proper search
        return RegEx(Institution.name, re.compile(self.search, flags=re.IGNORECASE))
