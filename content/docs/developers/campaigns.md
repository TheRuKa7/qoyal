---
title: Campaigns
description: A campaign is one agent run against one list. Create it, upload contacts (first as a dry run to check the column mapping), and read results as calls finish.
sidebarTitle: Campaigns API
keywords:
- campaigns API
updated: '2026-09-29'
---

<Endpoint method="POST" path="/v1/campaigns" title="Create a campaign" id="create-campaign">

Creates an empty campaign for an agent. It is named after the agent and the time.

<Params title="Body">
<ParamField name="agent" type="string" required></ParamField>
<ParamField name="direction" type="string">`outbound` (default) or `inbound`.</ParamField>
<ParamField name="description" type="string">Which list this is.</ParamField>
<ParamField name="metadata" type="object">Your own references.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/campaigns" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "dispatch-followup",
    "direction": "outbound",
    "description": "Week 39 open POs"
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/campaigns",
    headers=HEADERS,
    json={
  "agent": "dispatch-followup",
  "direction": "outbound",
  "description": "Week 39 open POs"
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "agent": "dispatch-followup",
    "direction": "outbound",
    "description": "Week 39 open POs"
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
  "id": "cmp_7Hq2",
  "name": "Dispatch follow-up - 2026-09-25 10:00",
  "agent": "dispatch-followup",
  "direction": "outbound",
  "description": "Week 39 open POs",
  "status": "created",
  "source": "api",
  "contacts_count": 0,
  "dialled_count": 0,
  "captured_count": 0,
  "created_at": "2026-09-25T10:00:03Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns" title="List campaigns" id="list-campaigns">

Newest first.

<Params title="Query parameters">
<ParamField name="agent" type="string"></ParamField>
<ParamField name="status" type="string">`created`, `ready`, `running`, `completed`, `failed`.</ParamField>
<ParamField name="limit" type="integer"></ParamField>
<ParamField name="cursor" type="string"></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns`, {
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
      "id": "cmp_7Hq2",
      "name": "Dispatch follow-up - 2026-09-25 10:00",
      "agent": "dispatch-followup",
      "direction": "outbound",
      "description": "Week 39 open POs",
      "status": "running",
      "source": "api",
      "contacts_count": 148,
      "dialled_count": 120,
      "captured_count": 96,
      "created_at": "2026-09-25T10:00:03Z"
    }
  ],
  "next_cursor": null
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns/{campaign_id}" title="Retrieve a campaign" id="get-campaign">

Counts and status.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns/cmp_7Hq2" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns/cmp_7Hq2",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2`, {
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
  "id": "cmp_7Hq2",
  "name": "Dispatch follow-up - 2026-09-25 10:00",
  "agent": "dispatch-followup",
  "direction": "outbound",
  "description": "Week 39 open POs",
  "status": "running",
  "source": "api",
  "contacts_count": 148,
  "dialled_count": 120,
  "captured_count": 96,
  "created_at": "2026-09-25T10:00:03Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="POST" path="/v1/campaigns/{campaign_id}/contacts" title="Upload contacts" id="upload-contacts">

Uploads the list. With `dry_run=true` nothing is stored: you get the proposed column mapping and sample values to check. Without it, the list is stored and dialling starts.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<Params title="Body">
<ParamField name="file" type="file" required>.xlsx or .csv, one row per contact.</ParamField>
<ParamField name="dry_run" type="boolean">Default `false`.</ParamField>
<ParamField name="mapping" type="object">Input key to column index, as confirmed from a dry run. Omit to accept the proposal.</ParamField>
</Params>

<Note>
**Note**

A campaign takes one upload. A second upload returns `409 contacts_exist`; create a new campaign for another list. Rows that fail validation are stored with status `input_validation_failed` and are not dialled.
</Note>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/campaigns/cmp_7Hq2/contacts" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -F "file=@open_pos.xlsx" \
  -F "dry_run=true"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/campaigns/cmp_7Hq2/contacts",
    headers=HEADERS,
    files={"file": open("open_pos.xlsx", "rb")},
    data={"dry_run": "true"},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
import fs from "node:fs";
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const form = new FormData();
form.append("file", new Blob([await fs.promises.readFile("open_pos.xlsx")]), "open_pos.xlsx");
form.append("dry_run", "true");
const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/contacts`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}` },
  body: form,
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "dry_run": true,
  "sheet_headers": [
    "Contact no.",
    "Supplier",
    "PO No",
    "Qty"
  ],
  "mapping": [
    {
      "input": "phone",
      "column": 0,
      "header": "Contact no.",
      "matched_by": "name",
      "required": true
    },
    {
      "input": "supplier_name",
      "column": 1,
      "header": "Supplier",
      "matched_by": "name",
      "required": true
    },
    {
      "input": "po_number",
      "column": 2,
      "header": "PO No",
      "matched_by": "name",
      "required": true
    },
    {
      "input": "open_qty",
      "column": 3,
      "header": "Qty",
      "matched_by": "position",
      "required": false
    }
  ],
  "sample_rows": [
    [
      "9876543210",
      "Mehta Packaging",
      "4471",
      "14"
    ]
  ],
  "rows": 148
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="POST" path="/v1/campaigns/{campaign_id}/start" title="Start dialling" id="start-campaign">

Dials a stored list that has not been dialled. Real numbers are called; this cannot be undone.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/campaigns/cmp_7Hq2/start" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/campaigns/cmp_7Hq2/start",
    headers=HEADERS,
    json={},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/start`, {
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
  "campaign_id": "cmp_7Hq2",
  "dialled": 148,
  "status": "running"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns/{campaign_id}/contacts" title="List contacts" id="list-contacts">

Every row with its call status.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<Params title="Query parameters">
<ParamField name="status" type="string">`pending`, `dialled`, `captured`, `no_outputs`, `disconnected_early`, `input_validation_failed`.</ParamField>
<ParamField name="limit" type="integer"></ParamField>
<ParamField name="cursor" type="string"></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns/cmp_7Hq2/contacts" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns/cmp_7Hq2/contacts",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/contacts`, {
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
      "primary_id": "4471",
      "name": "Mehta Packaging",
      "phone": "+919876543210",
      "status": "captured",
      "call_id": "call_8f2k1q"
    },
    {
      "primary_id": "5208",
      "name": "R K Castings",
      "phone": "+919811122233",
      "status": "input_validation_failed",
      "validation_error": "open_qty is not a number"
    }
  ],
  "next_cursor": null
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns/{campaign_id}/contacts/{primary_id}" title="Retrieve a contact" id="get-contact">

