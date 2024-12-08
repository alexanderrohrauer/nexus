import logging
from datetime import date

from app.models import Work, Researcher, Institution
from app.models.institutions import InstitutionExternalId
from app.models.researchers import ResearcherExternalId, Affiliation, AffiliationType
from app.models.works import WorkExternalId, WorkType
from app.utils.text_utils import parse_openalex_id

logger = logging.getLogger("uvicorn.error")


def restructure_works(works: list[dict], authors: list[Researcher]):
    result = []
    for work in works:
        keywords = [kw["display_name"] for kw in work["keywords"]]
        # TODO implement a merger logic
        author_links = []
        for author in work["authorships"]:
            author_id = parse_openalex_id(author["author"]["id"])
            try:
                author_links.append(next(a for a in authors if a.external_id.openalex == author_id).id)
            except StopIteration:
                logger.error(f"Author with id " + author_id + " not found in work " + work["id"])
                continue
        parsed = Work(
            external_id=WorkExternalId(openalex=parse_openalex_id(work["id"])),
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


def restructure_authors(authors: list[dict], institutions: list[Institution]):
    result = []
    affiliations = []
    institution = None
    for author in authors:
        for affiliation in author["affiliations"]:
            institution_id = parse_openalex_id(affiliation["institution"]["id"])
            try:
                institution = next(i for i in institutions if i.external_id.openalex == institution_id)
                i_type = AffiliationType.EDUCATION if institution.type == "Education" else AffiliationType.EMPLOYMENT
                affiliations.append(Affiliation(years=affiliation["years"], type=i_type, institution=institution.id))
            except StopIteration:
                logger.error(f"Institution with id " + institution_id + " not found in author " + author["id"])
                continue
        if len(author["last_known_institutions"]) > 0:
            institution_id = parse_openalex_id(author["last_known_institutions"][0]["id"])
            institution = next(i for i in institutions if i.external_id.openalex == institution_id)
        parsed = Researcher(
            external_id=ResearcherExternalId(openalex=parse_openalex_id(author["id"])),
            full_name=author["display_name"],
            alternative_names=author["display_name_alternatives"],
            affiliations=affiliations,
            institution=institution.id if institution is not None else None,
            topic_keywords=[t["display_name"] for t in author["topics"]],
            openalex_meta=author
        )
        result.append(parsed)
    return result


def restructure_institutions(institutions: list[dict]):
    result = []
    for institution in institutions:
        parsed = Institution(
            external_id=InstitutionExternalId(openalex=parse_openalex_id(institution["id"])),
            name=institution["display_name"],
            acronyms=institution["display_name_acronyms"],
            alternative_names=institution["display_name_alternatives"],
            international_names=institution["international"]["display_name"],
            city=institution["geo"]["city"],
            region=institution["geo"]["region"],
            country=institution["geo"]["country_code"],
            location=(institution["geo"]["longitude"], institution["geo"]["latitude"]) if institution["geo"][
                "longitude"] else None,
            homepage_url=institution["homepage_url"],
            image_url=institution["image_url"],
            # TODO maybe do UUIDs some day:
            parent_institutions_ids=[parse_openalex_id(url) for url in institution["lineage"]],
            # TODO maybe convert to enum one day
            type=institution["type"],
            topic_keywords=[t["display_name"] for t in institution["topics"]],
            openalex_meta=institution
        )
        result.append(parsed)
    return result
