---
title: Calls
description: A call is one conversation with one person. Place single calls from your own events, such as a new order, and read back transcripts, outcomes and recordings for any call.
sidebarTitle: Calls API
keywords:
- calls API
- outbound call API
updated: '2026-09-29'
---

<Endpoint method="POST" path="/v1/calls" title="Place a call" id="create-call">

Dials one number with an agent. Values in `context` fill the agent’s inputs for this call only.

<Params title="Body">
<ParamField name="agent" type="string" required>Agent id.</ParamField>
<ParamField name="to" type="string" required>Number to call. E.164, or 10 digits for India (+91 is added).</ParamField>
<ParamField name="context" type="object">Input values by key. Missing required inputs are passed as “(not provided)”.</ParamField>
<ParamField name="voice" type="string">Override the agent’s voice for this call.</ParamField>
<ParamField name="metadata" type="object">Your own references, returned on the call and in webhooks.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/calls" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "dispatch-followup",
    "to": "+919876543210",
    "context": {
      "supplier_name": "Mehta Packaging",
      "po_number": "4471",
      "open_qty": 14
    },
    "metadata": {
      "erp_line_id": "L-44713"
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
  "agent": "dispatch-followup",
  "to": "+919876543210",
  "context": {
    "supplier_name": "Mehta Packaging",
    "po_number": "4471",
    "open_qty": 14
  },
  "metadata": {
    "erp_line_id": "L-44713"
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
    "agent": "dispatch-followup",
    "to": "+919876543210",
    "context": {
      "supplier_name": "Mehta Packaging",
      "po_number": "4471",
      "open_qty": 14
    },
    "metadata": {
      "erp_line_id": "L-44713"
    }
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="202">
```json
{
  "id": "call_8f2k1q",
  "status": "queued"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/calls/{call_id}" title="Retrieve a call" id="get-call">

Returns the call with its context, reported outputs, transcript, recording link and analysis when it exists.

<Params title="Path parameters">
<ParamField name="call_id" type="string" required></ParamField>
</Params>

<Note>
**Note**

`status` is `queued`, `in_progress` or `completed`. A completed call with `turns: 0` was answered but had no audio.
</Note>

<RequestExample>
<CodeGroup>
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
</RequestExample>
<ResponseExample status="200">
```json
{
  "id": "call_8f2k1q",
  "agent": "dispatch-followup",
  "campaign_id": "cmp_7Hq2",
  "direction": "outbound",
  "to": "+919876543210",
  "status": "completed",
  "started_at": "2026-09-25T10:04:12Z",
  "duration_seconds": 112,
  "turns": 14,
  "context": {
    "supplier_name": "Mehta Packaging",
    "po_number": "4471",
    "open_qty": 14
  },
  "outputs": {
    "status": "PARTIAL",
    "dispatch_date": "2026-09-28",
    "qty_ready": 10
  },
  "summary": "Supplier confirmed 10 of 14 cartons for 28 Sep.",
  "transcript": [
    {
      "role": "agent",
      "text": "Namaste, PO 4471: 14 cartons. Dispatch kab tak ho jayega?"
    },
    {
      "role": "contact",
      "text": "28 ko, par abhi sirf 10 ready hain."
    }
  ],
  "recording_url": "$ECHO_API/v1/calls/call_8f2k1q/recording",
  "analysis": null
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/calls" title="List calls" id="list-calls">

The call log, newest first, with the same filters as the dashboard.

<Params title="Query parameters">
<ParamField name="agent" type="string"></ParamField>
<ParamField name="campaign_id" type="string"></ParamField>
<ParamField name="q" type="string">Search by name or number.</ParamField>
<ParamField name="since" type="timestamp">ISO 8601.</ParamField>
<ParamField name="until" type="timestamp"></ParamField>
<ParamField name="min_duration" type="integer">Seconds.</ParamField>
<ParamField name="max_duration" type="integer">Seconds.</ParamField>
<ParamField name="limit" type="integer">1 to 100.</ParamField>
<ParamField name="cursor" type="string"></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/calls?agent=dispatch-followup&since=2026-09-18T00:00:00Z&limit=50" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/calls",
    headers=HEADERS,
    params={"agent": "dispatch-followup", "since": "2026-09-18T00:00:00Z", "limit": "50"},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls?agent=dispatch-followup&since=2026-09-18T00:00:00Z&limit=50`, {
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
      "id": "call_8f2k1q",
      "agent": "dispatch-followup",
      "to": "+919876543210",
      "status": "completed",
      "started_at": "2026-09-25T10:04:12Z",
      "duration_seconds": 112,
      "turns": 14,
      "summary": "Supplier confirmed 10 of 14 cartons for 28 Sep."
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOjUwfQ"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/calls/live" title="List live calls" id="live-calls">

Calls in progress right now, each with the transcript so far.

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/calls/live" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/calls/live",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls/live`, {
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
      "id": "call_9a1",
      "agent": "wismo",
      "to": "+919123456789",
      "started_at": "2026-09-25T11:20:02Z",
      "transcript": [
        {
          "role": "agent",
          "text": "Hi, this is Meera from support..."
        }
      ]
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/calls/{call_id}/recording" title="Download a recording" id="get-recording">

The call audio.

<Params title="Path parameters">
<ParamField name="call_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/calls/call_8f2k1q/recording" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -o call.wav
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/calls/call_8f2k1q/recording",
    headers=HEADERS,
)
res.raise_for_status()
open("call.wav", "wb").write(res.content)
```
```javascript Node.js
import fs from "node:fs";
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls/call_8f2k1q/recording`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
await fs.promises.writeFile("call.wav", Buffer.from(await res.arrayBuffer()));
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```text
Binary audio file
```
</ResponseExample>

</Endpoint>

<Endpoint method="POST" path="/v1/calls/{call_id}/analyze" title="Analyse a call" id="analyze-call">

Runs or re-runs analysis on the transcript and saves it on the call.

<Params title="Path parameters">
<ParamField name="call_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/calls/call_8f2k1q/analyze" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/calls/call_8f2k1q/analyze",
    headers=HEADERS,
    json={},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls/call_8f2k1q/analyze`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({}),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "call_id": "call_8f2k1q",
  "executive_summary": "Supplier confirmed 10 of 14 cartons for 28 Sep; remaining 4 depend on raw material.",
  "priority": "medium",
  "issue_resolved": "partial",
  "action_items": [
    "Update PO 4471 line 3 to 10 cartons, 28 Sep",
    "Follow up on 27 Sep"
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/calls/export" title="Export the call log" id="export-calls">

The filtered call log as a spreadsheet. Takes the same filters as [List calls](#list-calls).

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/calls/export?since=2026-09-01T00:00:00Z" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -o calls.xlsx
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/calls/export",
    headers=HEADERS,
    params={"since": "2026-09-01T00:00:00Z"},
)
res.raise_for_status()
open("calls.xlsx", "wb").write(res.content)
```
```javascript Node.js
import fs from "node:fs";
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/calls/export?since=2026-09-01T00:00:00Z`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
await fs.promises.writeFile("calls.xlsx", Buffer.from(await res.arrayBuffer()));
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```text
Binary .xlsx file
```
</ResponseExample>

</Endpoint>
