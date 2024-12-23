import logging

import pydash as _
from aiohttp_client_cache import CachedSession, SQLiteBackend

from evaluation.test_data import TestDataInjector

DBLP_URL = "https://dblp.org"

logger = logging.getLogger("uvicorn.error")

works_test_data = TestDataInjector()
authors_test_data = TestDataInjector()


# TODO config (1day * 7)
class DBLPSession(CachedSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, headers={"User-Agent": "mailto:k12105578@students.jku.at"},
                         cache=SQLiteBackend('dblp_cache', expire_after=-1))


async def fetch_works(keywords: list[str], page: int, page_size: int):
    result = []
    for keyword in keywords:
        params = {"q": keyword, "f": page * page_size, "h": page_size,
                  "format": "json"}
        async with DBLPSession() as session:
            response = await session.get(f"{DBLP_URL}/search/publ/api", params=params)
            logger.debug(f"Fetching DBLP works({response.url})...")
            body = await response.json()
            hits = body["result"]["hits"]["hit"] if "hit" in body["result"]["hits"] else []
            # TODO extract
            works_test_data.inject(page, "dblp_works.json", hits)
            result = result + hits

    return result


async def fetch_authors_for_works(works: list[dict], batch_id: int) -> list[dict]:
    flat = list(filter(lambda val: isinstance(val, dict), _.flatten(
        map(lambda w: [a for a in w["info"]["authors"]["author"]] if "authors" in w["info"] else [],
            works))))
    # TODO extract
    authors_test_data.inject(batch_id, "dblp_authors.json", flat)
    return flat
