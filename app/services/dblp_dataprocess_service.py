import logging

from app.models import Work, Researcher
from app.models.researchers import ResearcherExternalId
from app.models.works import WorkExternalId, WorkType

logger = logging.getLogger("uvicorn.error")


def restructure_works(works: list[dict], authors: list[Researcher]):
    result = []
    for work in works:
        # TODO implement a merger logic
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
            # TODO add doi here
            external_id=WorkExternalId(dblp=work["@id"]),
            title=info["title"],
            type=WorkType(dblp=info["type"]),
            publication_year=int(info["year"]),
            authors=author_links if len(author_links) > 0 else None,
            open_access=info["access"] == "open" if "access" in info else None,
            dblp_meta=work
        )
        result.append(parsed)
    return result


def restructure_authors(authors: list[dict]):
    result = []
    for author in authors:
        parsed = Researcher(
            external_id=ResearcherExternalId(dblp=author["@pid"]),
            full_name=author["text"],
            dblp_meta=author
        )
        result.append(parsed)
    return result
