import re

from app.models import Work, Researcher, Institution


def parse_openalex_id(url: str | None):
    return url.replace("https://openalex.org/", "") if url is not None else None


def parse_doi(url: str | None):
    if url is None:
        return None
    if url.startswith("10"):
        return url.lower()
    return re.search(r"/10.+", url).group()[1:].lower()


def parse_orcid(url: str | None):
    return url.replace("https://orcid.org/", "") if url is not None else None


def parse_ror(url: str | None):
    return url.replace("https://ror.org/", "") if url is not None else None


CONSONANTS_REGEX = re.compile(r"[^ABCDFGHJKLMNPQRSTVWXYZabcdfghjklmnpqrstvwxyz]")


def compute_work_snm_key(work: Work):
    title = re.sub(CONSONANTS_REGEX, "", work.normalized_title)
    return f"{title}{work.publication_year}".lower()


def compute_researcher_snm_key(researcher: Researcher):
    name = re.sub(CONSONANTS_REGEX, "", researcher.normalized_full_name)
    return name


def compute_institution_snm_key(institution: Institution):
    name = re.sub(CONSONANTS_REGEX, "", institution.normalized_name)
    city = re.sub(CONSONANTS_REGEX, "", institution.city) if institution.city is not None else ""
    country = institution.country or ""
    return f"{name}{city}{country}".lower()
