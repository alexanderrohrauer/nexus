import aiohttp

from app.utils.text_utils import parse_openalex_id

OPENALEX_URL = "https://api.openalex.org"


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
