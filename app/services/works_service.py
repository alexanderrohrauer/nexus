from app.models import Work


async def insert_many(works: list[Work]):
    for work in works:
        await Work.insert_one(work)

