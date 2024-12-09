import logging

import pydash as _
from aiohttp_client_cache import CachedSession, SQLiteBackend

from app.utils.text_utils import parse_openalex_id

OPENALEX_URL = "https://api.openalex.org"
OPENALEX_AUTHOR_BATCH_SIZE = 20
OPENALEX_INSTITUTION_BATCH_SIZE = 20

logger = logging.getLogger("uvicorn.error")


# TODO maybe use https://pypi.org/project/cacheproxy/
# TODO config (1day * 7)
class OpenAlexSession(CachedSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, headers={"User-Agent": "mailto:k12105578@students.jku.at"},
                         cache=SQLiteBackend('openalex_cache', expire_after=60 * 60 * 24 * 7))


async def fetch_topic_ids(keywords: list[str]):
    result = []
    for keyword in keywords:
        params = {"filter": f"default.search:{keyword}", "per-page": 1}
        async with OpenAlexSession() as session:
            logging.debug("Fetching topics...")
            response = await session.get(f"{OPENALEX_URL}/topics", params=params)
            body = await response.json()
            topic = body["results"][0]
            logger.info(f"Adding topic {topic['display_name']}")
            result.append(parse_openalex_id(topic["id"]))
    return result


async def fetch_works(topic_ids: list[str], page: int, page_size: int):
    topic_expr = "|".join(topic_ids)
    params = {"filter": f"topics.id:{topic_expr}", "page": page, "per-page": page_size,
              "sort": "publication_year:desc"}
    async with OpenAlexSession() as session:
        response = await session.get(f"{OPENALEX_URL}/works", params=params)
        logging.debug("Fetching works...")
        body = await response.json()
        result = body["results"]
    return result


async def fetch_authors_for_works(works: list[dict]) -> list[dict]:
    authors = []
    author_ids = _.uniq(_.flatten(
        map(lambda w: [parse_openalex_id(a["author"]["id"]) for a in w["authorships"]],
            works)))
    author_id_chunks = _.chunk(author_ids, OPENALEX_AUTHOR_BATCH_SIZE)
    for chunk in author_id_chunks:
        chunk_expr = "|".join(chunk)
        params = {"filter": f"ids.openalex:{chunk_expr}", "per-page": OPENALEX_AUTHOR_BATCH_SIZE}
        async with OpenAlexSession() as session:
            response = await session.get(f"{OPENALEX_URL}/authors", params=params)
            logging.debug("Fetching authors...")
            body = await response.json()
        authors = authors + body["results"]
    return authors


async def fetch_institutions_for_authors(authors: list[dict]) -> list[dict]:
    institutions = []
    institution_ids = _.uniq(_.flatten(
        map(lambda a: [parse_openalex_id(a["institution"]["id"]) for a in a["affiliations"]],
            authors)))
    last_institution_authors = filter(lambda a: len(a["last_known_institutions"]) > 0, authors)
    institution_ids = institution_ids + [a["last_known_institutions"][0]["id"] for a in last_institution_authors]
    institution_id_chunks = _.chunk(institution_ids, OPENALEX_INSTITUTION_BATCH_SIZE)
    for chunk in institution_id_chunks:
        chunk_expr = "|".join(chunk)
        params = {"filter": f"ids.openalex:{chunk_expr}", "per-page": OPENALEX_AUTHOR_BATCH_SIZE}
        async with OpenAlexSession() as session:
            response = await session.get(f"{OPENALEX_URL}/institutions", params=params)
            logging.debug("Fetching institution...")
            body = await response.json()
        institutions = institutions + body["results"]
    return institutions
