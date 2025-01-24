import html
import logging
from datetime import date
from string import digits

from app.models import Work, Researcher, Institution
from app.models.institutions import InstitutionExternalId
from app.models.researchers import ResearcherExternalId, Affiliation, AffiliationType
from app.models.works import WorkExternalId, WorkType
from app.utils.text_utils import parse_openalex_id, parse_doi, parse_orcid, parse_ror, compute_work_snm_key, \
    compute_researcher_snm_key, compute_institution_snm_key

logger = logging.getLogger("uvicorn.error")


def restructure_works(works: list[dict], authors: list[Researcher]):
    result = []
    for work in works:
        if work["title"] is not None:
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
            ids = work["ids"].copy()
            ids["openalex"] = parse_openalex_id(ids["openalex"])
            ids["doi"] = parse_doi(ids["doi"]) if "doi" in ids else None
            parsed = Work(
                external_id=WorkExternalId(**ids),
                title=html.unescape(work["title"].strip()),
                type=WorkType(openalex=work["type"]),
                publication_year=int(work["publication_year"]),
                publication_date=date.fromisoformat(work["publication_date"]),
                keywords=keywords,
                authors=author_links,
                language=work["language"],
                open_access=work["open_access"]["is_oa"],
                openalex_meta=work
            )
            parsed.snm_key = compute_work_snm_key(parsed)
            result.append(parsed)
    return result


def restructure_authors(authors: list[dict], institutions: list[Institution]):
    result = []
    for author in authors:
        institution = None
        affiliations = []
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
        ids = author["ids"].copy()
        ids["openalex"] = parse_openalex_id(ids["openalex"])
        ids["orcid"] = parse_orcid(ids["orcid"]) if "orcid" in ids else None
        parsed = Researcher(
            external_id=ResearcherExternalId(**ids),
            full_name=author["display_name"].strip().translate(str.maketrans('', '', digits)),
            alternative_names=author["display_name_alternatives"],
            affiliations=affiliations,
            institution=institution.id if institution is not None else None,
            topic_keywords=[t["display_name"] for t in author["topics"]],
            openalex_meta=author
        )
        parsed.snm_key = compute_researcher_snm_key(parsed)
        result.append(parsed)
    return result


def restructure_institutions(institutions: list[dict]):
    result = []
    for institution in institutions:
        ids = institution["ids"].copy()
        ids["openalex"] = parse_openalex_id(ids["openalex"])
        ids["ror"] = parse_ror(ids["ror"]) if "ror" in ids else None
        parsed = Institution(
            external_id=InstitutionExternalId(**ids),
            name=institution["display_name"].strip(),
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
        parsed.snm_key = compute_institution_snm_key(parsed)
        result.append(parsed)
    return result
