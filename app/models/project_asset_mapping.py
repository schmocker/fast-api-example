from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import declared_attr
from sqlalchemy.util import classproperty
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .asset import Asset, AssetRead
    from .project import Project, ProjectRead


class ProjectAssetMappingBase(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    assetId: int
    projectId: int


class ProjectAssetMapping(ProjectAssetMappingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    assetId: int = Field(default=None, foreign_key="Asset.id")
    projectId: int = Field(default=None, foreign_key="Project.id")

    # relationships
    # asset: "Asset" = Relationship(back_populates="projectAssetMappings")
    # project: "Project" = Relationship(back_populates="projectAssetMappings")


class ProjectAssetMappingCreate(ProjectAssetMappingBase):
    pass


class ProjectAssetMappingRead(ProjectAssetMappingBase):
    id: int


class ProjectAssetMappingReadRelations(ProjectAssetMappingRead):
    # asset: Optional["AssetRead"]
    # project: Optional["ProjectRead"]
    pass


class ProjectAssetMappingUpdate(ProjectAssetMappingBase):
    assetId: Optional[int] = None
    projectId: Optional[int] = None
