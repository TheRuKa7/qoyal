---
title: Core concepts
description: The handful of ideas behind every screen in Echo.
keywords:
- voice agent concepts
- campaigns and outcomes
updated: '2026-09-25'
---

## The model in one picture

An **agent** knows how to have one kind of call. A **campaign** runs that agent against one list of **contacts**. Each contact gets a **call**, and each call ends in an **outcome**: the values the agent was asked to capture, with the transcript and recording attached.

```
Agent  ──►  Campaign  ──►  Contacts  ──►  Calls  ──►  Outcomes
(how to talk)  (one list)    (one row each)  (the conversation)  (the answers)
```

## Agent

An agent owns everything about how a call sounds and what it is for: the **prompt**, the **voice**, the **calling line** it dials from, and its **variables**. Change the agent and every campaign that uses it follows on its next call, with no restart.

## Inputs and outputs

**Input variables** are what the agent knows before it dials: a name, an order number, an amount due. They come from the columns of your sheet and fill the `{{tokens}}` in the prompt.

**Output variables** are what the agent must find out and report before it hangs up: a status, a date, a quantity, a reason. They become the columns of your results.

One input can be the **primary id**, such as an order or PO number. It identifies each row in results and exports.

## Campaign

A campaign is **one agent run against one list**. It is named after the agent and the time it was created, and you can add a description to say which list it was. A campaign can be outbound or inbound.

A campaign takes one upload. To call another list, create another campaign. This keeps every result tied to exactly the list that produced it.

## Call and outcome

Every call is logged with its time, number, agent, length, transcript and recording. When the agent has what it needs, it reports its output variables. Those values are saved against the contact and shown in results. Later, [call analysis](analysis) can add a summary, a priority and action items.

## Workspace

Everything lives in a workspace for your organisation. Admins decide who can use it, and [groups](team) decide who sees which campaigns.

## Lifecycle of a contact

| Status | What it means |
| --- | --- |
| Pending | Uploaded, not called yet. |
| Dialled | A call has been placed. Waiting for it to finish and report. |
| Captured | The call finished and the agent reported its outputs. |
| No answer | The call ended without any outputs, for example nobody picked up. |
| Disconnected, partial | The line dropped before the end. Whatever was captured is kept. |
| Input validation failed | Something in the row was wrong, such as a missing required value. It is stored but not called. Hover the status to see why. |
