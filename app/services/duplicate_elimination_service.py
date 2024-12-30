import logging
from typing import Optional
from uuid import UUID

from beanie.odm.operators.find.comparison import In
from pydantic import BaseModel, Field

from app.models import Work, Researcher, Institution, Affiliation
from app.services import merge_service

logger = logging.getLogger("uvicorn.error")


class FindKeysResult(BaseModel):
    id: Optional[UUID] = Field(None, alias="_id")
    count: int


# TODO Implement filter for specific duplication key
async def eliminate_work_duplicates(filter=None):
    logger.info("Work duplicate elimination started...")
    keys = await Work.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            works = await Work.find(Work.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = works[0]
            should_clear_key = True
            for i in range(1, len(works)):
                if works[i].marked_for_removal:
                    merged = await merge_service.merge_works(merged, works[i])
                else:
                    should_clear_key = False
            if should_clear_key:
                await merged.set({Work.duplication_key: None})
    await Work.find(Work.marked_for_removal == True).delete()
    logger.info("Work duplicate elimination finished...")


async def eliminate_researcher_duplicates(filter=None):
    logger.info("Researcher duplicate elimination started...")
    keys = await Researcher.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            researchers = await Researcher.find(Researcher.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = researchers[0]
            should_clear_key = True
            for i in range(1, len(researchers)):
                if researchers[i].marked_for_removal:
                    merged = await merge_service.merge_researchers(merged, researchers[i])
                else:
                    should_clear_key = False
            if should_clear_key:
                await merged.set({Researcher.duplication_key: None})
    researchers_to_delete = await Researcher.find(Researcher.marked_for_removal == True).to_list()
    for researcher in researchers_to_delete:
        await researcher.delete()
        if researcher.affiliations is not None:
            await Affiliation.find(In(Affiliation.id, list(map(lambda a: a.ref.id, researcher.affiliations)))).delete()
    logger.info("Researcher duplicate elimination finished...")


async def eliminate_institutions_duplicates(filter=None):
    logger.info("Institution duplicate elimination started...")
    keys = await Institution.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            institutions = await Institution.find(Institution.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = institutions[0]
            should_clear_key = True
            for i in range(1, len(institutions)):
                if institutions[i].marked_for_removal:
                    merged = await merge_service.merge_institutions(merged, institutions[i])
                else:
                    should_clear_key = False
            if should_clear_key:
                await merged.set({Institution.duplication_key: None})
    await Institution.find(Institution.marked_for_removal == True).delete()
    logger.info("Institution duplicate elimination finished...")
