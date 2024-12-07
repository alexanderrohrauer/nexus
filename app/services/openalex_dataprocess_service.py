from datetime import date

from app.models import Work, Researcher
from app.models.researchers import ResearcherExternalId
from app.models.works import ExternalId, WorkType
from app.utils.text_utils import parse_openalex_id


def restructure_works(works: list[dict], authors: list[Researcher]):
    result = []
    for work in works:
        keywords = [kw["display_name"] for kw in work["keywords"]]
        # TODO implement a merger logic
        author_links = []
        for author in work["authorships"]:
            author_id = parse_openalex_id(author["author"]["id"])
            author_links.append(next(a for a in authors if a.external_id.openalex == author_id).id)
        parsed = Work(
            external_id=ExternalId(openalex=parse_openalex_id(work["id"])),
            title=work["title"],
            type=WorkType(openalex=work["type"]),
            publication_year=int(work["publication_year"]),
            publication_date=date.fromisoformat(work["publication_date"]),
            keywords=keywords,
            authors=author_links,
            language=work["language"],
            open_access=work["open_access"]["is_oa"],
            openalex_meta=work
        )
        result.append(parsed)
    return result


def restructure_authors(authors: list[dict]):
    result = []
    for author in authors:
        parsed = Researcher(
            external_id=ResearcherExternalId(openalex=parse_openalex_id(author["id"])),
            full_name=author["display_name"],
            alternative_names=author["display_name_alternatives"],
            # TODO do affiliation
            affiliations=[],
            # TODO institution: Optional[Link[Institution]] = None
            topic_keywords=[t["display_name"] for t in author["topics"]],
            openalex_meta=author
        )
        result.append(parsed)
    return result
