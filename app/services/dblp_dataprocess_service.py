import html
import logging
from string import digits

from app.models import Work, Researcher
from app.models.researchers import ResearcherExternalId
from app.models.works import WorkExternalId, WorkType
from app.utils.text_utils import parse_doi, compute_work_snm_key, compute_researcher_snm_key

logger = logging.getLogger("uvicorn.error")


def restructure_works(works: list[dict], authors: list[Researcher]):
    result = []
    for work in works:
        author_links = []
        info = work["info"]
        filtered_authors = filter(lambda val: isinstance(val, dict),
                                  info["authors"]["author"]) if "authors" in info else []
        for author in filtered_authors:
            author_id = author["@pid"]
            try:
                author_links.append(next(a for a in authors if a.external_id.dblp == author_id).id)
            except StopIteration:
                logger.error(f"Author with id " + author_id + " not found in work " + work["@id"])
                continue
        parsed = Work(
            external_id=WorkExternalId(dblp=work["@id"], doi=parse_doi(info["doi"] if "doi" in info else None)),
            title=html.unescape(info["title"].strip()),
            type=WorkType(dblp=info["type"]),
            publication_year=int(info["year"]),
            authors=author_links if len(author_links) > 0 else None,
            open_access=info["access"] == "open" if "access" in info else None,
            dblp_meta=work
        )
        parsed.snm_key = compute_work_snm_key(parsed)
        result.append(parsed)
    return result


def restructure_authors(authors: list[dict]):
    result = []
    for author in authors:
        parsed = Researcher(
            external_id=ResearcherExternalId(dblp=author["@pid"]),
            full_name=author["text"].strip().translate(str.maketrans('', '', digits)),
            dblp_meta=author
        )
        parsed.snm_key = compute_researcher_snm_key(parsed)
        result.append(parsed)
    return result
