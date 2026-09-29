---
title: Relay MCP server
description: Relay is the Echo MCP server. It gives Claude Code, Cursor, VS Code and other MCP clients the tools to list agents, place a test call and read outcomes.
sidebarTitle: Relay MCP server
status: soon
soon_note: Relay is not released yet. Tool names may change before release. Ask your account team for early access.
keywords:
- voice AI MCP server
- Relay MCP
updated: '2026-09-29'
---

Relay speaks the Model Context Protocol, so any AI assistant that supports MCP can work with your Echo agents on your behalf, with your permissions.

## Connect

<Tabs>
<Tab title="Claude Code">

```bash
reverb relay install --client claude-code
```

</Tab>
<Tab title="Cursor and VS Code">

```bash
reverb relay install --client cursor
reverb relay install --client vscode
```

</Tab>
<Tab title="Any MCP client">

```json mcp.json
{
  "mcpServers": {
    "echo": { "command": "reverb", "args": ["relay"] }
  }
}
```

</Tab>
</Tabs>

Relay runs through the [Reverb CLI](cli.md) and uses the account you logged in with.

## Tools

| Tool | What the assistant can do |
| --- | --- |
| `list_agents`, `get_agent` | Read agents, their prompt sections and variables. |
| `update_prompt` | Propose a prompt change. You confirm it before it is saved. |
| `test_agent` | Run a test conversation and return the captured outputs. |
| `start_call` | Place one call to a number you give it. Asks you first. |
| `get_results` | Read a campaign’s responses. |

<Info title="You stay in control">Relay asks before anything that places a call or changes a saved prompt. Everything it does is logged under your name.</Info>

## Pair it with skills

[Agent skills](skills.md) teach the assistant how Echo agents are written, so its prompt and variable changes follow the same rules as the console.
