def _create_item(client, **overrides):
    payload = {"title": "Comprar pan", "priority": "high"}
    payload.update(overrides)
    return client.post("/items", json=payload)


def test_create_item_returns_201(client):
    response = _create_item(client, description="de la panaderia")
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Comprar pan"
    assert body["priority"] == "high"
    assert body["status"] == "pending"
    assert "id" in body
    assert "createdAt" in body


def test_create_item_missing_required_fields_returns_400(client):
    response = client.post("/items", json={"description": "faltan campos"})
    assert response.status_code == 400


def test_list_items_with_pagination(client):
    _create_item(client)
    _create_item(client, title="Tarea 2", priority="low")
    response = client.get("/items?page=1&limit=10")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["page"] == 1
    assert body["limit"] == 10
    assert len(body["items"]) == 2


def test_get_item_by_id(client):
    created = _create_item(client).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_item_not_found_returns_404(client):
    response = client.get("/items/no-existe-123")
    assert response.status_code == 404


def test_update_status_returns_200(client):
    created = _create_item(client).json()
    response = client.patch(f"/items/{created['id']}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_status_not_found_returns_404(client):
    response = client.patch("/items/no-existe-123", json={"status": "done"})
    assert response.status_code == 404


def test_update_status_invalid_value_returns_400(client):
    created = _create_item(client).json()
    response = client.patch(f"/items/{created['id']}", json={"status": "volando"})
    assert response.status_code == 400
