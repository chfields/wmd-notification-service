---
type: convention
title: Migrations run at startup in one locked transaction
description: Every replica applies pending migrations on boot inside a single transaction under an advisory lock, so each migration must be transactional and safe to wait on.
tags: [data, migrations, postgres]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: database-migrate
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L32-L49
  - id: app-lifespan
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L51-L54
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/db.py, migrations/**, app/main.py]
  citations:
    - id: database-migrate
      repo: github:chfields/wmd-notification-service
      path: app/db.py
      lines: [32, 49]
      symbol: Database.migrate
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:b407b73603296fbfa7070366011bf9fcd67d69526c3480a8be4047fa2204001d
    - id: app-lifespan
      repo: github:chfields/wmd-notification-service
      path: app/main.py
      lines: [51, 54]
      symbol: create_app.lifespan
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:5b233974ec31888d79b7a53b0b0e265cc9129c9005424504254090891c1841db
  confidence: high
---

Migrations are applied by the app on startup, not by a separate job; replicas serialize on an advisory transaction lock and all pending files run in one transaction. So a migration must not use statements that cannot run inside a transaction (e.g. `CREATE INDEX CONCURRENTLY`), and long-running migrations block every starting replica's readiness.[^database-migrate][^app-lifespan]

What to do: keep migrations transactional, short enough for startup, and safe to wait on.

[^database-migrate]: [Database.migrate](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L32-L49)
[^app-lifespan]: [create_app lifespan](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L51-L54)
