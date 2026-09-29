---
title: Errors
description: Every error has an HTTP status and a stable code you can branch on.
keywords:
- API errors
- error codes
updated: '2026-09-29'
---

## The error object

```json Response · 422
{
  "error": {
    "code": "no_calling_line",
    "message": "Agent dispatch-followup has no calling line, so this campaign cannot upload contacts or dial.",
    "request_id": "req_2b9x"
  }
}
```

Quote `request_id` when you contact support.

## Status codes

| Status | Meaning |
| --- | --- |
| 200, 201, 202 | Success. 202 means accepted and still running, such as a queued call. |
| 400 | The request is malformed. |
| 401 | Missing or invalid key. |
| 403 | The key cannot do this. |
| 404 | Not found in this workspace. |
| 409 | Conflicts with the current state. |
| 422 | Understood, but cannot be done as asked. |
| 429 | Too many requests. See [Rate limits](limits). |
| 500, 503 | Our side. Retry with backoff. |

## Common codes

| Code | Status | What to do |
| --- | --- | --- |
| invalid_request | 400 | Check the fields named in the message. |
| unauthorized | 401 | Check the header and the key. |
| forbidden | 403 | Ask for access. |
| not_found | 404 | Check the id and the workspace. |
| contacts_exist | 409 | This campaign already has a list. Create a new campaign. |
| already_dialled | 409 | The list has already been dialled. |
| no_calling_line | 422 | Set a calling line on the agent. |
| missing_required_mapping | 422 | Map every required input. |
| undeclared_tokens | 422 | Declare the listed tokens as inputs, or remove them. |
| invalid_phone | 422 | Use E.164 or a 10-digit Indian number. |
| rate_limited | 429 | Wait for `Retry-After`, then retry. |
| server_error | 500 | Retry with backoff. |

## What to retry

Retry `429`, `500` and `503` with exponential backoff and jitter. Do not retry other `4xx` errors without changing the request.

<Warning title="Placing calls is not idempotent yet">`POST /v1/calls` has no idempotency key. If it times out, list recent calls for that number before you retry, so the same person is not called twice. Pass your own reference in `metadata` to make that lookup easy.</Warning>
