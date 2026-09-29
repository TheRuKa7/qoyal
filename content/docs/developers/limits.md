---
title: Rate limits and pagination
description: How much you can ask for, and how to page through long lists.
sidebarTitle: Rate limits
keywords:
- API rate limits
updated: '2026-09-29'
status: soon
soon_note: The public REST API is not open yet. Endpoints and fields may change before release. Ask your account team for early access.
---

## Rate limits

Limits are set per workspace. Every response carries the current state: the limit, what is left, and when the window resets as a Unix time in seconds.

```text Headers
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 587
X-RateLimit-Reset: 1790330820
```

Over the limit you get `429 rate_limited` with a `Retry-After` header in seconds. Your account team can raise limits for your volume.

## Concurrent calls

How many calls run at once depends on your calling lines. Extra calls wait in a queue and start as lines free up, so you can submit a large list at once. Queued calls are placed only within the calling hours that apply to the campaign.

## Pagination

List endpoints take `limit` (1 to 100) and `cursor`, and return `next_cursor`. Keep requesting until it is `null`.

```python Python
import os, requests

API = os.environ["ECHO_API"]
H = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

def handle(calls):
    for call in calls:
        print(call["id"], call["status"])

cursor = None
while True:
    page = requests.get(f"{API}/v1/calls", headers=H,
                        params={"limit": 100, "cursor": cursor}).json()
    handle(page["data"])
    cursor = page["next_cursor"]
    if not cursor:
        break
```
