import random
from typing import Union, Tuple

from beanie.odm.documents import FindType
from beanie.odm.queries.find import FindOne
from fastapi import HTTPException

from app.db.db import client


def with_transaction(func):
    async def wrapper(*args, **kwargs):
        try:
            async with await client.start_session() as session:
                async with session.start_transaction():
                    result = await func(*args, **kwargs, session=session)
                    return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

    return wrapper


async def require_instance(result: Union[FindOne[FindType], FindOne["DocumentProjectionType"]]):
    result = await result
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="This instance was not found!")


def fix_location_util(location: Tuple[float, float]):
    return location[0] + random.uniform(0.0002, 0.0003), location[1]
