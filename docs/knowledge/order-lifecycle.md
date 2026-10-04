---
type: invariant
title: Orders reserve stock first and are confirmed only after notification
description: An order exists only after catalog-service reserves all its stock in one transaction, and moves from pending to confirmed only when notification-service accepts the confirmation, which is idempotent per order and kind.
tags: [core, orders, idempotency]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: send
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L60-L76
  - id: notifications-migration
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/migrations/001_init.sql#L1-L11
  - id: retry-test
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/tests/test_notifications.py#L17-L22
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/order-lifecycle.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/main.py, migrations/**]
  citations:
    - id: send
      repo: github:chfields/wmd-notification-service
      path: app/main.py
      lines: [60, 76]
      symbol: send
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:50c76e728034a12304ea79552d4f9afe646a041bf11a28343d01294401f921b2
    - id: notifications-migration
      repo: github:chfields/wmd-notification-service
      path: migrations/001_init.sql
      lines: [1, 11]
      symbol: notifications
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:b1dc150f026a712a359da2ff90396a36fe7fa868f5b2362c996bd2e1f3a45cf7
    - id: retry-test
      repo: github:chfields/wmd-notification-service
      path: tests/test_notifications.py
      lines: [17, 22]
      symbol: test_a_retry_returns_the_first_notification
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:3d814c0536a9f55e5206ada65861a1005ff605636a2a3f5b2980c002d5412b2e
  confidence: high
---

order-service confirms an order only after `POST /v1/notifications` succeeds, so this endpoint must stay idempotent per (`order_id`, `kind`): the first call returns 201, a retry returns 200 with the same notification and creates no duplicate. Never drop the unique constraint or make a retry fail.[^send][^notifications-migration][^retry-test]

Why: a retried confirmation must preserve the first delivery record.

[^send]: [send](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L60-L76)
[^notifications-migration]: [notifications migration](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/migrations/001_init.sql#L1-L11)
[^retry-test]: [retry behavior test](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/tests/test_notifications.py#L17-L22)
