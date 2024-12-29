import datetime
import json
import logging
import re
from uuid import UUID

from beanie.odm.operators.find.evaluation import RegEx
from fastapi import APIRouter

from app.models import Researcher
from app.services import researchers_service

router = APIRouter(
    prefix="/researchers",
    tags=["researcher"]
)

logger = logging.getLogger("uvicorn.error")

transforms = {
    "imported_at": datetime.datetime.fromisoformat
}


def transform(field):
    if field["field"] == "imported_at":
        return datetime.datetime.fromisoformat(field["value"])
    if field["operator"] == "$regex":
        return re.compile(field["value"], flags=re.IGNORECASE)
    if field["field"] == "uuid":
        return list(map(lambda option: UUID(option["value"]), field["value"]))
    return field["value"]


@router.get("")
async def get_researchers(limit: int = 20, offset: int = 0, q="[]", search: str | None = None) -> list[Researcher]:
    query = json.loads(q)
    boolean_builder = [
        {criterion["field"]: {criterion["operator"]: transform(criterion)}}
        for criterion in query
    ]
    if search is not None:
        boolean_builder.append(RegEx(Researcher.full_name, re.compile(search, flags=re.IGNORECASE)))
    query = {
        "$and": boolean_builder
    } if len(boolean_builder) > 0 else {}
    logger.debug(query)
    # TODO implement proper search
    result = await Researcher.find(query, fetch_links=True).limit(limit).skip(offset).to_list()
    return result


@router.get("/{uuid}")
async def get_researcher(uuid: UUID) -> Researcher:
    return await researchers_service.find_by_id(uuid)
