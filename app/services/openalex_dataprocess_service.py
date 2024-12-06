from datetime import date

from app.models import Work
from app.models.works import ExternalId, WorkType
from app.utils.text_utils import parse_openalex_id


def restructure_works(works: list[dict]):
    result = []
    for work in works:
        keywords = [kw["display_name"] for kw in work["keywords"]]
        parsed = Work(
            external_id=ExternalId(openalex=parse_openalex_id(work["id"])),
            title=work["title"],
            type=WorkType(openalex=work["type"]),
            publication_year=int(work["publication_year"]),
            publication_date=date.fromisoformat(work["publication_date"]),
            keywords=keywords,
            # TODO do authors...
            authors=[],
            language=work["language"],
            open_access=work["open_access"]["is_oa"],
            openalex_meta=work
        )
        result.append(parsed)
    return result
