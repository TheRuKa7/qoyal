---
title: Webhooks API
description: Get each outcome the moment it lands instead of polling. Register an endpoint, then verify every delivery.
sidebarTitle: Webhook endpoints
keywords:
- webhook endpoints API
- webhook signature
updated: '2026-09-29'
---

<Note>
**Preview**

Part of the developer preview. Fields may change before general availability.
</Note>

<Endpoint method="POST" path="/v1/webhooks" title="Register an endpoint" id="create-webhook">

Subscribes a URL to events. The response includes the signing secret, shown once.

<Params title="Body">
<ParamField name="url" type="string" required>HTTPS endpoint.</ParamField>
<ParamField name="events" type="array" required>Any of `call.completed`, `call.analyzed`, `contact.captured`, `campaign.completed`.</ParamField>
<ParamField name="description" type="string"></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/webhooks" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://erp.example.com/echo/outcomes",
    "events": [
      "contact.captured",
      "campaign.completed"
    ]
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/webhooks",
    headers=HEADERS,
    json={
  "url": "https://erp.example.com/echo/outcomes",
  "events": [
    "contact.captured",
    "campaign.completed"
  ]
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/webhooks`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "url": "https://erp.example.com/echo/outcomes",
    "events": [
      "contact.captured",
      "campaign.completed"
    ]
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="201">
```json
{
  "id": "wh_31k",
  "url": "https://erp.example.com/echo/outcomes",
  "events": [
    "contact.captured",
    "campaign.completed"
  ],
  "secret": "whsec_...",
  "created_at": "2026-09-25T09:00:00Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/webhooks" title="List endpoints" id="list-webhooks">

Your registered endpoints. Secrets are not returned.

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/webhooks" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/webhooks",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/webhooks`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "data": [
    {
      "id": "wh_31k",
      "url": "https://erp.example.com/echo/outcomes",
      "events": [
        "contact.captured",
        "campaign.completed"
      ]
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/webhooks/{webhook_id}/deliveries" title="List deliveries" id="list-deliveries">

Recent deliveries with status codes and attempts, for debugging.

<Params title="Path parameters">
<ParamField name="webhook_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/webhooks/wh_31k/deliveries" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/webhooks/wh_31k/deliveries",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/webhooks/wh_31k/deliveries`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "data": [
    {
      "event_id": "evt_5c2",
      "type": "contact.captured",
      "status": 200,
      "attempts": 1,
      "delivered_at": "2026-09-25T10:06:05Z"
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="DELETE" path="/v1/webhooks/{webhook_id}" title="Remove an endpoint" id="delete-webhook">

Stops deliveries to this URL.

<Params title="Path parameters">
<ParamField name="webhook_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X DELETE "$ECHO_API/v1/webhooks/wh_31k" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.delete(
    f"{API}/v1/webhooks/wh_31k",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/webhooks/wh_31k`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "id": "wh_31k",
  "deleted": true
}
```
</ResponseExample>

</Endpoint>
