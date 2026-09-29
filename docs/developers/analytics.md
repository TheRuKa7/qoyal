---
title: Analytics
description: The same funnel you see on the dashboard, for your own reports.
sidebarTitle: Analytics API
keywords:
- call analytics API
updated: '2026-09-29'
---

<Note>
**Preview**

Part of the developer preview. Fields may change before general availability.
</Note>

<Endpoint method="GET" path="/v1/metrics" title="Retrieve the funnel" id="get-metrics">

Counts for a period, from uploaded rows to confirmed outcomes.

<Params title="Query parameters">
<ParamField name="days" type="integer">Look-back window. Default 30.</ParamField>
<ParamField name="agent" type="string"></ParamField>
<ParamField name="campaign_id" type="string"></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/metrics?days=30" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/metrics",
    headers=HEADERS,
    params={"days": "30"},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/metrics?days=30`, {
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
  "funnel": {
    "planned": 2480,
    "will_dial": 2410,
    "blocked": 70,
    "attempted": 2390,
    "connected": 1697,
    "connected_rate": 0.71,
    "achieved": 1086,
    "achieved_rate": 0.64,
    "inconclusive": 153,
    "inconclusive_rate": 0.09,
    "callbacks_open": 112,
    "tech_failures": 14
  },
  "calls": {
    "total": 2390,
    "avg_duration_seconds": 108,
    "avg_turns": 6.2
  }
}
```
</ResponseExample>

</Endpoint>
