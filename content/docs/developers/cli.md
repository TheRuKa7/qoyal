---
title: CLI, MCP and skills
description: Build, test and run Echo voice agents from your terminal with the Echo CLI, drive them from AI coding tools over MCP, and add agent skills.
sidebarTitle: CLI, MCP and skills
keywords:
- voice agent CLI
- voice AI MCP server
- agent skills for voice agents
updated: '2026-09-29'
---

The Echo CLI is the main way developers work with Echo. It wraps the same API, so anything you do here you can also do over HTTP.

<Note title="Developer preview">The CLI, the MCP server and the skills pack are in developer preview. Your account team shares the install link with your pilot access.</Note>

## Log in

```bash
cognilix login
cognilix auth whoami
```

`login` opens your browser and stores a key for this machine. Use `cognilix auth switch` if you work across more than one workspace.

## Build and test an agent

<Steps>
<Step title="Scaffold">`cognilix agents init dispatch-followup --template delivery-date` creates the agent from a template.</Step>
<Step title="Test">`cognilix agents test dispatch-followup --lang hi-IN` runs a test call in the language you pick.</Step>
<Step title="Call yourself">`cognilix calls start --agent dispatch-followup --to <your number>` places one real call.</Step>
</Steps>

<Warning title="Calls are real">There is no sandbox yet. Place test calls to your own phone.</Warning>

## Run a campaign

```bash
cognilix campaigns run \
  --agent dispatch-followup \
  --contacts open_pos.xlsx \
  --window 10:00-18:00 --retries 3
```

Read results as JSON with `cognilix campaigns results <campaign id> --json`, or see [Run a campaign](guide-campaign.md) for the API version.

## Get outcomes on your laptop

```bash
cognilix listen --forward http://localhost:3000/echo
```

`listen` forwards [webhook events](webhooks.md) to a local server while you build, so you do not need a public URL.

## MCP server

The MCP server gives AI tools such as Claude Code, Cursor and VS Code the same actions as the CLI: list agents, place a test call, read outcomes.

```bash
cognilix mcp install --client claude-code
```

Or add it to any MCP client by hand:

```json mcp.json
{
  "mcpServers": {
    "echo": { "command": "cognilix", "args": ["mcp"] }
  }
}
```

## Agent skills

The Echo skills pack teaches AI coding tools how to write Echo agents, prompts and webhook handlers correctly. It follows the Agent Skills format, so it works in Claude Code, Cursor and other tools that support it.

## Prefer HTTP?

The API is open to every workspace. Start with the [API quickstart](quickstart.md).
