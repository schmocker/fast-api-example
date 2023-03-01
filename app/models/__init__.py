from typing import Type

from .asset import Asset, AssetCreate, AssetUpdate, AssetRead, AssetReadRelations
from .project import Project, ProjectRead, ProjectReadRelations
from .project_asset_mapping import (
    ProjectAssetMapping,
    ProjectAssetMappingRead,
    ProjectAssetMappingReadRelations,
)
from sqlmodel import SQLModel

models: list[Type[SQLModel]] = [
    AssetRead,
    AssetReadRelations,
    ProjectRead,
    ProjectReadRelations,
    ProjectAssetMappingRead,
    ProjectAssetMappingReadRelations,
]

for model in models:
    model.update_forward_refs(**{m.__name__: m for m in models})
