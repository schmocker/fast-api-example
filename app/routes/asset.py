from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..dependencies.sql import get_session
from ..models.asset import (
    AssetRead,
    AssetCreate,
    Asset,
    AssetUpdate,
    AssetReadRelations,
)
from sqlalchemy.orm import Session

route = APIRouter(tags=["assets"])


@route.get("/", response_model=list[AssetRead])
async def get_assets(session: Session = Depends(get_session)):
    assets = session.query(Asset).all()
    return assets


@route.get("/{asset_id}", response_model=AssetReadRelations)
async def get_asset_by_id(asset_id: int, session: Session = Depends(get_session)):
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@route.post(
    "/",
    response_model=AssetRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_asset(asset: AssetCreate, session: Session = Depends(get_session)):
    db_asset = Asset.from_orm(asset)
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


@route.put("/{asset_id}", response_model=AssetRead)
async def create_or_update_asset(
    asset_id: int, asset: AssetCreate, session: Session = Depends(get_session)
):
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        return await create_asset(asset, session)
    asset_data = asset.dict()
    for key, value in asset_data.items():
        setattr(db_asset, key, value)
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


@route.patch("/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: int, asset: AssetUpdate, session: Session = Depends(get_session)
):
    db_asset = session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset_data = asset.dict(exclude_unset=True)
    for key, value in asset_data.items():
        setattr(db_asset, key, value)
    session.add(db_asset)
    session.commit()
    session.refresh(db_asset)
    return db_asset


@route.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset_by_id(asset_id: int, session: Session = Depends(get_session)):
    asset = session.query(Asset).get(asset_id)

    if asset:
        session.delete(asset)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"asset with id {id} not found",
        )
    return None
