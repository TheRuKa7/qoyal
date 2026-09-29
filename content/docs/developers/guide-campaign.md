---
title: Run a campaign from code
description: Create a campaign, check the column mapping with a dry run, upload, and collect results.
keywords:
- campaign API
- bulk calls API
updated: '2026-09-29'
status: soon
soon_note: The public REST API is not open yet. Endpoints and fields may change before release. Ask your account team for early access.
---

## The flow

<Steps>
<Step title="Create">
`POST /v1/campaigns` with the agent.
</Step>
<Step title="Dry run">
Upload with `dry_run=true` and check the proposed mapping.
</Step>
<Step title="Upload">
Upload again with the confirmed `mapping`. Dialling starts.
</Step>
<Step title="Follow">
Poll the campaign or listen for `contact.captured` and `campaign.completed`.
</Step>
<Step title="Collect">
Read `/results`, or download CSV, XLSX or the transcripts and audio archive.
</Step>
</Steps>

## A complete script

```python Python
import os, json, time, requests

API = os.environ["ECHO_API"]
H = {"Authorization": f"Bearer {os.environ['ECHO_API_KEY']}"}

# 1. Create the campaign
c = requests.post(f"{API}/v1/campaigns", headers=H, json={
    "agent": "dispatch-followup",
    "description": "Week 39 open POs",
}).json()

# 2. Dry run: see how Echo maps your columns, without storing anything
with open("open_pos.xlsx", "rb") as f:
    plan = requests.post(f"{API}/v1/campaigns/{c['id']}/contacts", headers=H,
                         files={"file": f}, data={"dry_run": "true"}).json()
for m in plan["mapping"]:
    print(m["input"], "<-", m["header"], "(by", m["matched_by"] + ")")

# 3. Upload for real with the mapping you checked. Dialling starts now.
mapping = {m["input"]: m["column"] for m in plan["mapping"]}
with open("open_pos.xlsx", "rb") as f:
    requests.post(f"{API}/v1/campaigns/{c['id']}/contacts", headers=H,
                  files={"file": f}, data={"mapping": json.dumps(mapping)})

# 4. Wait for the campaign to finish (or use webhooks)
while requests.get(f"{API}/v1/campaigns/{c['id']}", headers=H).json()["status"] == "running":
    time.sleep(60)

# 5. Read the results
rows = requests.get(f"{API}/v1/campaigns/{c['id']}/results", headers=H).json()["data"]
for r in rows:
    print(r["primary_id"], r["status"], r["outputs"])
```

## Checking the mapping

Each mapping entry says how the column was matched. `matched_by: "position"` means Echo guessed from column order because no header matched; check those. Required inputs must be mapped or the upload is rejected with `422 missing_required_mapping`.

## Following progress

| Campaign status | Meaning |
| --- | --- |
| created | No list yet |
| ready | List stored, not dialled |
| running | Calls going out |
| completed | Dialling finished |
| failed | Dialling could not complete; see `error` |

## Rules to know

- One campaign takes one upload. Create a new campaign for each list.
- An agent without a calling line cannot dial: `422 no_calling_line`.
- Rows with bad data are stored as `input_validation_failed` with a reason, and are not dialled.
- Deleting a campaign deletes its results.
