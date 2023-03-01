from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import declared_attr
from sqlalchemy.util import classproperty
from sqlmodel import SQLModel, Field, Relationship
from .project_asset_mapping import ProjectAssetMapping, ProjectAssetMappingRead

if TYPE_CHECKING:
    from .asset import Asset, AssetRead


class ProjectBase(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    name: str
    description: Optional[str] = None


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # projectAssetMappings: List["ProjectAssetMapping"] = Relationship(
    #     back_populates="project"
    # )
    assets: List["Asset"] = Relationship(
        back_populates="projects", link_model=ProjectAssetMapping
    )


class ProjectCreate(ProjectBase):
    pass

    class Config:
        schema_extra = {
            "example": {"name": "Foo", "description": "A very nice Project"}
        }


class ProjectRead(ProjectBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Foo",
                "description": "A very nice Project",
            }
        }


class ProjectReadRelations(ProjectRead):
    # projectAssetMappings: List["ProjectAssetMappingRead"]
    assets: List["AssetRead"]

    class Config:
        schema_extra = {
            "example": {"id": 2, "name": "Bar", "description": "A super nice Project"}
        }


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {"name": "Bar", "description": "A super nice Project"}
        }
