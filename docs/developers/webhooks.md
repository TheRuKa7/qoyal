---
title: Webhooks
description: Receive outcomes as they happen. Verify each delivery, reply fast, and handle retries.
sidebarTitle: Receive outcomes by webhook
keywords:
- voice AI webhooks
- call outcome webhook
updated: '2026-09-29'
---

## Events

| Event | Sent when |
| --- | --- |
| `call.completed` | Any call ends, with its outputs. |
| `call.analyzed` | Analysis finishes on a call. |
| `contact.captured` | A campaign contact reports its outputs. |
| `campaign.completed` | A campaign finishes dialling. |

## Payload

Each delivery is a `POST` with a JSON body and these headers:

```text Headers
Content-Type: application/json
X-Echo-Event: contact.captured
X-Echo-Delivery: evt_5c2
X-Echo-Signature: t=1790330765,v1=5f2b...
```

```json Body
{
  "id": "evt_5c2",
  "type": "contact.captured",
  "created_at": "2026-09-25T10:06:05Z",
  "data": {
    "campaign_id": "cmp_7Hq2",
    "primary_id": "4471",
    "status": "captured",
    "call_id": "call_8f2k1q",
    "outputs": {
      "status": "PARTIAL",
      "dispatch_date": "2026-10-06",
      "qty_ready": 10
    },
    "metadata": {}
  }
}
```

`data.status` is the contact's state in the campaign (see [Core objects](objects)). `data.outputs` holds the values your agent captured, so `outputs.status` is your own output field, such as `PARTIAL`. `primary_id` is the value of the agent's primary id input, here the PO number.

## Verify the signature

The signature is an HMAC SHA-256 of `timestamp.body` with your endpoint’s secret. Verify it on the raw body, before parsing, and reject old timestamps.

<CodeGroup title="Verify">
```python Python
import hmac, hashlib, time

def verify(secret: str, header: str, body: bytes, tolerance=300) -> bool:
    parts = dict(p.split("=", 1) for p in header.split(","))
    ts, sig = int(parts["t"]), parts["v1"]
    if abs(time.time() - ts) > tolerance:
        return False  # too old: possible replay
    expected = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
```
```javascript Node.js
import crypto from "node:crypto";

export function verify(secret, header, rawBody, tolerance = 300) {
  const parts = Object.fromEntries(header.split(",").map((p) => p.split("=")));
  const ts = Number(parts.t);
  if (Math.abs(Date.now() / 1000 - ts) > tolerance) return false;
  const expected = crypto.createHmac("sha256", secret)
    .update(`${ts}.`).update(rawBody).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(parts.v1));
}
```
</CodeGroup>

## Respond and retry

- Reply with any `2xx` within 10 seconds. Do the real work after replying.
- Failed deliveries are retried with increasing delays. The same event can arrive more than once: use `id` to ignore duplicates. Ask your account team for the retry schedule on your workspace.
- Events can arrive out of order. Use `created_at`, or read the latest state from the API.
- See recent deliveries and their status codes with [List deliveries](webhooks-api#list-deliveries).

## Manage endpoints

Register, list and remove endpoints with the [Webhooks API](webhooks-api).
