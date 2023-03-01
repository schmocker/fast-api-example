from sqlalchemy.engine import Engine

from sqlmodel import SQLModel

from app import models
from app.dependencies.sql import get_engine

from fastapi import APIRouter, Depends

route = APIRouter(tags=["admin"])


@route.post("/init_db")
async def init_db(engine: Engine = Depends(get_engine)):
    SQLModel.metadata.create_all(engine)
