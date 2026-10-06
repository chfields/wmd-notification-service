"""notification-service: sends customers notifications and records their delivery status."""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field

from app.db import Database, database_from_env
from app.observability import configure_logging, install

SERVICE = "notification-service"


class NotificationRequest(BaseModel):
    userId: str = Field(min_length=1, max_length=64)
    orderId: str = Field(min_length=1, max_length=64)
    kind: Literal["order_confirmed"]
    totalCents: int = Field(ge=0)
    giftMessage: str | None = Field(default=None, max_length=200)
    deliveryWindow: Literal["morning", "afternoon", "evening"] | None = "morning"


class Notification(BaseModel):
    id: str
    userId: str
    orderId: str
    kind: str
    title: str
    body: str
    channel: str
    status: str
    createdAt: datetime


def _content(request: NotificationRequest) -> tuple[str, str]:
    total = f"${request.totalCents / 100:.2f}"
    delivery_window = request.deliveryWindow or "morning"
    delivery_phrase = {
        "morning": "morning (8am–12pm)",
        "afternoon": "afternoon (12–5pm)",
        "evening": "evening (5–9pm)",
    }[delivery_window]
    body = (
        f"Your order {request.orderId[:8]} for {total} is confirmed for delivery in the "
        f"{delivery_phrase}."
    )
    gift_message = request.giftMessage.strip() if request.giftMessage else ""
    if gift_message:
        body += f' Gift message: "{gift_message}"'
    return "Order confirmed", body


def _notification(row: dict) -> Notification:
    return Notification(
        id=str(row["id"]),
        userId=row["user_id"],
        orderId=row["order_id"],
        kind=row["kind"],
        title=row["title"],
        body=row["body"],
        channel=row["channel"],
        status=row["status"],
        createdAt=row["created_at"],
    )


COLUMNS = "id, user_id, order_id, kind, title, body, channel, status, created_at"


def create_app(db: Database | None = None, *, migrate: bool = True) -> FastAPI:
    database = db or database_from_env("notification")

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        if migrate:
            database.migrate()
        yield

    app = FastAPI(title="wmd notification-service", version="1.0.0", lifespan=lifespan)
    install(app, database.ping)

    @app.post("/v1/notifications", response_model=Notification, status_code=201)
    def send(request: NotificationRequest, response: Response) -> Notification:
        """Deliver once per order and kind: a retry returns the first notification (200)."""
        title, body = _content(request)
        with database.connect() as conn:
            row = conn.execute(
                f"insert into notifications (user_id, order_id, kind, title, body)"
                f" values (%s, %s, %s, %s, %s)"
                f" on conflict (order_id, kind) do nothing returning {COLUMNS}",
                (request.userId, request.orderId, request.kind, title, body),
            ).fetchone()
            if row is None:
                response.status_code = 200
                row = conn.execute(
                    f"select {COLUMNS} from notifications where order_id = %s and kind = %s",
                    (request.orderId, request.kind),
                ).fetchone()
        return _notification(row)

    @app.get("/v1/notifications", response_model=list[Notification])
    def list_for_user(
        userId: str = Query(min_length=1, max_length=64),  # noqa: N803 - API field name
    ) -> list[Notification]:
        with database.connect() as conn:
            rows = conn.execute(
                f"select {COLUMNS} from notifications where user_id = %s"
                f" order by created_at desc limit 50",
                (userId,),
            ).fetchall()
        return [_notification(row) for row in rows]

    return app


def main() -> FastAPI:
    """uvicorn entrypoint: `uvicorn app.main:main --factory`."""
    configure_logging(SERVICE)
    return create_app()
