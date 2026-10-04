# Architecture knowledge

## Core

- [Each service owns one Postgres schema and nothing else](service-data-ownership.md) — A service reads and writes only its own schema through its own login role; another service's data is reached only through that service's HTTP API.
- [The BFF is the only API the app and the outside world reach](bff-only-public-api.md) — wmd-app calls only wmd-bff; services stay internal and trust the user id the BFF passes, never one taken from a request body.
- [Every request carries one x-correlation-id end to end](correlation-id-propagation.md) — Each service accepts x-correlation-id (or makes one), logs it, returns it, and forwards it on every outbound call.
- [Errors are {"error": {"code", "message"}} with stable codes](error-contract.md) — Every API error uses this shape, and codes are stable identifiers clients branch on, so they are never renamed.
- [Orders reserve stock first and are confirmed only after notification](order-lifecycle.md) — An order exists only after catalog-service reserves all its stock in one transaction, and moves from pending to confirmed only when notification-service accepts the confirmation, which is idempotent per order and kind.
- [Only merged main reaches staging](only-merged-code-reaches-staging.md) — deploy.sh builds every service from its origin/main in a clean checkout, so staging never runs unreviewed code.

## This repository

- [Migrations run at startup in one locked transaction](migrations-run-at-startup.md) — Every replica applies pending migrations on boot inside a single transaction under an advisory lock, so each migration must be transactional and safe to wait on.
