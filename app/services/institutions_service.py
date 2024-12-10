from app.models import Institution


async def upsert_many(institutions: list[Institution]):
    # TODO do find logic here for upsert
    for i, institution in enumerate(institutions):
        found_institution = await Institution.find_one(
            Institution.external_id.openalex == institution.external_id.openalex)
        if found_institution is None:
            await Institution.insert_one(institution)
        else:
            institutions[i] = found_institution


async def find_by_openalex(openalex_id: str):
    return await Institution.find_one(Institution.external_id.openalex == openalex_id)
