---
type: convention
title: Every request carries one x-correlation-id end to end
description: Each service accepts x-correlation-id (or makes one), logs it, returns it, and forwards it on every outbound call.
tags: [core, observability, logging]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: correlation-middleware
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L18-L25
  - id: json-formatter
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L34-L48
  - id: outbound-headers
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L62-L65
  - id: dispatch
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L67-L93
  - id: correlation-test
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/tests/test_platform.py#L8-L17
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/correlation-id-propagation.md
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/observability.py, app/main.py]
  citations:
    - id: correlation-middleware
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [18, 25]
      symbol: CORRELATION_HEADER and _VALID_CORRELATION
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:2b1bf1dea5b96886da9cc887629a999cc8e1ffe41086fa838018e383e99b305f
    - id: json-formatter
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [34, 48]
      symbol: JsonFormatter.format
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:33d4dc436af5bc4c5a6ab80c0abf80b27a9564118bebb3eb6ab8e751a49fa597
    - id: outbound-headers
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [62, 65]
      symbol: outbound_headers
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:a8c9ed01285b262debce27aefa6e9f36ca6e03d5408ce0e17cf2bfc241646e53
    - id: dispatch
      repo: github:chfields/wmd-notification-service
      path: app/observability.py
      lines: [67, 93]
      symbol: _Observability.dispatch
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:b3a1e1d78ecfcf2235c0f57a5385b54f1b20f1872a86274611bfa4d59c4d67dc
    - id: correlation-test
      repo: github:chfields/wmd-notification-service
      path: tests/test_platform.py
      lines: [8, 17]
      symbol: test_echoes_a_valid_correlation_id_and_generates_one_otherwise
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:0daa13cea72b4a7d5379c5a8e85fc645b97e747f35b6de117ae7b2765c1c1680
  confidence: high
---

The middleware accepts a valid `x-correlation-id` (else generates a UUID), stores it in a contextvar that every JSON log line includes, and returns it on the response; any future outbound HTTP call must pass `outbound_headers()`.[^correlation-middleware][^json-formatter][^outbound-headers][^dispatch][^correlation-test]

What to do: forward the current correlation header on every outbound service call.

[^correlation-middleware]: [correlation constants](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L18-L25)
[^json-formatter]: [JsonFormatter.format](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L34-L48)
[^outbound-headers]: [outbound_headers](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L62-L65)
[^dispatch]: [_Observability.dispatch](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/app/observability.py#L67-L93)
[^correlation-test]: [correlation platform test](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/tests/test_platform.py#L8-L17)
