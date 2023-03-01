from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..dependencies.sql import get_session
from ..models.project import (
    ProjectRead,
    ProjectCreate,
    Project,
    ProjectUpdate,
    ProjectReadRelations,
)
from sqlalchemy.orm import Session

route = APIRouter(tags=["projects"])


@route.get("/", response_model=list[ProjectRead])
async def get_projects(session: Session = Depends(get_session)):
    projects = session.query(Project).all()
    return projects


@route.get("/{project_id}", response_model=ProjectReadRelations)
async def get_project_by_id(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@route.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project: ProjectCreate, session: Session = Depends(get_session)
):
    db_project = Project.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@route.put("/{project_id}", response_model=ProjectRead)
async def create_or_update_project(
    project_id: int, project: ProjectCreate, session: Session = Depends(get_session)
):
    db_project = session.get(Project, project_id)
    if not db_project:
        return await create_project(project, session)
    project_data = project.dict()
    for key, value in project_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@route.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int, project: ProjectUpdate, session: Session = Depends(get_session)
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@route.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(
    project_id: int, session: Session = Depends(get_session)
):
    project = session.query(Project).get(project_id)

    if project:
        session.delete(project)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id {id} not found",
        )
    return None
