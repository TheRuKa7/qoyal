---
title: Authentication
description: Every request carries your API key as a bearer token.
keywords:
- API key authentication
- bearer token
updated: '2026-09-25'
---

## The header

```text HTTP
Authorization: Bearer ek_live_...
Content-Type: application/json
```

Requests without a valid key return `401 unauthorized`. Keys are tied to one workspace, so every request acts on that workspace’s agents, campaigns and calls.

## Managing keys

- Keys are issued and revoked by your account team during the preview.
- Use separate keys for test and production systems, so you can rotate one without touching the other.
- To rotate: ask for a new key, deploy it, then revoke the old one.

## What a key can do

| Area | Access |
| --- | --- |
| Agents | Read, create, update, delete |
| Calls | Place, read, analyse, download |
| Campaigns | Create, upload, start, read, delete |
| Analytics | Read |
| People and access | Dashboard only |

## Keeping keys safe

- Store keys in a secret manager or environment variables, never in code.
- Call Echo from your backend. Browsers and mobile apps should call your backend, not Echo.
- If a key leaks, ask for it to be revoked immediately. Revocation takes effect on the next request.
