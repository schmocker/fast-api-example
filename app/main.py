from typing import Optional, List
from sqlalchemy.engine import create_engine
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

app = FastAPI(docs_url='/')


async def get_engine() -> Engine:
    return create_engine('sqlite:///app.db', echo=True)


async def get_session(engine: Engine = Depends(get_engine)) -> Session:
    with Session(engine) as session:
        yield session


class AssetBase(SQLModel):
    name: str


class Asset(AssetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class AssetRead(AssetBase):
    id: int


class AssetCreate(AssetBase):
    pass


asset_router = APIRouter(tags=['asset'])


@asset_router.get('/{id}', response_model=AssetRead)
async def get_asset_by_id(id: int, session: Session = Depends(get_session)):
    asset = session.get(Asset, id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@asset_router.get('/', response_model=List[AssetRead])
async def get_all_assets(session: Session = Depends(get_session)):
    assets = session.query(Asset).all()
    return assets


@asset_router.post('/', response_model=AssetRead)
async def get_all_assets(asset: AssetCreate, session: Session = Depends(get_session)):
    db_asset = Asset.from_orm(asset)
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


admin_router = APIRouter(tags=['admin'])


@admin_router.post('/init_db')
async def get_all_assets(engine: Engine = Depends(get_engine)):
    SQLModel.metadata.create_all(engine)
    return None


app.include_router(asset_router, prefix='/assets')
app.include_router(admin_router, prefix='/assets')
