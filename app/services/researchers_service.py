from app.models import Researcher


async def upsert_many_openalex(researchers: list[Researcher]):
    # TODO do find logic here for upsert (via openalexid or doi - Record linking)
    # TODO maybe extract find to fetch process
    for i, researcher in enumerate(researchers):
        found_researcher = await Researcher.find_one(Researcher.external_id.openalex == researcher.external_id.openalex)
        if found_researcher is None:
            await Researcher.insert_one(researcher)
        else:
            researchers[i] = found_researcher


async def upsert_many_dblp(researchers: list[Researcher]):
    # TODO do find logic here for upsert
    for i, researcher in enumerate(researchers):
        found_researcher = await Researcher.find_one(Researcher.external_id.dblp == researcher.external_id.dblp)
        if found_researcher is None:
            await Researcher.insert_one(researcher)
        else:
            researchers[i] = found_researcher
