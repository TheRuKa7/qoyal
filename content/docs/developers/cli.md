---
title: Reverb CLI
description: Reverb is the Echo command line. Log in, scaffold an agent from a template, test it in any language, run campaigns and stream outcomes to your laptop.
sidebarTitle: Reverb CLI
status: soon
soon_note: Reverb is not released yet. Commands and flags may change before release. Ask your account team for early access.
keywords:
- voice agent CLI
- Reverb CLI
updated: '2026-09-29'
---

Reverb wraps the Echo API in one command, `reverb`. Anything you do with it you can also do in the console or over HTTP.

## Log in

```bash
reverb login
reverb whoami
```

`login` opens your browser and stores a key for this machine. Use `reverb org switch` if you work across more than one organisation.

## Build and test an agent

<Steps>
<Step title="Scaffold">
`reverb agents init dispatch-followup --template delivery-date` creates an agent from a template, with its prompt sections and variables.
</Step>
<Step title="Check">
`reverb agents check dispatch-followup` lists tokens used in the prompt but not declared as inputs, and outputs with no description.
</Step>
<Step title="Test">
`reverb agents test dispatch-followup --lang hi-IN` runs a test conversation in the language you pick and prints the captured outputs.
</Step>
<Step title="Call yourself">
`reverb calls start --agent dispatch-followup --to <your number>` places one real call.
</Step>
</Steps>

<Warning title="Calls are real">Calls placed with Reverb dial real numbers. Test with your own phone.</Warning>

## Run a campaign

```bash
reverb campaigns run \
  --agent dispatch-followup \
  --contacts open_pos.xlsx
```

Reverb shows the proposed column mapping and asks you to confirm before any call goes out, the same check as the console. Read the results as JSON with `reverb campaigns results <campaign id> --json`.

## Stream outcomes to your laptop

```bash
reverb listen --forward http://localhost:3000/echo
```

`listen` forwards [webhook events](webhooks.md) to a local server while you build, so you do not need a public URL.

## Command reference

| Command | What it does |
| --- | --- |
| `reverb login`, `reverb whoami` | Sign in and check the account in use. |
| `reverb agents list`, `init`, `check`, `test`, `pull`, `push` | Work with agents. `pull` and `push` keep prompts in your repository. |
| `reverb calls start`, `watch`, `get` | Place a call, follow it live, read its result. |
| `reverb campaigns run`, `status`, `results` | Run a list and read what it captured. |
| `reverb listen` | Forward webhook events to a local URL. |
| `reverb relay` | Start the [Relay MCP server](mcp.md). |
