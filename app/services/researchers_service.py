from app.models import Researcher


async def upsert_many(researchers: list[Researcher]):
    # TODO do find logic here for upsert
    for i, researcher in enumerate(researchers):
        found_researcher = await Researcher.find_one(Researcher.external_id.openalex == researcher.external_id.openalex)
        if found_researcher is None:
            await Researcher.insert_one(researcher)
        else:
            researchers[i] = found_researcher

