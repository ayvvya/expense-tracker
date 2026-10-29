def create_category(client, name="Продукты"):
    return client.post("/categories", json={"name": name}).json()["id"]


def create_expense(client, category_id, amount, date):
    return client.post(
        "/expenses",
        json={
            "amount": amount,
            "description": "Покупка",
            "date": date,
            "category_id": category_id,
        },
    )


def test_put_budget_creates_budget(client):
    category_id = create_category(client)

    response = client.put(
        "/budgets",
        json={"category_id": category_id, "month": "2026-10", "limit_amount": "5000.00"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == category_id
    assert data["month"] == "2026-10"
    assert data["limit_amount"] == "5000.00"


def test_put_budget_updates_existing_budget(client):
    category_id = create_category(client)
    payload = {"category_id": category_id, "month": "2026-10", "limit_amount": "5000.00"}
    first = client.put("/budgets", json=payload).json()

    payload["limit_amount"] = "7000.00"
    second = client.put("/budgets", json=payload).json()

    assert second["id"] == first["id"]
    assert second["limit_amount"] == "7000.00"


def test_put_budget_unknown_category_returns_404(client):
    response = client.put(
        "/budgets",
        json={"category_id": 999, "month": "2026-10", "limit_amount": "100.00"},
    )

    assert response.status_code == 404


def test_put_budget_invalid_month_returns_422(client):
    category_id = create_category(client)

    response = client.put(
        "/budgets",
        json={"category_id": category_id, "month": "2026-13", "limit_amount": "100.00"},
    )

    assert response.status_code == 422


def test_status_shows_spent_remaining_and_not_exceeded(client):
    category_id = create_category(client)
    client.put(
        "/budgets",
        json={"category_id": category_id, "month": "2026-10", "limit_amount": "1000.00"},
    )
    create_expense(client, category_id, "300.00", "2026-10-05")
    create_expense(client, category_id, "200.50", "2026-10-20")

    response = client.get("/budgets/status", params={"month": "2026-10"})

    assert response.status_code == 200
    item = response.json()[0]
    assert item["category_name"] == "Продукты"
    assert item["spent"] == "500.50"
    assert item["remaining"] == "499.50"
    assert item["exceeded"] is False


def test_status_marks_exceeded_budget(client):
    category_id = create_category(client)
    client.put(
        "/budgets",
        json={"category_id": category_id, "month": "2026-10", "limit_amount": "100.00"},
    )
    create_expense(client, category_id, "150.00", "2026-10-03")

    item = client.get("/budgets/status", params={"month": "2026-10"}).json()[0]

    assert item["spent"] == "150.00"
    assert item["remaining"] == "-50.00"
    assert item["exceeded"] is True


def test_status_ignores_expenses_from_other_months(client):
    category_id = create_category(client)
    client.put(
        "/budgets",
        json={"category_id": category_id, "month": "2026-10", "limit_amount": "1000.00"},
    )
    create_expense(client, category_id, "400.00", "2026-09-30")
    create_expense(client, category_id, "100.00", "2026-11-01")
    create_expense(client, category_id, "70.00", "2026-10-31")

    item = client.get("/budgets/status", params={"month": "2026-10"}).json()[0]

    assert item["spent"] == "70.00"
