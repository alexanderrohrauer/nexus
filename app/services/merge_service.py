import logging

from app.models import Work, Researcher, Institution, Affiliation

logger = logging.getLogger("uvicorn.error")


async def merge_institutions(i1: Institution, i2: Institution):
    logger.info(f"Deduplicate institutions '{i1.name}' and '{i2.name}'")
    external_id = i2.external_id.model_copy(update=i1.external_id.model_dump(exclude_none=True))
    i1 = i2.model_copy(
        update=i1.model_dump(exclude_none=True))
    i1.external_id = external_id
    i2_affiliations = await Affiliation.find(Affiliation.institution.id == i2.id, fetch_links=True, nesting_depth=1).to_list()
    for affiliation in i2_affiliations:
        affiliation.institution = i1
        await affiliation.save()
    i2_researchers = await Researcher.find(Researcher.institution.id == i2.id).to_list()
    for researcher in i2_researchers:
        researcher.institution = i1
        await researcher.save()
    i1.marked_for_removal = False
    await i2.set({Institution.marked_for_removal: True})
    await i1.save()
    return i1


async def merge_researchers(r1: Researcher, r2: Researcher) -> Researcher:
    logger.info(f"Deduplicate researchers '{r1.full_name}' and '{r2.full_name}'")
    external_id = r2.external_id.model_copy(update=r1.external_id.model_dump(exclude_none=True))
    r1 = r2.model_copy(
        update=r1.model_dump(exclude_none=True))
    r1.external_id = external_id
    # TODO some researchers do not have affiliations after deduplication
    r1.affiliations = r1.affiliations or r2.affiliations
    r1.institution = r1.institution or r2.institution
    assigned_works = await Work.find(Work.authors.id == r2.id).to_list()
    for work in assigned_works:
        work.replace_author(r2, r1)
        await work.save()
    r1.marked_for_removal = False
    await r2.set({Researcher.marked_for_removal: True})
    await r1.save()
    return r1


async def merge_works(w1: Work, w2: Work) -> Work:
    logger.info(f"Deduplicate works '{w1.title}' and '{w2.title}'")
    external_id = w2.external_id.model_copy(update=w1.external_id.model_dump(exclude_none=True))
    w_type = w2.type.model_copy(update=w1.type.model_dump(exclude_none=True))
    w1 = w2.model_copy(update=w1.model_dump(exclude_none=True))
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
    await w2.set({Work.marked_for_removal: True})
    await w1.save()
    return w1
