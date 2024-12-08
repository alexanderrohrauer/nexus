import logging

import aiohttp
import pydash as _

from app.utils.text_utils import parse_openalex_id

OPENALEX_URL = "https://api.openalex.org"
OPENALEX_AUTHOR_BATCH_SIZE = 20
OPENALEX_INSTITUTION_BATCH_SIZE = 20

logger = logging.getLogger("uvicorn.error")


# TODO maybe use https://pypi.org/project/cacheproxy/

async def fetch_topic_ids(keywords: list[str]):
    result = []
    for keyword in keywords:
        params = {"filter": f"default.search:{keyword}", "per-page": 1}
        session: aiohttp.ClientSession
        async with aiohttp.ClientSession() as session:
            logging.debug("Fetching topics...")
            async with session.get(f"{OPENALEX_URL}/topics", params=params) as response:
                result.append(parse_openalex_id((await response.json())["results"][0]["id"]))
    return result


# TODO add user agent everywhere
async def fetch_works(topic_ids: list[str], page: int, page_size: int):
    topic_expr = "|".join(topic_ids)
    params = {"filter": f"topics.id:{topic_expr}", "page": page, "per-page": page_size,
              "sort": "publication_year:desc"}
    session: aiohttp.ClientSession
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{OPENALEX_URL}/works", params=params) as response:
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
        session: aiohttp.ClientSession
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{OPENALEX_URL}/authors", params=params) as response:
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
        session: aiohttp.ClientSession
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{OPENALEX_URL}/institutions", params=params) as response:
                logging.debug("Fetching institution...")
                body = await response.json()
        institutions = institutions + body["results"]
    return institutions
