from uuid import uuid4

import nltk
import pydash as _

from app.models import Work, Researcher, Institution

w_works = 5
w_researchers = 5
w_institutions = 5

WORKS_LEVENSHTEIN_THRESHOLD = 3
RESEARCHERS_LEVENSHTEIN_THRESHOLD = 3
INSTITUTIONS_LEVENSHTEIN_THRESHOLD = 3


async def deduplicate_works():
    works = None
    skip = 0
    limit = 2
    while works is None or len(works) > 0:
        print(f"Work batch: {skip}")
        works = await Work.find_all(skip=skip, limit=limit).sort(Work.snm_key).to_list()
        if len(works) > 0:
            current_work = works[-1]
            duplication_key = current_work.duplication_key or uuid4()
            for prev_work in reversed(works[:-1]):
                if prev_work.uuid != current_work.uuid:
                    distance = nltk.edit_distance(prev_work.normalized_title, current_work.normalized_title)
                    id_match = prev_work.external_id.matches(current_work.external_id)
                    if distance <= 3 or id_match:
                        print(
                            f"Duplicate work found: {prev_work.title} and {current_work.title} ({prev_work.uuid}, {current_work.uuid}, DOI match: {id_match})")
                        await prev_work.set({Work.duplication_key: duplication_key, Work.marked_for_removal: id_match or prev_work.marked_for_removal})
                        await current_work.set(
                            {Work.duplication_key: duplication_key, Work.marked_for_removal: id_match or current_work.marked_for_removal})

                else:
                    break

            skip = skip + 1 if limit >= w_works else skip
            limit = limit + 1 if limit < w_works else limit


async def deduplicate_researchers():
    researchers = None
    skip = 0
    limit = 2
    while researchers is None or len(researchers) > 0:
        print(f"Researcher batch: {skip}")
        researchers = await Researcher.find_all(skip=skip, limit=limit).sort(
            Researcher.snm_key).to_list()
        if len(researchers) > 0:
            current_researcher = researchers[-1]
            duplication_key = current_researcher.duplication_key or uuid4()
            for prev_researcher in reversed(researchers[:-1]):
                if prev_researcher.uuid != current_researcher.uuid:
                    distance = nltk.edit_distance(prev_researcher.normalized_full_name, current_researcher.normalized_full_name)
                    id_match = prev_researcher.external_id.matches(current_researcher.external_id)
                    distance_match = distance <= RESEARCHERS_LEVENSHTEIN_THRESHOLD
                    if distance_match:
                        prev_works = await Work.find(Work.authors.id == prev_researcher.id).to_list()
                        current_works = await Work.find(Work.authors.id == current_researcher.id).to_list()
                        all_works_dois = [w.external_id.doi for w in prev_works if w.external_id.doi is not None] \
                                         + [w.external_id.doi for w in current_works if w.external_id.doi is not None]
                        duplicates = _.duplicates(all_works_dois)
                        if len(duplicates) > 0:
                            id_match = True
                    if distance_match or id_match:
                        print(
                            f"Duplicate researcher found: {prev_researcher.full_name} and {current_researcher.full_name} ({prev_researcher.uuid}, {current_researcher.uuid})")
                        await prev_researcher.set(
                            {Researcher.duplication_key: duplication_key, Researcher.marked_for_removal: id_match or prev_researcher.marked_for_removal})
                        await current_researcher.set(
                            {Researcher.duplication_key: duplication_key, Researcher.marked_for_removal: id_match or current_researcher.marked_for_removal})
                else:
                    break
            skip = skip + 1 if limit >= w_researchers else skip
            limit = limit + 1 if limit < w_researchers else limit




async def deduplicate_institutions():
    institutions = None
    skip = 0
    limit = 2
    while institutions is None or len(institutions) > 0:
        print(f"Institution batch: {skip}")
        institutions = await Institution.find_all(skip=skip, limit=limit).sort(
            Institution.snm_key).to_list()
        if len(institutions) > 0:
            current_institution = institutions[-1]
            duplication_key = current_institution.duplication_key or uuid4()
            for prev_institution in reversed(institutions[:-1]):
                if prev_institution.uuid != current_institution.uuid:
                    distance = nltk.edit_distance(prev_institution.normalized_name, current_institution.normalized_name)
                    id_match = prev_institution.external_id.matches(current_institution.external_id)
                    attribute_match = (
                            distance <= INSTITUTIONS_LEVENSHTEIN_THRESHOLD and prev_institution.city == current_institution.city and prev_institution.country == current_institution.country)
                    if attribute_match or id_match:
                        print(
                            f"Duplicate institution found: {prev_institution.name} and {current_institution.name} ({prev_institution.uuid}, {current_institution.uuid}, ROR match: {id_match})")
                        await prev_institution.set(
                            {Institution.duplication_key: duplication_key, Institution.marked_for_removal: id_match or prev_institution.marked_for_removal})
                        await current_institution.set(
                            {Institution.duplication_key: duplication_key, Institution.marked_for_removal: id_match or current_institution.marked_for_removal})
                else:
                    break
            skip = skip + 1 if limit >= w_institutions else skip
            limit = limit + 1 if limit < w_institutions else limit
