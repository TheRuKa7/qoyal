---
title: Call on an event
description: Place a single call the moment something happens in your system, and write the answer back.
keywords:
- trigger a call from an event
- ERP event call
updated: '2026-09-29'
status: soon
soon_note: The public REST API is not open yet. Endpoints and fields may change before release. Ask your account team for early access.
---

## When to use it

Use single calls for work that arrives one item at a time: a new cash on delivery order, a PO line that just went late, an invoice past due. For a list you already have, [run a campaign](guide-campaign).

## Map your data to inputs

Every key in `context` must match an input on the agent. Read the agent to see them:

<CodeGroup title="Retrieve an agent">
```bash cURL
curl "$ECHO_API/v1/agents/cod-confirmation" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents/cod-confirmation",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/cod-confirmation`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>

Values marked `share_on_call: false` are given to the agent but never spoken. Put internal ids there.

## Place the call

<CodeGroup title="Place a call">
```bash cURL
curl -X POST "$ECHO_API/v1/calls" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "cod-confirmation",
    "to": "9876543210",
    "context": {
      "customer_name": "Asha",
      "order_id": "88213",
      "amount": 1499
    },
    "metadata": {
      "order_ref": "SO-88213"
    }
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/calls",
    headers=HEADERS,
    json={
  "agent": "cod-confirmation",
  "to": "9876543210",
  "context": {
    "customer_name": "Asha",
    "order_id": "88213",
    "amount": 1499
  },
  "metadata": {
    "order_ref": "SO-88213"
  }
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "agent": "cod-confirmation",
    "to": "9876543210",
    "context": {
      "customer_name": "Asha",
      "order_id": "88213",
      "amount": 1499
    },
    "metadata": {
      "order_ref": "SO-88213"
    }
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>

Ten-digit Indian numbers get +91. Keep `metadata` for your own references; it comes back on the call and in every webhook.

## Write the outcome back

Subscribe to `call.completed` and update your system from `data.outputs`, matched by `data.metadata`. See [Webhooks](webhooks).

## Tips

- Respect calling windows in your own scheduler: queue events that arrive at night for the morning.
- Check the outcome’s `status` output, not only the call status. A completed call can still end in `CALL_BACK`.
- Test the agent in the [call console](../platform/testing) with the same context first.
