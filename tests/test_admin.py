from fastapi.testclient import TestClient
from app.main import app
import os
from app.dependencies.settings import get_settings

client = TestClient(app)


def test_init_db():
    settings = get_settings()
    if settings.database.dialect == "sqlite":
        os.remove(settings.database.name)

    response = client.post("/admin/init_db")
    assert response.status_code == 200
