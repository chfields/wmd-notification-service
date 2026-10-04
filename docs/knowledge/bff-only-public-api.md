---
type: invariant
title: The BFF is the only API the app and the outside world reach
description: wmd-app calls only wmd-bff; services stay internal and trust the user id the BFF passes, never one taken from a request body.
tags: [core, api, security]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: notification-request
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L16-L21
  - id: notification-routes
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L60-L86
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/bff-only-public-api.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/main.py, openapi.json]
  citations:
    - id: notification-request
      repo: github:chfields/wmd-notification-service
      path: app/main.py
      lines: [16, 21]
      symbol: NotificationRequest.userId
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:36adb12255da1a2ccc6aa3b0248bf769ad1eebb84faa6a543c9a81878af51c3d
    - id: notification-routes
      repo: github:chfields/wmd-notification-service
      path: app/main.py
      lines: [60, 86]
      symbol: send and list_for_user
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:88a972ba190dad0d6bea439b1c090316c2eb86cde584da4992332cd76b4f19c3
  confidence: high
---

notification-service has no authentication of its own; it is reached only by internal callers (wmd-bff for listing, wmd-order-service for sending) and trusts the `userId` they pass, which the BFF derives from the authenticated user. Never expose it publicly or accept a user id originating from the end user's request body.[^notification-request][^notification-routes]

What to do: keep these endpoints internal and preserve the trusted caller identity contract.

[^notification-request]: [NotificationRequest.userId](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L16-L21)
[^notification-routes]: [send and list_for_user](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/main.py#L60-L86)
