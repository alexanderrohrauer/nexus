import logging

from app.models import Work, Researcher, Institution

logger = logging.getLogger("uvicorn.error")


async def merge_institutions(i1: Institution, i2: Institution):
    logger.info(f"Deduplicate institutions '{i1.name}' and '{i2.name}'")
    external_id = i1.external_id.model_copy(update=i2.external_id.model_dump(exclude_none=True))
    r1 = i1.model_copy(
        update=i1.model_dump(exclude_none=True, exclude={"id", "external_id"}))
    r1.external_id = external_id
    r2_researchers = await Researcher.find(Researcher.affiliations.institution.id == i2.id).to_list()
    for researcher in r2_researchers:
        researcher.replace_affiliation(i2, i1)
        await researcher.save()
    r2_researchers = await Researcher.find(Researcher.institution.id == i2.id).to_list()
    for researcher in r2_researchers:
        researcher.institution = i1
        await researcher.save()
    i1.marked_for_removal = False
    i1.duplication_key = None
    await i1.save()
    await i2.delete()
    return i1


async def merge_researchers(r1: Researcher, r2: Researcher) -> Researcher:
    logger.info(f"Deduplicate researchers '{r1.full_name}' and '{r2.full_name}'")
    external_id = r1.external_id.model_copy(update=r2.external_id.model_dump(exclude_none=True))
    r1 = r1.model_copy(
        update=r2.model_dump(exclude_none=True, exclude={"id", "external_id", "affiliations", "institution"}))
    r1.external_id = external_id
    # TODO dblp does not return institutions so we do not need to merge them here but maybe a different datasource returns it...
    r1.affiliations = r1.affiliations or r2.affiliations
    r1.institution = r1.institution or r2.institution
    assigned_works = await Work.find(Work.authors.id == r2.id).to_list()
    for work in assigned_works:
        work.replace_author(r2, r1)
        await work.save()
    r1.marked_for_removal = False
    r1.duplication_key = None
    await r1.save()
    await r2.delete()
    return r1


async def merge_works(w1: Work, w2: Work) -> Work:
    logger.info(f"Deduplicate works '{w1.title}' and '{w2.title}'")
    external_id = w1.external_id.model_copy(update=w2.external_id.model_dump(exclude_none=True))
    w_type = w1.type.model_copy(update=w2.type.model_dump(exclude_none=True))
    w1 = w1.model_copy(update=w2.model_dump(exclude_none=True, exclude={"id", "external_id", "type", "authors"}))
    w1.external_id = external_id
    w1.type = w_type
    authors = []
    await w1.fetch_link(Work.authors)
    await w2.fetch_link(Work.authors)
    for i in range(len(w1.authors)):
        author = await merge_researchers(w1.authors[i], w2.authors[i])
        authors.append(author)
    w1.authors = authors
    w1.marked_for_removal = False
    w1.duplication_key = None
    await w1.save()
    await w2.delete()
    return w1
