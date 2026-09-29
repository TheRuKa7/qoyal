---
title: Echo for developers
description: Build and run Echo voice agents from your terminal, your AI coding tools and your own systems, with the Reverb CLI, the Relay MCP server, agent skills and the REST API.
sidebarTitle: Introduction
keywords:
- voice AI developer tools
- voice agent CLI
updated: '2026-09-29'
---

Everything in this tab is <Badge tone="soon">Coming soon</Badge>. The pages show how each tool will work, so you can plan an integration now. Your business team can already build, test and run agents in the Echo console; see the [Platform guide](../platform/index.md).

## The tools

<CardGroup cols="2">
<Card title="Reverb CLI" href="cli" eyebrow="Command line">Log in, scaffold agents, test them and run campaigns from your terminal. The main way to build with Echo.</Card>
<Card title="Relay MCP server" href="mcp" eyebrow="AI tools">Give Claude Code, Cursor and other MCP clients the same actions as the CLI.</Card>
<Card title="Agent skills" href="skills" eyebrow="AI tools">Teach AI coding tools to write correct Echo prompts, variables and webhook handlers.</Card>
<Card title="REST API" href="quickstart" eyebrow="HTTP">Calls, campaigns, results and webhooks, for any language.</Card>
</CardGroup>

## Which one to use

| You want to | Use |
| --- | --- |
| Build and test agents day to day | [Reverb CLI](cli.md) |
| Let an AI assistant draft, test and run agents | [Relay MCP server](mcp.md) with [agent skills](skills.md) |
| Place a call when something happens in your ERP | [REST API](guide-call.md) and [webhooks](webhooks.md) |
| Pull results, recordings and transcripts into your storage | [Exports](guide-exports.md) |

## The object model

```text
Agent ── has ──► inputs, outputs, prompt, voice, calling line
  │
  ├─► Call        one conversation   →  outputs, transcript, recording, analysis
  │
  └─► Campaign    one list           →  contacts  →  calls  →  results
```

Every tool works on these same objects, so an agent built in the console, the CLI or the API is the same agent. [Core objects](objects.md) lists every field.

## Early access

Tell your account team which tool you need first and what you want to connect it to. [Talk to an expert](/#pilot).
