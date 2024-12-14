import logging
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models import Work, Researcher, Institution
from app.services import merge_service

logger = logging.getLogger("uvicorn.error")


class FindKeysResult(BaseModel):
    id: Optional[UUID] = Field(None, alias="_id")
    count: int


# TODO Implement filter for specific duplication key
async def eliminate_work_duplicates(filter=None, delete_marked=False):
    logger.info("Work duplicate elimination started...")
    keys = await Work.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            works = await Work.find(Work.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = works[0]
            for i in range(1, len(works)):
                if delete_marked or works[i].marked_for_removal:
                    merged = await merge_service.merge_works(merged, works[i])
    logger.info("Work duplicate elimination finished...")


async def eliminate_researcher_duplicates(filter=None, delete_marked=False):
    logger.info("Researcher duplicate elimination started...")
    keys = await Researcher.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            researchers = await Researcher.find(Researcher.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = researchers[0]
            for i in range(1, len(researchers)):
                if delete_marked or researchers[i].marked_for_removal:
                    merged = await merge_service.merge_researchers(merged, researchers[i])
    logger.info("Researcher duplicate elimination finished...")


async def eliminate_institutions_duplicates(filter=None, delete_marked=False):
    logger.info("Institution duplicate elimination started...")
    keys = await Institution.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            institutions = await Institution.find(Institution.duplication_key == key).to_list()
            # TODO maybe get latest record here?
            merged = institutions[0]
            for i in range(1, len(institutions)):
                if delete_marked or institutions[i].marked_for_removal:
                    merged = await merge_service.merge_institutions(merged, institutions[i])
    logger.info("Institution duplicate elimination finished...")
