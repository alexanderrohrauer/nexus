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


async def eliminate_work_duplicates():
    logger.info("Work duplicate elimination started...")
    keys = await Work.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            works = await Work.find(Work.duplication_key == key).to_list()
            try:
                merged = next(filter(lambda w: not w.marked_for_removal, works))
            except StopIteration:
                merged = sorted(works, key=lambda w: w.imported_at)[0]
            should_clear_key = True
            for i in range(len(works)):
                if works[i].uuid != merged.uuid:
                    if works[i].marked_for_removal:
                        merged = await merge_service.merge_works(merged, works[i])
                    else:
                        should_clear_key = False
            if should_clear_key:
                await merged.set({Work.duplication_key: None})
    await Work.find(Work.marked_for_removal == True).delete()
    logger.info("Work duplicate elimination finished...")


async def eliminate_researcher_duplicates():
    logger.info("Researcher duplicate elimination started...")
    keys = await Researcher.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            researchers = await Researcher.find(Researcher.duplication_key == key).to_list()
            try:
                merged = next(filter(lambda r: not r.marked_for_removal, researchers))
            except StopIteration:
                merged = sorted(researchers, key=lambda r: r.imported_at)[0]
            should_clear_key = True
            for i in range(len(researchers)):
                if researchers[i].uuid != merged.uuid:
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


async def eliminate_institutions_duplicates():
    logger.info("Institution duplicate elimination started...")
    keys = await Institution.aggregate([{"$group": {"_id": "$duplication_key", "count": {"$sum": 1}}}], projection_model=FindKeysResult).to_list()
    for key_res in keys:
        key = key_res.id
        if key is not None:
            institutions = await Institution.find(Institution.duplication_key == key).to_list()
            try:
                merged = next(filter(lambda ins: not ins.marked_for_removal, institutions))
            except StopIteration:
                merged = sorted(institutions, key=lambda ins: ins.imported_at)[0]
            should_clear_key = True
            for i in range(len(institutions)):
                if institutions[i].uuid != merged.uuid:
                    if institutions[i].marked_for_removal:
                        merged = await merge_service.merge_institutions(merged, institutions[i])
                    else:
                        should_clear_key = False
            if should_clear_key:
                await merged.set({Institution.duplication_key: None})
    await Institution.find(Institution.marked_for_removal == True).delete()
    logger.info("Institution duplicate elimination finished...")
