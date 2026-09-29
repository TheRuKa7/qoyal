---
# API reference template: one resource, several endpoints (Swagger style).
# Copy to content/docs/developers/<resource>.md and add it to docs.yml under "API reference".
title: Resource name API
description: What the resource is and what you can do with it, in one sentence.
keywords: [resource API]
updated: 2026-09-29
---

One paragraph on the resource. Link to [Core objects](objects) for the full object.

<Endpoint method="POST" path="/v1/resources" title="Create a resource">

What the call does and when to use it.

<Params title="Body">
<ParamField name="name" type="string" required>What it is.</ParamField>
<ParamField name="limit" type="integer" default="50">An optional field with a default.</ParamField>
</Params>

<Params title="Response">
<ResponseField name="id" type="string">Stable id.</ResponseField>
</Params>

<RequestExample>
<CodeGroup>
```bash cURL
curl -X POST "$ECHO_API/v1/resources" \
  -H "Authorization: Bearer $ECHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Example" }'
```
```python Python
import os, requests

res = requests.post(f"{os.environ['ECHO_API']}/v1/resources",
                    headers={"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"},
                    json={"name": "Example"})
res.raise_for_status()
```
```javascript Node.js
const res = await fetch(`${process.env.ECHO_API}/v1/resources`, {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.ECHO_API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Example" }),
});
```
</CodeGroup>
</RequestExample>

<ResponseExample status="201">
```json
{ "id": "res_123", "name": "Example" }
```
</ResponseExample>

</Endpoint>
