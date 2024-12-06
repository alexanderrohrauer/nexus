from app.models import Work


def insert_many(works: list[Work]):
    return Work.insert_many(works)
