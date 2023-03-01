from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..dependencies.sql import get_session
from ..models.project_asset_mapping import (
    ProjectAssetMappingRead,
    ProjectAssetMappingCreate,
    ProjectAssetMapping,
    ProjectAssetMappingUpdate,
    ProjectAssetMappingReadRelations,
)
from sqlalchemy.orm import Session

route = APIRouter(tags=["project_project_asset_mapping_mappings"])


@route.get("/", response_model=List[ProjectAssetMappingRead])
async def get_project_asset_mappings(session: Session = Depends(get_session)):
    project_asset_mappings = session.query(ProjectAssetMapping).all()
    return project_asset_mappings


@route.get(
    "/{project_asset_mapping_id}", response_model=ProjectAssetMappingReadRelations
)
async def get_project_asset_mapping_by_id(
    project_asset_mapping_id: int, session: Session = Depends(get_session)
):
    project_asset_mapping = session.get(ProjectAssetMapping, project_asset_mapping_id)
    if not project_asset_mapping:
        raise HTTPException(status_code=404, detail="ProjectAssetMapping not found")
    return project_asset_mapping


@route.post(
    "/",
    response_model=ProjectAssetMappingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_asset_mapping(
    project_asset_mapping: ProjectAssetMappingCreate,
    session: Session = Depends(get_session),
):
    db_project_asset_mapping = ProjectAssetMapping.from_orm(project_asset_mapping)
    session.add(db_project_asset_mapping)
    session.commit()
    session.refresh(db_project_asset_mapping)
    return db_project_asset_mapping


@route.put("/{project_asset_mapping_id}", response_model=ProjectAssetMappingRead)
async def create_or_update_project_asset_mapping(
    project_asset_mapping_id: int,
    project_asset_mapping: ProjectAssetMappingCreate,
    session: Session = Depends(get_session),
):
    db_project_asset_mapping = session.get(
        ProjectAssetMapping, project_asset_mapping_id
    )
    if not db_project_asset_mapping:
        return await create_project_asset_mapping(project_asset_mapping, session)
    project_asset_mapping_data = project_asset_mapping.dict()
    for key, value in project_asset_mapping_data.items():
        setattr(db_project_asset_mapping, key, value)
    session.add(db_project_asset_mapping)
    session.commit()
    session.refresh(db_project_asset_mapping)
    return db_project_asset_mapping


@route.patch("/{project_asset_mapping_id}", response_model=ProjectAssetMappingRead)
async def update_project_asset_mapping(
    project_asset_mapping_id: int,
    project_asset_mapping: ProjectAssetMappingUpdate,
    session: Session = Depends(get_session),
):
    db_project_asset_mapping = session.get(
        ProjectAssetMapping, project_asset_mapping_id
    )
    if not db_project_asset_mapping:
        raise HTTPException(status_code=404, detail="ProjectAssetMapping not found")
    project_asset_mapping_data = project_asset_mapping.dict(exclude_unset=True)
    for key, value in project_asset_mapping_data.items():
        setattr(db_project_asset_mapping, key, value)
    session.add(db_project_asset_mapping)
    session.commit()
    session.refresh(db_project_asset_mapping)
    return db_project_asset_mapping


@route.delete("/{project_asset_mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_asset_mapping_by_id(
    project_asset_mapping_id: int, session: Session = Depends(get_session)
):
    project_asset_mapping = session.query(ProjectAssetMapping).get(
        project_asset_mapping_id
    )

    if project_asset_mapping:
        session.delete(project_asset_mapping)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project_asset_mapping with id {id} not found",
        )
    return None
