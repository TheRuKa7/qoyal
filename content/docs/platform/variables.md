---
title: Input and output variables
description: Decide what the agent knows before the call and what it must report after. This is what turns a conversation into data.
keywords:
- input and output variables
- structured call outcomes
updated: '2026-10-05'
---

## Input variables

![Call data tab listing input columns](assets/variables/agent-call-data.webp "Call data: the columns each call uses, with samples for test calls")

Each input is one column of your sheet and one token in the prompt.

| Field | What it does |
| --- | --- |
| Key | The token name, such as `order_id`. Used as `{{order_id}}` in the prompt and as the column name in the template. |
| Type | The kind of value, such as text or a number. |
| Transform | **Spell digits** makes the agent read a value digit by digit, right for order, PO and phone numbers. Never use it for amounts or counts. |
| Sample value | Used in test calls and previews, so you can try the agent without a sheet. |
| Share on call | On: the agent may say and discuss this value. Off: the value is internal (see below). |

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Agents · Dispatch follow-up · Input variables</span></div><div class="ui-b"><div class="ui-t"><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>Key (the token)</span><span>Type</span><span>Transform</span><span>Sample value</span><span>Share on call</span></div><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>supplier_name</span><span>string</span><span>None</span><span>Mehta Packaging</span><span>✓</span></div><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>po_number</span><span>string</span><span>Spell digits</span><span>4471</span><span>✓</span></div><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>open_qty</span><span>number</span><span>None</span><span>14</span><span>✓</span></div><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>supplier_code</span><span>string</span><span>None</span><span>V-20931</span><span>internal</span></div><div style="grid-template-columns:1.3fr .8fr .9fr 1fr .8fr"><span>phone</span><span>phone</span><span>None</span><span>98765 43210</span><span>✓</span></div></div><div class="ui-row"><span class="ui-kv"><b>Primary id column</b><span>po_number</span></span></div><div class="ui-t"><div style="grid-template-columns:1fr 1fr .7fr 1.4fr .6fr"><span>Key</span><span>Label</span><span>Type</span><span>Options</span><span>Required</span></div><div style="grid-template-columns:1fr 1fr .7fr 1.4fr .6fr"><span>status</span><span>Status</span><span>enum</span><span>CONFIRMED, PARTIAL, NEW_DATE, CALL_BACK</span><span>✓</span></div><div style="grid-template-columns:1fr 1fr .7fr 1.4fr .6fr"><span>dispatch_date</span><span>Dispatch date</span><span>string</span><span></span><span>✓</span></div><div style="grid-template-columns:1fr 1fr .7fr 1.4fr .6fr"><span>qty_ready</span><span>Quantity ready</span><span>number</span><span></span><span>✓</span></div><div style="grid-template-columns:1fr 1fr .7fr 1.4fr .6fr"><span>next_step</span><span>Next step</span><span>string</span><span></span><span></span></div></div></div><figcaption>Inputs are what the agent knows before the call. Outputs are what it must report before hanging up.</figcaption></figure>

## Internal values

Untick **Share on call** for values the agent needs but must never say, such as a supplier code or an internal account id. The agent still receives them for matching and lookups, under an explicit instruction never to speak, confirm or reveal them.

## Primary id

Choose one input as the **primary id column**, usually the reference your team already uses: order id, PO number, loan number. It identifies each row in results and becomes the first column in exports.

## Output variables

![Answers tab listing what the agent reports](assets/variables/agent-answers.webp "Answers: what the agent must report after every call, including one answer per row")

Outputs are the fields the agent must report before it hangs up. They become the columns of your results.

| Field | What it does |
| --- | --- |
| Key | The column name in results, such as `promised_date`. |
| Label | A readable name shown in the dashboard. |
| Type | Text, number, yes or no, or a **choice** from a fixed list. |
| Options | For choice outputs: the allowed values, such as `CONFIRMED, PARTIAL, CALL_BACK`. |
| Description | Tells the agent exactly what to capture and when. This is the most important field. |
| Required | Whether the agent must report it on every call. |

If a required output was not reported, it shows as “-” rather than disappearing. A missing answer is a result too.

## A worked example

A supplier follow-up agent might use:

| Kind | Key | Notes |
| --- | --- | --- |
| Input | supplier_name | Shared on call |
| Input | po_number | Spell digits · primary id |
| Input | open_qty | Number |
| Input | supplier_code | Internal, never spoken |
| Output | status | Choice: CONFIRMED, PARTIAL, NEW_DATE, CALL_BACK, WRONG_CONTACT |
| Output | dispatch_date | The date confirmed after read-back |
| Output | qty_ready | Number, only after read-back |
| Output | next_step | Free text, for example a call-back time |

## Design tips

- Keep outputs few. Four to six fields that someone will act on beat fifteen that nobody reads.
- Always include one **status** output with fixed options. It is what you will filter and count by.
- Write descriptions as instructions: “The date the supplier confirms after read-back, in DD MMM format. Leave empty if they did not commit.”
- Add a call-back field so “call me at 4” is captured, not lost.
- Save inputs and outputs, then press **Refresh** on the automatic prompt sections.

## The upload template

Every agent has a spreadsheet template with one column per input, ready to fill in. Download it from a campaign or from the new-campaign form with **Preview template**.
