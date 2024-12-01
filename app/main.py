from contextlib import asynccontextmanager
from typing import List, Annotated

from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import And, Or
from fastapi import FastAPI
from fastapi.params import Depends

from app.db import db
from app.middlewares import cors_middleware
from app.models import Product
from app.utils.api_utils import SearchAndFilterParams


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield


app = FastAPI(lifespan=lifespan)

cors_middleware.add(app)


def service(params: SearchAndFilterParams):
    query_parsed = params.get_filter()
    sorts = params.get_sort()
    return Product.find(*query_parsed).sort(sorts).to_list()


@app.get("/")
async def root(params: Annotated[SearchAndFilterParams, Depends()]) -> List[Product]:
    custom_filter = And(
        Product.name == "Yoga Mat",
        Or(Product.category.name == "Fitness", RegEx(Product.category.description, r"abc"))
    )

    print(custom_filter)

    docs = await service(params)

    return docs
    # raise HTTPException(status_code=500)
