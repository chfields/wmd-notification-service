---
type: decision
title: Only merged main reaches staging
description: deploy.sh builds every service from its origin/main in a clean checkout, so staging never runs unreviewed code.
tags: [core, deploy, ci]
status: stable
generated:
  by: wmd-notification-builder/gpt-5.6-terra
  at: 2026-10-04T15:29:48Z
sources:
  - id: dockerfile
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/Dockerfile#L1-L11
  - id: test-workflow
    url: https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/.github/workflows/test.yml#L1-L28
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/only-merged-code-reaches-staging.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [Dockerfile, .github/workflows/**, requirements.txt]
  citations:
    - id: dockerfile
      repo: github:chfields/wmd-notification-service
      path: Dockerfile
      lines: [1, 11]
      symbol: Dockerfile
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:1872275d6b7dd1b4610c0cff3e812abbece7998217ba51a84e1f855cb3561c99
    - id: test-workflow
      repo: github:chfields/wmd-notification-service
      path: .github/workflows/test.yml
      lines: [1, 28]
      symbol: test workflow
      sha: 3fa9595165439ca1685409ed2aa9437c37f0b8fd
      spanHash: sha256:7cef579bba2a7f44dbd10a7ffedabc61710997d310718be8b13ee5536007053d
  confidence: medium
---

Staging runs the image built from this repository's merged main, so a change reaches staging only by merging a reviewed PR that passes CI; the Dockerfile must build from a clean checkout with nothing local.[^dockerfile][^test-workflow]

What to do: retain the clean image inputs and CI coverage for pull requests and `main`.

[^dockerfile]: [Dockerfile](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/Dockerfile#L1-L11)
[^test-workflow]: [test workflow](https://github.com/chfields/wmd-notification-service/blob/3fa9595165439ca1685409ed2aa9437c37f0b8fd/.github/workflows/test.yml#L1-L28)
