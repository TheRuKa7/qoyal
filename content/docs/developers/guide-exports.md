---
title: Recordings, transcripts and exports
description: Keep the evidence for every call in your own systems.
sidebarTitle: Recordings and exports
keywords:
- call recordings export
- transcript export
updated: '2026-09-29'
status: soon
soon_note: The public REST API is not open yet. Endpoints and fields may change before release. Ask your account team for early access.
---

## One call

[Retrieve a call](calls#get-call) returns the transcript and outputs as JSON. Download the audio with [Download a recording](calls#get-recording).

<CodeGroup title="Download a recording">
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

## A whole campaign

Results as JSON, CSV or XLSX from [Retrieve results](campaigns#get-results); every transcript and recording in one archive from [Export transcripts and audio](campaigns#export-campaign).

<CodeGroup title="Export a campaign">
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

## The call log

[Export the call log](calls#export-calls) gives a spreadsheet with the same filters as the dashboard.

## Retention

Recordings stay available for a limited period set for your workspace. Copy anything you need to keep longer into your own storage.
