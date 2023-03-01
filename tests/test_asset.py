from fastapi.testclient import TestClient
from app.main import app
from app.models.asset import Asset

client = TestClient(app)

asset = Asset(name="string", description="string")


def test_post_asset():
    response = client.post("/assets", json=asset.dict())
    assert response.status_code == 201


def test_get_assets():
    response = client.get("/assets")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_asset():
    response = client.get(f"/assets/1")
    assert response.status_code == 200
    assert response.json()["name"] == asset.name


def test_put_asset():
    asset.id = 1
    asset.name = "new_string"
    response = client.put(f"/assets/{asset.id}", json=asset.dict())
    assert response.status_code == 200
    assert response.json()["name"] == asset.name


def test_patch_asset():
    asset.name = "new_string"
    new_description = "new patched description"
    response = client.patch(
        f"/assets/{asset.id}", json={"description": new_description}
    )
    assert response.status_code == 200
    assert response.json()["description"] == new_description


def test_delete_asset():
    response = client.delete(f"/assets/{asset.id}")
    assert response.status_code == 204
    response = client.get("/assets")
    assert len(response.json()) == 0
