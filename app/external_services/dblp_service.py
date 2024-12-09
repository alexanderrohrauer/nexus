import logging

import pydash as _
from aiohttp_client_cache import CachedSession, SQLiteBackend

DBLP_URL = "https://dblp.org"

logger = logging.getLogger("uvicorn.error")


# TODO config (1day * 7)
class DBLPSession(CachedSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, headers={"User-Agent": "mailto:k12105578@students.jku.at"},
                         cache=SQLiteBackend('dblp_cache', expire_after=60 * 60 * 24 * 7))


async def fetch_works(keywords: list[str], page: int, page_size: int):
    result = []
    for keyword in keywords:
        params = {"q": keyword, "f": page * page_size, "h": page_size,
                  "format": "json"}
        async with DBLPSession() as session:
            response = await session.get(f"{DBLP_URL}/search/publ/api", params=params)
            logging.debug("Fetching DBLP works...")
            body = await response.json()
            result = result + body["result"]["hits"]["hit"]

    return result


async def fetch_authors_for_works(works: list[dict]) -> list[dict]:
    flat = filter(lambda val: isinstance(val, dict), _.flatten(
        map(lambda w: [a for a in w["info"]["authors"]["author"]] if "authors" in w["info"] else [],
            works)))
    return _.uniq_by(flat, lambda val: val["@pid"])
