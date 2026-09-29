---
title: Agents
description: Read, clone and update voice agents by API, including prompts, voice, calling line and variables, so prompts can live in version control.
sidebarTitle: Agents API
keywords:
- agents API
updated: '2026-09-29'
---

<Endpoint method="GET" path="/v1/agents" title="List agents" id="list-agents">

Returns the agents in your workspace, newest first.

<Params title="Query parameters">
<ParamField name="limit" type="integer">1 to 100. Default 25.</ParamField>
<ParamField name="cursor" type="string">The `next_cursor` from the previous page.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/agents?limit=25" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents",
    headers=HEADERS,
    params={"limit": "25"},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents?limit=25`, {
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
      "id": "dispatch-followup",
      "name": "Dispatch follow-up",
      "inputs_count": 4,
      "outputs_count": 3,
      "primary_id": "po_number",
      "calling_line": "ops-outbound"
    }
  ],
  "next_cursor": null
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/agents/{agent_id}" title="Retrieve an agent" id="get-agent">

Returns one agent with its inputs, outputs and settings. The prompt is returned by [Retrieve the prompt](#get-prompt).

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required>The agent id, such as `dispatch-followup`.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/agents/dispatch-followup" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents/dispatch-followup",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup`, {
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
  "id": "dispatch-followup",
  "name": "Dispatch follow-up",
  "description": "Confirms dispatch dates on open PO lines",
  "voice": null,
  "calling_line": "ops-outbound",
  "primary_id": "po_number",
  "inputs": [
    {
      "key": "supplier_name",
      "type": "string",
      "transform": null,
      "sample": "Mehta Packaging",
      "share_on_call": true
    },
    {
      "key": "po_number",
      "type": "string",
      "transform": "spell_digits",
      "sample": "4471",
      "share_on_call": true
    },
    {
      "key": "open_qty",
      "type": "number",
      "transform": null,
      "sample": "14",
      "share_on_call": true
    },
    {
      "key": "supplier_code",
      "type": "string",
      "transform": null,
      "sample": "V-20931",
      "share_on_call": false
    }
  ],
  "outputs": [
    {
      "key": "status",
      "label": "Status",
      "type": "enum",
      "options": [
        "CONFIRMED",
        "PARTIAL",
        "NEW_DATE",
        "CALL_BACK"
      ],
      "description": "Outcome after read-back",
      "required": true
    },
    {
      "key": "dispatch_date",
      "label": "Dispatch date",
      "type": "string",
      "options": [],
      "description": "Date confirmed after read-back",
      "required": true
    },
    {
      "key": "qty_ready",
      "label": "Quantity ready",
      "type": "number",
      "options": [],
      "description": "Cartons ready on that date",
      "required": true
    }
  ],
  "created_at": "2026-09-18T10:02:11Z",
  "updated_at": "2026-09-24T16:40:05Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="POST" path="/v1/agents" title="Create an agent" id="create-agent">

Creates an agent. Start blank or copy an existing agent’s prompt, inputs and outputs.

<Params title="Body">
<ParamField name="name" type="string" required>Shown to your team. The id is derived from it.</ParamField>
<ParamField name="description" type="string">What the agent is for.</ParamField>
<ParamField name="copy_from" type="string">Id of an agent to copy.</ParamField>
<ParamField name="calling_line" type="string">Line the agent dials from. Campaigns cannot dial until this is set.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/agents" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "COD confirmation",
    "description": "Confirms cash on delivery orders before dispatch",
    "copy_from": "wismo",
    "calling_line": "cx-outbound"
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/agents",
    headers=HEADERS,
    json={
  "name": "COD confirmation",
  "description": "Confirms cash on delivery orders before dispatch",
  "copy_from": "wismo",
  "calling_line": "cx-outbound"
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents`, {
  method: "POST",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "name": "COD confirmation",
    "description": "Confirms cash on delivery orders before dispatch",
    "copy_from": "wismo",
    "calling_line": "cx-outbound"
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
  "id": "cod-confirmation",
  "name": "COD confirmation",
  "description": "Confirms dispatch dates on open PO lines",
  "voice": null,
  "calling_line": "ops-outbound",
  "primary_id": "po_number",
  "inputs": [
    {
      "key": "supplier_name",
      "type": "string",
      "transform": null,
      "sample": "Mehta Packaging",
      "share_on_call": true
    },
    {
      "key": "po_number",
      "type": "string",
      "transform": "spell_digits",
      "sample": "4471",
      "share_on_call": true
    },
    {
      "key": "open_qty",
      "type": "number",
      "transform": null,
      "sample": "14",
      "share_on_call": true
    },
    {
      "key": "supplier_code",
      "type": "string",
      "transform": null,
      "sample": "V-20931",
      "share_on_call": false
    }
  ],
  "outputs": [
    {
      "key": "status",
      "label": "Status",
      "type": "enum",
      "options": [
        "CONFIRMED",
        "PARTIAL",
        "NEW_DATE",
        "CALL_BACK"
      ],
      "description": "Outcome after read-back",
      "required": true
    },
    {
      "key": "dispatch_date",
      "label": "Dispatch date",
      "type": "string",
      "options": [],
      "description": "Date confirmed after read-back",
      "required": true
    },
    {
      "key": "qty_ready",
      "label": "Quantity ready",
      "type": "number",
      "options": [],
      "description": "Cartons ready on that date",
      "required": true
    }
  ],
  "created_at": "2026-09-18T10:02:11Z",
  "updated_at": "2026-09-24T16:40:05Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="PATCH" path="/v1/agents/{agent_id}" title="Update an agent" id="update-agent">

Changes settings. Each change applies to the next call, with no restart.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required>The agent id.</ParamField>
</Params>

<Params title="Body">
<ParamField name="name" type="string"></ParamField>
<ParamField name="description" type="string"></ParamField>
<ParamField name="voice" type="string">A voice from [options](#list-options). `null` uses the default.</ParamField>
<ParamField name="calling_line" type="string"></ParamField>
<ParamField name="primary_id" type="string">Key of the input that identifies each contact.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X PATCH "$ECHO_API/v1/agents/dispatch-followup" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "voice": "meera",
    "primary_id": "po_number"
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.patch(
    f"{API}/v1/agents/dispatch-followup",
    headers=HEADERS,
    json={
  "voice": "meera",
  "primary_id": "po_number"
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup`, {
  method: "PATCH",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "voice": "meera",
    "primary_id": "po_number"
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "id": "dispatch-followup",
  "name": "Dispatch follow-up",
  "description": "Confirms dispatch dates on open PO lines",
  "voice": null,
  "calling_line": "ops-outbound",
  "primary_id": "po_number",
  "inputs": [
    {
      "key": "supplier_name",
      "type": "string",
      "transform": null,
      "sample": "Mehta Packaging",
      "share_on_call": true
    },
    {
      "key": "po_number",
      "type": "string",
      "transform": "spell_digits",
      "sample": "4471",
      "share_on_call": true
    },
    {
      "key": "open_qty",
      "type": "number",
      "transform": null,
      "sample": "14",
      "share_on_call": true
    },
    {
      "key": "supplier_code",
      "type": "string",
      "transform": null,
      "sample": "V-20931",
      "share_on_call": false
    }
  ],
  "outputs": [
    {
      "key": "status",
      "label": "Status",
      "type": "enum",
      "options": [
        "CONFIRMED",
        "PARTIAL",
        "NEW_DATE",
        "CALL_BACK"
      ],
      "description": "Outcome after read-back",
      "required": true
    },
    {
      "key": "dispatch_date",
      "label": "Dispatch date",
      "type": "string",
      "options": [],
      "description": "Date confirmed after read-back",
      "required": true
    },
    {
      "key": "qty_ready",
      "label": "Quantity ready",
      "type": "number",
      "options": [],
      "description": "Cartons ready on that date",
      "required": true
    }
  ],
  "created_at": "2026-09-18T10:02:11Z",
  "updated_at": "2026-09-24T16:40:05Z"
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/agents/{agent_id}/prompt" title="Retrieve the prompt" id="get-prompt">

Returns the prompt as ordered sections. Sections of kind `inputs` and `outputs` are generated from the variables unless you have overridden their text.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/agents/dispatch-followup/prompt" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents/dispatch-followup/prompt",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/prompt`, {
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
  "sections": [
    {
      "id": "sec_1",
      "title": "Role and goal",
      "kind": "text",
      "enabled": true,
      "body": "You are Riya from the purchase team. Confirm the dispatch date for PO {{po_number}}."
    },
    {
      "id": "sec_2",
      "title": "Call details",
      "kind": "inputs",
      "enabled": true,
      "body": ""
    },
    {
      "id": "sec_3",
      "title": "Outcome reporting",
      "kind": "outputs",
      "enabled": true,
      "body": ""
    }
  ],
  "missing_tokens": []
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="PUT" path="/v1/agents/{agent_id}/prompt" title="Replace the prompt" id="update-prompt">

Replaces all sections. The new prompt is live on the next call for every campaign that uses the agent.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<Params title="Body">
<ParamField name="sections" type="array" required>Ordered list of `{title, body, kind, enabled}`. `kind` is `text`, `inputs` or `outputs`. An empty body on a generated section keeps it following the variables.</ParamField>
</Params>

<Note>
**Note**

If a section uses a `{{token}}` that is not an input, it is listed in `missing_tokens`. Fix these before calling.
</Note>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X PUT "$ECHO_API/v1/agents/dispatch-followup/prompt" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sections": [
      {
        "title": "Role and goal",
        "kind": "text",
        "enabled": true,
        "body": "You are Riya from the purchase team..."
      },
      {
        "title": "Read-back rules",
        "kind": "text",
        "enabled": true,
        "body": "Repeat every date and quantity back. Save only on a clear yes."
      },
      {
        "title": "Call details",
        "kind": "inputs",
        "enabled": true,
        "body": ""
      },
      {
        "title": "Outcome reporting",
        "kind": "outputs",
        "enabled": true,
        "body": ""
      }
    ]
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.put(
    f"{API}/v1/agents/dispatch-followup/prompt",
    headers=HEADERS,
    json={
  "sections": [
    {
      "title": "Role and goal",
      "kind": "text",
      "enabled": True,
      "body": "You are Riya from the purchase team..."
    },
    {
      "title": "Read-back rules",
      "kind": "text",
      "enabled": True,
      "body": "Repeat every date and quantity back. Save only on a clear yes."
    },
    {
      "title": "Call details",
      "kind": "inputs",
      "enabled": True,
      "body": ""
    },
    {
      "title": "Outcome reporting",
      "kind": "outputs",
      "enabled": True,
      "body": ""
    }
  ]
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/prompt`, {
  method: "PUT",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "sections": [
      {
        "title": "Role and goal",
        "kind": "text",
        "enabled": true,
        "body": "You are Riya from the purchase team..."
      },
      {
        "title": "Read-back rules",
        "kind": "text",
        "enabled": true,
        "body": "Repeat every date and quantity back. Save only on a clear yes."
      },
      {
        "title": "Call details",
        "kind": "inputs",
        "enabled": true,
        "body": ""
      },
      {
        "title": "Outcome reporting",
        "kind": "outputs",
        "enabled": true,
        "body": ""
      }
    ]
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "saved": true,
  "missing_tokens": []
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="POST" path="/v1/agents/{agent_id}/prompt/preview" title="Preview the full prompt" id="preview-prompt">

Returns the prompt exactly as the agent receives it, with tokens left as written. Send `sections` to preview a draft without saving it.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<Params title="Body">
<ParamField name="sections" type="array">Draft sections. Omit to preview the saved prompt.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/agents/dispatch-followup/prompt/preview" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.post(
    f"{API}/v1/agents/dispatch-followup/prompt/preview",
    headers=HEADERS,
    json={},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/prompt/preview`, {
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
  "prompt": "# ROLE AND GOAL\nYou are Riya from the purchase team...",
  "characters": 2841,
  "draft": false
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="PUT" path="/v1/agents/{agent_id}/inputs" title="Replace input variables" id="update-inputs">

Sets what the agent knows before each call. Each input is a column in the upload template and a `{{token}}` in the prompt.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<Params title="Body">
<ParamField name="variables" type="array" required>List of `{key, type, transform, sample, share_on_call}`. `transform: "spell_digits"` reads a value digit by digit. `share_on_call: false` gives the value to the agent but it is never spoken.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X PUT "$ECHO_API/v1/agents/dispatch-followup/inputs" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "variables": [
      {
        "key": "supplier_name",
        "type": "string",
        "transform": null,
        "sample": "Mehta Packaging",
        "share_on_call": true
      },
      {
        "key": "po_number",
        "type": "string",
        "transform": "spell_digits",
        "sample": "4471",
        "share_on_call": true
      },
      {
        "key": "open_qty",
        "type": "number",
        "transform": null,
        "sample": "14",
        "share_on_call": true
      },
      {
        "key": "supplier_code",
        "type": "string",
        "transform": null,
        "sample": "V-20931",
        "share_on_call": false
      }
    ]
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.put(
    f"{API}/v1/agents/dispatch-followup/inputs",
    headers=HEADERS,
    json={
  "variables": [
    {
      "key": "supplier_name",
      "type": "string",
      "transform": None,
      "sample": "Mehta Packaging",
      "share_on_call": True
    },
    {
      "key": "po_number",
      "type": "string",
      "transform": "spell_digits",
      "sample": "4471",
      "share_on_call": True
    },
    {
      "key": "open_qty",
      "type": "number",
      "transform": None,
      "sample": "14",
      "share_on_call": True
    },
    {
      "key": "supplier_code",
      "type": "string",
      "transform": None,
      "sample": "V-20931",
      "share_on_call": False
    }
  ]
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/inputs`, {
  method: "PUT",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "variables": [
      {
        "key": "supplier_name",
        "type": "string",
        "transform": null,
        "sample": "Mehta Packaging",
        "share_on_call": true
      },
      {
        "key": "po_number",
        "type": "string",
        "transform": "spell_digits",
        "sample": "4471",
        "share_on_call": true
      },
      {
        "key": "open_qty",
        "type": "number",
        "transform": null,
        "sample": "14",
        "share_on_call": true
      },
      {
        "key": "supplier_code",
        "type": "string",
        "transform": null,
        "sample": "V-20931",
        "share_on_call": false
      }
    ]
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "saved": true,
  "inputs": [
    {
      "key": "supplier_name",
      "type": "string",
      "transform": null,
      "sample": "Mehta Packaging",
      "share_on_call": true
    },
    {
      "key": "po_number",
      "type": "string",
      "transform": "spell_digits",
      "sample": "4471",
      "share_on_call": true
    },
    {
      "key": "open_qty",
      "type": "number",
      "transform": null,
      "sample": "14",
      "share_on_call": true
    },
    {
      "key": "supplier_code",
      "type": "string",
      "transform": null,
      "sample": "V-20931",
      "share_on_call": false
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="PUT" path="/v1/agents/{agent_id}/outputs" title="Replace output variables" id="update-outputs">

Sets what the agent must report before hanging up. Outputs become the columns of campaign results.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<Params title="Body">
<ParamField name="variables" type="array" required>List of `{key, label, type, options, description, required}`. Use `type: "enum"` with `options` for statuses.</ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X PUT "$ECHO_API/v1/agents/dispatch-followup/outputs" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "variables": [
      {
        "key": "status",
        "label": "Status",
        "type": "enum",
        "options": [
          "CONFIRMED",
          "PARTIAL",
          "NEW_DATE",
          "CALL_BACK"
        ],
        "description": "Outcome after read-back",
        "required": true
      },
      {
        "key": "dispatch_date",
        "label": "Dispatch date",
        "type": "string",
        "options": [],
        "description": "Date confirmed after read-back",
        "required": true
      },
      {
        "key": "qty_ready",
        "label": "Quantity ready",
        "type": "number",
        "options": [],
        "description": "Cartons ready on that date",
        "required": true
      }
    ]
  }'
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.put(
    f"{API}/v1/agents/dispatch-followup/outputs",
    headers=HEADERS,
    json={
  "variables": [
    {
      "key": "status",
      "label": "Status",
      "type": "enum",
      "options": [
        "CONFIRMED",
        "PARTIAL",
        "NEW_DATE",
        "CALL_BACK"
      ],
      "description": "Outcome after read-back",
      "required": True
    },
    {
      "key": "dispatch_date",
      "label": "Dispatch date",
      "type": "string",
      "options": [],
      "description": "Date confirmed after read-back",
      "required": True
    },
    {
      "key": "qty_ready",
      "label": "Quantity ready",
      "type": "number",
      "options": [],
      "description": "Cartons ready on that date",
      "required": True
    }
  ]
},
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/outputs`, {
  method: "PUT",
  headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    "variables": [
      {
        "key": "status",
        "label": "Status",
        "type": "enum",
        "options": [
          "CONFIRMED",
          "PARTIAL",
          "NEW_DATE",
          "CALL_BACK"
        ],
        "description": "Outcome after read-back",
        "required": true
      },
      {
        "key": "dispatch_date",
        "label": "Dispatch date",
        "type": "string",
        "options": [],
        "description": "Date confirmed after read-back",
        "required": true
      },
      {
        "key": "qty_ready",
        "label": "Quantity ready",
        "type": "number",
        "options": [],
        "description": "Cartons ready on that date",
        "required": true
      }
    ]
  }),
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
console.log(await res.json());
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```json
{
  "saved": true,
  "outputs": [
    {
      "key": "status",
      "label": "Status",
      "type": "enum",
      "options": [
        "CONFIRMED",
        "PARTIAL",
        "NEW_DATE",
        "CALL_BACK"
      ],
      "description": "Outcome after read-back",
      "required": true
    },
    {
      "key": "dispatch_date",
      "label": "Dispatch date",
      "type": "string",
      "options": [],
      "description": "Date confirmed after read-back",
      "required": true
    },
    {
      "key": "qty_ready",
      "label": "Quantity ready",
      "type": "number",
      "options": [],
      "description": "Cartons ready on that date",
      "required": true
    }
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/agents/{agent_id}/template" title="Download the upload template" id="agent-template">

A spreadsheet with one column per input, ready to fill in.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/agents/dispatch-followup/template" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -o template.xlsx
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents/dispatch-followup/template",
    headers=HEADERS,
)
res.raise_for_status()
open("template.xlsx", "wb").write(res.content)
```
```javascript Node.js
import fs from "node:fs";
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup/template`, {
  headers: { Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`Echo API ${res.status}`);
await fs.promises.writeFile("template.xlsx", Buffer.from(await res.arrayBuffer()));
```
</CodeGroup>
</RequestExample>
<ResponseExample status="200">
```text
Binary .xlsx file
```
</ResponseExample>

</Endpoint>

<Endpoint method="GET" path="/v1/agents/options" title="List options" id="list-options">

Voices, calling lines, variable types and transforms available to your workspace. Use it to build your own agent forms.

<RequestExample>
<CodeGroup>
```bash cURL
curl "$ECHO_API/v1/agents/options" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.get(
    f"{API}/v1/agents/options",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/options`, {
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
  "voices": [
    {
      "id": "default",
      "gender": "female"
    },
    {
      "id": "meera",
      "gender": "female"
    },
    {
      "id": "arjun",
      "gender": "male"
    }
  ],
  "calling_lines": [
    {
      "id": "ops-outbound",
      "direction": "outbound"
    }
  ],
  "input_types": [
    "string",
    "number",
    "phone",
    "date"
  ],
  "output_types": [
    "string",
    "number",
    "boolean",
    "enum"
  ],
  "transforms": [
    "spell_digits"
  ]
}
```
</ResponseExample>

</Endpoint>

<Endpoint method="DELETE" path="/v1/agents/{agent_id}" title="Delete an agent" id="delete-agent">

Deletes the agent. Past campaigns keep their results.

<Params title="Path parameters">
<ParamField name="agent_id" type="string" required></ParamField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X DELETE "$ECHO_API/v1/agents/dispatch-followup" \
  -H "Authorization: Bearer $ECHO_API_KEY"
```
```python Python
import os, requests

API = os.environ["ECHO_API"]
HEADERS = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

res = requests.delete(
    f"{API}/v1/agents/dispatch-followup",
    headers=HEADERS,
)
res.raise_for_status()
print(res.json())
```
```javascript Node.js
const API = process.env.ECHO_API;
const KEY = process.env.ECHO_API_KEY;

const res = await fetch(`${API}/v1/agents/dispatch-followup`, {
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
  "id": "cod-confirmation",
  "deleted": true
}
```
</ResponseExample>

</Endpoint>
