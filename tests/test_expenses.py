def create_category(client, name="Продукты"):
    response = client.post("/categories", json={"name": name})
    return response.json()["id"]


def test_create_expense(client):
    category_id = create_category(client)

    response = client.post(
        "/expenses",
        json={
            "amount": "250.50",
            "description": "Покупки в магазине",
            "date": "2026-10-15",
            "category_id": category_id,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "250.50"
    assert data["description"] == "Покупки в магазине"
    assert data["category_id"] == category_id


def test_create_expense_with_unknown_category_returns_404(client):
    response = client.post(
        "/expenses",
        json={
            "amount": "100.00",
            "description": "Тест",
            "date": "2026-10-15",
            "category_id": 999,
        },
    )

    assert response.status_code == 404


def test_create_expense_with_negative_amount_returns_422(client):
    category_id = create_category(client)

    response = client.post(
        "/expenses",
        json={
            "amount": "-10.00",
            "description": "Ошибка",
            "date": "2026-10-15",
            "category_id": category_id,
        },
    )

    assert response.status_code == 422


def test_list_expenses_filtered_by_category(client):
    food_id = create_category(client, "Продукты")
    transport_id = create_category(client, "Транспорт")

    client.post(
        "/expenses",
        json={"amount": "100.00", "description": "Хлеб", "date": "2026-10-10", "category_id": food_id},
    )
    client.post(
        "/expenses",
        json={"amount": "50.00", "description": "Метро", "date": "2026-10-11", "category_id": transport_id},
    )

    response = client.get("/expenses", params={"category_id": food_id})

    assert response.status_code == 200
    descriptions = [item["description"] for item in response.json()]
    assert descriptions == ["Хлеб"]


def test_delete_expense(client):
    category_id = create_category(client)
    created = client.post(
        "/expenses",
        json={"amount": "20.00", "description": "Кофе", "date": "2026-10-12", "category_id": category_id},
    ).json()

    response = client.delete(f"/expenses/{created['id']}")

    assert response.status_code == 204
    assert client.get("/expenses").json() == []


def test_delete_unknown_expense_returns_404(client):
    response = client.delete("/expenses/999")

    assert response.status_code == 404
