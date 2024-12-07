from app.models import Researcher


async def upsert_many(researchers: list[Researcher]):
    # TODO do find logic here for upsert
    for researcher in researchers:
        await Researcher.insert_one(researcher)

