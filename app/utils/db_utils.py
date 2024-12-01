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
