from fastapi import FastAPI
from .routes import admin_route, asset_route, project_route, project_asset_mapping_route


app = FastAPI(docs_url='/')


app.include_router(asset_route, prefix="/assets")
app.include_router(project_route, prefix="/projects")
app.include_router(project_asset_mapping_route, prefix="/project_asset_mappings")
app.include_router(admin_route, prefix="/admin")
