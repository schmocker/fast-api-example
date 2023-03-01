from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from fastapi import Depends

from .settings import get_settings, Settings


async def get_engine(settings: Settings = Depends(get_settings)) -> Engine:
    return create_engine(settings.database.url, echo=True)


async def get_session(engine=Depends(get_engine)) -> Session:
    with Session(engine) as session:
        yield session
