---
type: convention
title: 'Errors are {"error": {"code", "message"}} with stable codes'
description: Every API error uses this shape, and codes are stable identifiers clients branch on, so they are never renamed.
tags: [core, api, errors]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: api-error
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L27-L32
  - id: api-error-handler
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L102-L105
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/error-contract.md
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/observability.py, app/main.py, openapi.json]
  citations:
    - id: api-error
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [27, 32]
      symbol: ApiError
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:0dab7e706cce5dc33b85a13da7f920047c3b8c49f9e57f78468d9938bfabde87
    - id: api-error-handler
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [102, 105]
      symbol: install._api_error
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:0d58d01581214ff81d908b60c003a96ae3afa7e54d7b9da081ec156661f47a75
  confidence: high
---

Handlers raise `ApiError(status, code, message)`, which `install` renders as `{"error": {"code", "message"}}`; a code, once shipped, is never renamed.[^api-error][^api-error-handler]

What to do: preserve the error envelope and existing code values when adding failures.

[^api-error]: [ApiError](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L27-L32)
[^api-error-handler]: [_api_error handler](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L102-L105)
