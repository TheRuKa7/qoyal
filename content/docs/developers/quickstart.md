---
title: Quickstart
description: Check your pilot API key, place a call to your own phone, and read back what the agent captured.
sidebarTitle: API quickstart
keywords:
- voice API quickstart
- place a call by API
updated: '2026-09-29'
---

## 1. Get a key

Your account team issues an API key and your base URL during the pilot. Keep the key on your server. Never put it in a browser, an app or a repository.

<Warning title="Calls are real">There is no sandbox yet, and `ek_live_` keys dial real numbers. Place test calls to your own phone.</Warning>

## 2. Set your environment

```bash .env
ECHO_API=https://<your base URL>
ECHO_API_KEY=ek_live_...
```

## 3. Check the key

Agent ids are derived from the agent name, such as `dispatch-followup` or `wismo`. The list below shows them.

List the agents your team has built. A `200` with a list means you are ready.

<CodeGroup title="List agents">
```bash cURL
curl "$ECHO_API/v1/agents" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>

## 4. Place a call

Pick an agent id from the list and call your own phone. `context` fills the agent’s inputs for this call.

<CodeGroup title="Place a call">
```bash cURL
curl -X POST "$ECHO_API/v1/calls" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "wismo",
    "to": "+919876543210",
    "context": {
      "customer_name": "Asha",
      "order_id": "88213"
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
  "agent": "wismo",
  "to": "+919876543210",
  "context": {
    "customer_name": "Asha",
    "order_id": "88213"
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
    "agent": "wismo",
    "to": "+919876543210",
    "context": {
      "customer_name": "Asha",
      "order_id": "88213"
    }
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>

```json Response
{
  "id": "call_8f2k1q",
  "status": "queued"
}
```

## 5. Read the outcome

Answer the phone and talk to the agent. When the call ends, fetch it. `outputs` holds what the agent captured.

<CodeGroup title="Retrieve a call">
```bash cURL
curl "$ECHO_API/v1/calls/call_8f2k1q" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/calls/call_8f2k1q",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls/call_8f2k1q`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>

Polling is fine for a test. In production, [subscribe to webhooks](webhooks) instead.

## Next

- [Run a campaign from code](guide-campaign)
- [Learn the objects](objects)
- [Build a better agent in the dashboard](../platform/agents)
