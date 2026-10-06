import pytest

CONFIRMED = {
    "userId": "user-1",
    "orderId": "3f2a9c1e-0000",
    "kind": "order_confirmed",
    "totalCents": 2346,
}


def test_sends_an_order_confirmation(client):
    response = client.post("/v1/notifications", json=CONFIRMED)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Order confirmed"
    assert body["body"] == (
        "Your order 3f2a9c1e for $23.46 is confirmed for delivery in the morning (8am–12pm)."
    )
    assert (body["channel"], body["status"]) == ("in_app", "delivered")


def test_a_retry_returns_the_first_notification(client):
    first = client.post(
        "/v1/notifications", json={**CONFIRMED, "giftMessage": "Happy birthday!"}
    ).json()
    retry = client.post("/v1/notifications", json=CONFIRMED)
    assert retry.status_code == 200
    assert retry.json()["id"] == first["id"]
    assert retry.json()["body"] == first["body"]
    assert len(client.get("/v1/notifications", params={"userId": "user-1"}).json()) == 1


def test_includes_a_gift_message_in_an_order_confirmation(client):
    response = client.post(
        "/v1/notifications", json={**CONFIRMED, "giftMessage": "  Enjoy your gift!  "}
    )
    assert response.status_code == 201
    assert response.json()["body"] == (
        "Your order 3f2a9c1e for $23.46 is confirmed for delivery in the morning (8am–12pm). "
        'Gift message: "Enjoy your gift!"'
    )


@pytest.mark.parametrize(
    "gift_message", [{}, {"giftMessage": None}, {"giftMessage": ""}, {"giftMessage": "   "}]
)
def test_omits_an_empty_gift_message_from_an_order_confirmation(client, gift_message):
    payload = {**CONFIRMED, "orderId": "empty-gift-message", **gift_message}
    response = client.post("/v1/notifications", json=payload)
    assert response.status_code == 201
    assert response.json()["body"] == (
        "Your order empty-gi for $23.46 is confirmed for delivery in the morning (8am–12pm)."
    )


@pytest.mark.parametrize(
    ("delivery_window", "phrase"),
    [
        ("morning", "morning (8am–12pm)"),
        ("afternoon", "afternoon (12–5pm)"),
        ("evening", "evening (5–9pm)"),
    ],
)
def test_includes_the_delivery_window_in_an_order_confirmation(client, delivery_window, phrase):
    order_id = f"order-{delivery_window}"
    response = client.post(
        "/v1/notifications",
        json={**CONFIRMED, "orderId": order_id, "deliveryWindow": delivery_window},
    )
    assert response.status_code == 201
    assert response.json()["body"] == (
        f"Your order {order_id[:8]} for $23.46 is confirmed for delivery in the {phrase}."
    )


def test_rejects_an_invalid_delivery_window(client):
    response = client.post("/v1/notifications", json={**CONFIRMED, "deliveryWindow": "overnight"})
    assert response.status_code == 422


def test_rejects_a_gift_message_over_200_characters(client):
    response = client.post("/v1/notifications", json={**CONFIRMED, "giftMessage": "x" * 201})
    assert response.status_code == 422


def test_lists_a_users_notifications_newest_first(client):
    client.post("/v1/notifications", json={**CONFIRMED, "orderId": "order-a"})
    client.post("/v1/notifications", json={**CONFIRMED, "orderId": "order-b"})
    client.post("/v1/notifications", json={**CONFIRMED, "userId": "user-2", "orderId": "order-c"})
    listed = client.get("/v1/notifications", params={"userId": "user-1"}).json()
    assert [n["orderId"] for n in listed] == ["order-b", "order-a"]


def test_refuses_an_unknown_kind_and_requires_a_user(client):
    assert client.post("/v1/notifications", json={**CONFIRMED, "kind": "spam"}).status_code == 422
    assert client.get("/v1/notifications").status_code == 422
