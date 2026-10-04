---
type: invariant
title: Each service owns one Postgres schema and nothing else
description: A service reads and writes only its own schema through its own login role; another service's data is reached only through that service's HTTP API.
tags: [core, data, postgres]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: db-connect
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L23-L29
  - id: db-from-env
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L55-L56
  - id: app-create
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L47-L57
  - id: notifications-migration
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/migrations/001_init.sql#L1-L11
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/service-data-ownership.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/db.py, migrations/**, app/main.py]
  citations:
    - id: db-connect
      repo: github:chfields/wmd-notification-service
      path: app/db.py
      lines: [23, 29]
      symbol: Database.connect
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:f47fbe484a8aed2371dfcc053c0ba3b12e2ed7838c1b2141a219aa290b0e2b69
    - id: db-from-env
      repo: github:chfields/wmd-notification-service
      path: app/db.py
      lines: [55, 56]
      symbol: database_from_env
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:f14422881767f716c85da093b82fd433a9c92bdc845b815512b17cd199b1f26f
    - id: app-create
      repo: github:chfields/wmd-notification-service
      path: app/main.py
      lines: [47, 57]
      symbol: create_app
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:a5180c111a8de82917e2a2b58dc511ea6f78e076c401b9412ec0966687fe49e5
    - id: notifications-migration
      repo: github:chfields/wmd-notification-service
      path: migrations/001_init.sql
      lines: [1, 11]
      symbol: notifications
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:b1dc150f026a712a359da2ff90396a36fe7fa868f5b2362c996bd2e1f3a45cf7
  confidence: high
---

notification-service connects with `search_path` pinned to its own `notification` schema and creates only its own tables via `migrations/`; it never queries order or catalog data, and anything it needs (`userId`, `orderId`, `totalCents`) arrives in the request.[^db-connect][^db-from-env][^app-create][^notifications-migration]

Why: schema isolation keeps service data behind its owning service's API.

[^db-connect]: [Database.connect](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L23-L29)
[^db-from-env]: [database_from_env](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/db.py#L55-L56)
[^app-create]: [create_app](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L47-L57)
[^notifications-migration]: [notifications migration](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/migrations/001_init.sql#L1-L11)
