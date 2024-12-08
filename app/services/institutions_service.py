from app.models import Institution


async def upsert_many(institutions: list[Institution]):
    # TODO do find logic here for upsert
    for institution in institutions:
        found_institution = await Institution.find_one(
            Institution.external_id.openalex == institution.external_id.openalex)
        if found_institution is None:
            await Institution.insert_one(institution)
