from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import declared_attr
from sqlalchemy.util import classproperty
from sqlmodel import SQLModel, Field, Relationship
from .project_asset_mapping import ProjectAssetMapping, ProjectAssetMappingRead

if TYPE_CHECKING:
    from .project import Project, ProjectRead


class AssetBase(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    name: str
    description: Optional[str] = None
    parentId: Optional[int] = None


class Asset(AssetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    parentId: Optional[int] = Field(foreign_key="Asset.id")
    parent: Optional["Asset"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Asset.id"}
    )
    children: list["Asset"] = Relationship(back_populates="parent")
    # projectAssetMappings: List["ProjectAssetMapping"] = Relationship(
    #     back_populates="asset"
    # )
    projects: List["Project"] = Relationship(
        back_populates="assets", link_model=ProjectAssetMapping
    )


class AssetCreate(AssetBase):
    pass

    class Config:
        schema_extra = {"example": {"name": "Foo", "description": "A very nice Asset"}}


class AssetRead(AssetBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Foo",
                "description": "A very nice Asset",
            }
        }


class AssetReadRelations(AssetRead):
    parent: Optional[AssetRead] = None
    children: List[AssetRead] = []
    # projectAssetMappings: List["ProjectAssetMappingRead"] = Field(
    #     ..., description="list of associated project mappers"
    # )
    projects: List["ProjectRead"] = Field(
        ..., description="list of associated projects"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "name": "Bar",
                "description": "A super nice Asset",
                "parentId": 1,
                "parent": {
                    "id": 1,
                    "name": "Foo",
                    "description": "A very nice Asset",
                },
            }
        }


class AssetUpdate(AssetBase):
    name: Optional[str] = None
    description: Optional[str] = None
    parentId: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Bar",
                "description": "A super nice Asset",
                "parentId": 1,
            }
        }
