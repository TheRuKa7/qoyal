---
title: Echo for developers
description: Place calls, run campaigns and read outcomes from your own systems. The same agents your business team builds, driven by code.
sidebarTitle: Introduction
keywords:
- voice AI API
- Echo API
updated: '2026-09-29'
---

<Info title="Developer preview">The API is in developer preview. Endpoints and fields may change before general availability, and keys are issued to pilot customers only, so you cannot try it without one. [Request access](/#pilot).</Info>

## What you can build

<CardGroup cols="2">
<Card title="Call on an event" href="guide-call" eyebrow="Guide">A new order, a late PO, an unpaid invoice: place a call the moment it happens.</Card>
<Card title="Run a campaign from code" href="guide-campaign" eyebrow="Guide">Create a campaign, check the mapping, upload, and collect results.</Card>
<Card title="Receive outcomes by webhook" href="webhooks" eyebrow="Guide">Receive every captured answer on a webhook and update your ERP or CRM.</Card>
<Card title="Recordings and exports" href="guide-exports" eyebrow="Guide">Pull recordings, transcripts and analysis into your own storage.</Card>
</CardGroup>

## Platform or API?

| Task | Dashboard | API |
| --- | --- | --- |
| Write and test prompts | Best here: editor, preview, call console | Read, version and replace |
| Declare inputs and outputs | Yes | Yes |
| Run a list | Upload a sheet | Upload a file or rows |
| Place one call on an event | Call console, for tests | Yes |
| Read outcomes | Dashboard, downloads | JSON, CSV, webhooks |
| Manage people and access | Yes | Not yet |

## Getting outcomes into your ERP

The documented routes are the API, [webhooks](webhooks) and [exports](guide-exports): your integration receives each outcome and writes it to your ERP, CRM or helpdesk. Ask your account team what is set up for your ERP during the pilot.

## The object model

```
Agent ── has ──► inputs, outputs, prompt, voice, calling line
  │
  ├─► Call        one conversation   →  outputs, transcript, recording, analysis
  │
  └─► Campaign    one list           →  Contacts  →  Calls  →  Results
```

Read [Core objects](objects) for every field.

## Conventions

- **Base URL**: shared with your API key. All paths start with `/v1`, the only version so far.
- **Test mode**: there is no sandbox yet. Calls placed through the API dial real numbers, so test with your own phone.
- **Auth**: `Authorization: Bearer <key>` on every request. See [Authentication](authentication).
- **Format**: JSON in and out, UTF-8. Timestamps are ISO 8601 in UTC. Phone numbers are E.164; the API also accepts a 10-digit Indian number and adds +91.
- **Lists** are paginated with `limit` and `cursor`; the response carries `next_cursor`, which is `null` on the last page.
- **Errors** return a JSON `error` object with a stable `code`. See [Errors](errors).

## Where to go next

Once you have a key, the [API quickstart](quickstart) places your first call in a few minutes. The [API reference](agents) lists every endpoint with examples in cURL, Python and Node.js.
