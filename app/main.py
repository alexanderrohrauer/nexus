from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import dashboard_controller
from app.db import db
from app.middlewares import cors_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield


app = FastAPI(lifespan=lifespan)


cors_middleware.add(app)

app.include_router(dashboard_controller.router)
