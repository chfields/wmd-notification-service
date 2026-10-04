# wmd-notification-service

Sends customers notifications (in-app today) and records delivery status. Part of WMD Shop, the Wardby mobile demo.

| Route | Purpose |
|---|---|
| `POST /v1/notifications` | Send a notification once per order and kind (201; a retry returns the first, 200) |
| `GET /v1/notifications?userId=` | A user's notifications, newest first |
| `GET /healthz`, `/readyz`, `/metrics` | Health, readiness, Prometheus metrics |

The full contract is [`openapi.json`](openapi.json). See [`AGENTS.md`](AGENTS.md)
for how to run and change it.

Configuration: `DATABASE_URL` (required), `DB_SCHEMA` (default `notification`).
