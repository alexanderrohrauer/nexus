from app.models import Researcher


async def insert_many(researchers: list[Researcher]):
    for researcher in researchers:
        await Researcher.insert_one(researcher)
