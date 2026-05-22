def test_tenant_cannot_see_others_integration(client1, client2):
    integration = client1.post("/integrations", json={"name": "tenant1_int", "type": "isolated"}).json()
    resp = client2.get(f"/integrations/{integration['id']}")
    assert resp.status_code == 404

def test_tenant_cannot_modify_others_integration(client1, client2):
    integration = client1.post("/integrations", json={"name": "tenant1_int2", "type": "test"}).json()
    resp = client2.put("/integrations", json={"id": integration["id"], "name": "hacked"})
    assert resp.status_code == 404

def test_tenant_cannot_delete_others_integration(client1, client2):
    integration = client1.post("/integrations", json={"name": "tenant1_int3", "type": "test"}).json()
    resp = client2.delete(f"/integrations/{integration['id']}")
    assert resp.status_code == 404

def test_tenant_cannot_see_others_asset(client1, client2):
    integration = client1.post("/integrations", json={"name": "asset_tenant1", "type": "test"}).json()
    asset = client1.post("/assets", json={"integration_id": integration["id"], "name": "my_asset", "description": "secret"}).json()
    resp = client2.get(f"/assets/{asset['id']}")
    assert resp.status_code == 404
