from utils.data_generators import random_asset_name

def test_create_asset(client1):
    integration = client1.post("/integrations", json={"name": "asset_test_int", "type": "test"}).json()
    payload = {"integration_id": integration["id"], "name": random_asset_name(), "description": "test asset"}
    resp = client1.post("/assets", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["integration_id"] == integration["id"]

def test_get_asset(client1):
    integration = client1.post("/integrations", json={"name": "get_asset_int", "type": "test"}).json()
    asset = client1.post("/assets", json={"integration_id": integration["id"], "name": "get_asset", "description": "desc"}).json()
    resp = client1.get(f"/assets/{asset['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == asset["id"]

def test_update_asset(client1):
    integration = client1.post("/integrations", json={"name": "upd_asset_int", "type": "test"}).json()
    asset = client1.post("/assets", json={"integration_id": integration["id"], "name": "old_name", "description": "old_desc"}).json()
    update_payload = {"id": asset["id"], "name": "new_name", "description": "new_desc"}
    resp = client1.patch("/assets", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["name"] == "new_name"

def test_delete_asset(client1):
    integration = client1.post("/integrations", json={"name": "del_asset_int", "type": "test"}).json()
    asset = client1.post("/assets", json={"integration_id": integration["id"], "name": "del_asset", "description": ""}).json()
    resp = client1.delete(f"/assets/{asset['id']}")
    assert resp.status_code == 204
    get_resp = client1.get(f"/assets/{asset['id']}")
    assert get_resp.status_code == 404
