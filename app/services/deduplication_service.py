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


# TODO maybe some day only deduplicate newly added records...
# TODO extract mongo calls to service
# TODO generalize methods
async def deduplicate_works():
    works = None
    skip = 0
    while works is None or len(works) > 0:
        print(f"Work batch: {skip}")
        works = await Work.find_all(skip=skip, limit=w_works).sort(Work.snm_key).to_list()
        for current_work in reversed(works):
            duplication_key = current_work.duplication_key or uuid4()
            for prev_work in works:
                if prev_work.uuid != current_work.uuid:
                    distance = nltk.edit_distance(prev_work.title, current_work.title)
                    doi_match = prev_work.external_id.doi is not None and prev_work.external_id.doi == current_work.external_id.doi
                    if distance <= 3 or doi_match:
                        print(
                            f"Duplicate work found: {prev_work.title} and {current_work.title} ({prev_work.uuid}, {current_work.uuid}, DOI match: {doi_match})")
                        await prev_work.set({Work.duplication_key: duplication_key, Work.marked_for_removal: doi_match})
                        await current_work.set(
                            {Work.duplication_key: duplication_key, Work.marked_for_removal: doi_match})

                else:
                    break
        skip = skip + 1


async def deduplicate_researchers():
    researchers = None
    skip = 0
    while researchers is None or len(researchers) > 0:
        print(f"Researcher batch: {skip}")
        researchers = await Researcher.find_all(skip=skip, limit=w_researchers).sort(
            Researcher.snm_key).to_list()
        for current_researcher in reversed(researchers):
            duplication_key = current_researcher.duplication_key or uuid4()
            for prev_researcher in researchers:
                if prev_researcher.uuid != current_researcher.uuid:
                    distance = nltk.edit_distance(prev_researcher.full_name, current_researcher.full_name)
                    if distance <= RESEARCHERS_LEVENSHTEIN_THRESHOLD:
                        prev_works = await Work.find(Work.authors.id == prev_researcher.id).to_list()
                        current_works = await Work.find(Work.authors.id == current_researcher.id).to_list()
                        all_works_dois = [w.external_id.doi for w in prev_works if w.external_id.doi is not None] \
                                         + [w.external_id.doi for w in current_works if w.external_id.doi is not None]
                        duplicates = _.duplicates(all_works_dois)
                        if len(duplicates) > 0:
                            print(
                                f"Duplicate researcher found: {prev_researcher.full_name} and {current_researcher.full_name} ({prev_researcher.uuid}, {current_researcher.uuid})")
                            # TODO set marked_for_removal
                            await prev_researcher.set({Researcher.duplication_key: duplication_key})
                            await current_researcher.set({Researcher.duplication_key: duplication_key})
                    # TODO we could run here a merge-logic based on orcid some day
                else:
                    break
        skip = skip + 1


async def deduplicate_institutions():
    institutions = None
    skip = 0
    while institutions is None or len(institutions) > 0:
        print(f"Institution batch: {skip}")
        institutions = await Institution.find_all(skip=skip, limit=w_institutions).sort(
            Institution.snm_key).to_list()
        for current_institution in reversed(institutions):
            duplication_key = current_institution.duplication_key or uuid4()
            for prev_institution in institutions:
                if prev_institution.uuid != current_institution.uuid:
                    distance = nltk.edit_distance(prev_institution.name, current_institution.name)
                    ror_match = prev_institution.external_id.ror is not None and prev_institution.external_id.ror == current_institution.external_id.ror
                    attribute_match = (
                            distance <= INSTITUTIONS_LEVENSHTEIN_THRESHOLD and prev_institution.city == current_institution.city and prev_institution.country == current_institution.country)
                    # TODO do levenshtein maybe
                    if attribute_match or ror_match:
                        print(
                            f"Duplicate institution found: {prev_institution.name} and {current_institution.name} ({prev_institution.uuid}, {current_institution.uuid}, ROR match: {ror_match})")
                        await prev_institution.set(
                            {Institution.duplication_key: duplication_key, Institution.marked_for_removal: ror_match})
                        await current_institution.set(
                            {Institution.duplication_key: duplication_key, Institution.marked_for_removal: ror_match})
                else:
                    break
        skip = skip + 1
