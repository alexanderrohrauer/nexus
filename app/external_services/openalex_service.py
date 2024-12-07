

import aiohttp
import pydash as _

from app.utils.text_utils import parse_openalex_id

OPENALEX_URL = "https://api.openalex.org"
OPENALEX_AUTHOR_BATCH_SIZE = 20


# TODO maybe use https://pypi.org/project/cacheproxy/

async def fetch_topic_ids(keywords: list[str]):
    result = []
    for keyword in keywords:
        params = {"filter": f"default.search:{keyword}", "per-page": 1}
        session: aiohttp.ClientSession
        async with aiohttp.ClientSession() as session:
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
                body = await response.json()
        authors = authors + body["results"]
    return authors