One contact’s outputs, transcript and recording availability.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
<ParamField name="primary_id" type="string" required>The value of the agent’s primary id input.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns/cmp_7Hq2/contacts/4471" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns/cmp_7Hq2/contacts/4471",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/contacts/4471`, {
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
  "primary_id": "4471",
  "status": "captured",
  "outputs": {
    "status": "PARTIAL",
    "dispatch_date": "2026-09-28",
    "qty_ready": 10
  },
  "call_id": "call_8f2k1q",
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
  "recording_available": true
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns/{campaign_id}/results" title="Retrieve results" id="get-results">

One row per contact with every output as a field. Ask for `format=csv` or `xlsx` to download a file.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<Params title="Query parameters">
<ParamField name="format" type="string">`json` (default), `csv` or `xlsx`.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns/cmp_7Hq2/results" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns/cmp_7Hq2/results",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/results`, {
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
      "primary_id": "4471",
      "name": "Mehta Packaging",
      "phone": "+919876543210",
      "status": "captured",
      "captured_at": "2026-09-25T10:06:04Z",
      "call_id": "call_8f2k1q",
      "outputs": {
        "status": "PARTIAL",
        "dispatch_date": "2026-09-28",
        "qty_ready": 10
      }
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/campaigns/{campaign_id}/export" title="Export transcripts and audio" id="export-campaign">

Every transcript and recording from the campaign in one archive.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<Params title="Query parameters">
<ParamField name="include" type="string">`transcripts`, `audio` or both, comma separated.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/campaigns/cmp_7Hq2/export?include=transcripts,audio" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -o campaign.zip
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/campaigns/cmp_7Hq2/export",
    headers=HEADERS,
    params={"include": "transcripts,audio"},
)
res.raise_for_status()
open("campaign.zip", "wb").write(res.content)
```
```javascript Node.js
import fs from "node:fs";
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2/export?include=transcripts,audio`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
await fs.promises.writeFile("campaign.zip", Buffer.from(await res.arrayBuffer()));
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```text
Binary .zip file
```
</ResponseExample>

</Endpoint>

<Endpoint method="DELETE" path="/v1/campaigns/{campaign_id}" title="Delete a campaign" id="delete-campaign">

Deletes the campaign, its contacts and every captured result. This cannot be undone.

<Params title="Path parameters">
<ParamField name="campaign_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X DELETE "$ECHO_API/v1/campaigns/cmp_7Hq2" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.delete(
    f"{API}/v1/campaigns/cmp_7Hq2",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/campaigns/cmp_7Hq2`, {
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
  "id": "cmp_7Hq2",
  "deleted": true
}
```
</ResponseExample>

</Endpoint>
