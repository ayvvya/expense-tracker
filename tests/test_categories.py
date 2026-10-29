def test_create_category(client):
    response = client.post("/categories", json={"name": "Продукты"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Продукты"
    assert "id" in data


def test_create_duplicate_category_returns_409(client):
    client.post("/categories", json={"name": "Транспорт"})

    response = client.post("/categories", json={"name": "Транспорт"})

    assert response.status_code == 409


def test_create_category_with_empty_name_returns_422(client):
    response = client.post("/categories", json={"name": ""})

    assert response.status_code == 422


def test_list_categories_sorted_by_name(client):
    client.post("/categories", json={"name": "Транспорт"})
    client.post("/categories", json={"name": "Продукты"})

    response = client.get("/categories")

    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Продукты", "Транспорт"]
