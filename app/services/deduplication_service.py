from uuid import uuid4

import pydash as _

from app.models import Work, Researcher, Institution

w_works = 4
w_researchers = 4
w_institutions = 4


# TODO extract mongo calls to service
# TODO generalize methods
async def deduplicate_works():
    works = None
    page = 0
    while works is None or len(works) > 0:
        works = await Work.find_all(skip=page * w_works, limit=w_works).sort(Work.snm_key).to_list()
        for current_work in reversed(works):
            for prev_work in works:
                if prev_work.uuid != current_work.uuid:
                    # TODO do levenshtein maybe
                    if prev_work.title == current_work.title and prev_work.publication_year == current_work.publication_year:
                        duplication_key = uuid4()
                        print(
                            f"Duplicate work found: {prev_work.title} and {current_work.title} ({prev_work.uuid}, {current_work.uuid})")
                        await prev_work.set({Work.duplication_key: duplication_key})
                        await current_work.set({Work.duplication_key: duplication_key})
                else:
                    break
        page = page + 1


async def deduplicate_researchers():
    researchers = None
    page = 0
    while researchers is None or len(researchers) > 0:
        researchers = await Researcher.find_all(skip=page * w_researchers, limit=w_researchers).sort(
            Researcher.snm_key).to_list()
        for current_researcher in reversed(researchers):
            for prev_researcher in researchers:
                if prev_researcher.uuid != current_researcher.uuid:
                    # TODO do levenshtein maybe, works search
                    if prev_researcher.full_name == current_researcher.full_name:
                        prev_works = await Work.find(Work.authors.id == prev_researcher.id).to_list()
                        current_works = await Work.find(Work.authors.id == current_researcher.id).to_list()
                        all_works_dois = [w.external_id.doi for w in prev_works if w.external_id.doi is not None] \
                                         + [w.external_id.doi for w in current_works if w.external_id.doi is not None]
                        duplicates = _.duplicates(all_works_dois)
                        if len(duplicates) > 0:
                            duplication_key = uuid4()
                            print(
                                f"Duplicate researcher found: {prev_researcher.full_name} and {current_researcher.full_name} ({prev_researcher.uuid}, {current_researcher.uuid})")
                            await prev_researcher.set({Researcher.duplication_key: duplication_key})
                            await current_researcher.set({Researcher.duplication_key: duplication_key})
                else:
                    break
        page = page + 1


async def deduplicate_institutions():
    institutions = None
    page = 0
    while institutions is None or len(institutions) > 0:
        institutions = await Institution.find_all(skip=page * w_institutions, limit=w_institutions).sort(
            Institution.snm_key).to_list()
        for current_institution in reversed(institutions):
            for prev_institution in institutions:
                if prev_institution.uuid != current_institution.uuid:
                    # TODO do levenshtein maybe, works search
                    if prev_institution.name == current_institution.name and prev_institution.city == current_institution.city and prev_institution.country == current_institution.country:
                        duplication_key = uuid4()
                        print(
                            f"Duplicate institution found: {prev_institution.name} and {current_institution.name} ({prev_institution.uuid}, {current_institution.uuid})")
                        await prev_institution.set({Institution.duplication_key: duplication_key})
                        await current_institution.set({Institution.duplication_key: duplication_key})
                else:
                    break
        page = page + 1
