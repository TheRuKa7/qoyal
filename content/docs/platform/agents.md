---
title: Agents
description: Create an agent, write its prompt in sections, choose its voice and calling line, and keep it in step with its variables.
keywords:
- voice agent prompt
- agent voice and calling line
updated: '2026-09-25'
---

## The agents list

**Agents** shows every agent in your workspace with how many inputs and outputs it has and which input is its primary id. Click a row to open it. Access to this page is given per person by an admin, because it shows and edits every prompt.

## Create an agent

<Steps>
<Step title="Name and description">
Use a name that says what the call is for, such as “COD confirmation”. The description is for your team.
</Step>
<Step title="Start from">
Choose **Blank agent**, or **Copy of** an existing agent to inherit its prompt, inputs and outputs. Copying a working agent is the fastest way to a new one.
</Step>
<Step title="Calling line">
Pick the line this agent’s calls go out on. Campaigns that use the agent inherit it. Until an agent has a line, its campaigns cannot upload a list or place calls.
</Step>
</Steps>

## The prompt editor

An agent’s prompt is a list of **sections**, joined in order. Each section has a title and a body, and a small toolbar:

- **↑ ↓** move it up or down.
- **On / Off** skips a section without deleting it, useful when testing a change.
- **Copy** copies the text in use.
- **Delete** removes it. **Add section** adds a new one at the end.

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Agents · Dispatch follow-up</span></div><div class="ui-b"><div class="ui-tabs"><span class="on">Prompt</span><span>Input variables (5)</span><span>Output variables (4)</span></div><div class="ui-row"><span class="ui-kv"><b>Voice</b><span>Default · Female</span><b>Calling line</b><span>Outbound · Operations</span></span></div><div class="ui-sec"><div class="ui-sh">Role and goal<em>On · ↑ ↓ · Copy</em></div><div class="ui-code">You are Riya, calling from the purchase team of <u>{{company}}</u>. Your goal is to confirm the dispatch date and quantity for PO <u>{{po_number}}</u>.</div></div><div class="ui-sec"><div class="ui-sh">Read-back rules<em>On · ↑ ↓ · Copy</em></div><div class="ui-code">Repeat every date and quantity back. Save only on a clear yes. A filler is not a yes.</div></div><div class="ui-sec gen"><div class="ui-sh">Call details<em>auto · inputs · Refresh</em></div><div class="ui-code">- Supplier: <u>{{supplier_name}}</u>
- PO number: <u>{{po_number}}</u>
- Open quantity: <u>{{open_qty}}</u></div></div><div class="ui-sec gen"><div class="ui-sh">Outcome reporting<em>auto · outputs · Refresh</em></div><div class="ui-code">Before ending the call, report: dispatch_date, qty_ready, status, next_step.</div></div><div class="ui-row"><span class="ui-btn">+ Add section</span><span class="ui-btn p">Save prompt</span><span class="ui-btn">Preview full prompt</span></div></div><figcaption>The prompt is built from sections. Dashed sections are written for you from the agent’s variables.</figcaption></figure>

A good agent usually has these sections: role and goal, opening line, conversation flow, read-back and confirmation rules, handling of common moments (busy, wrong person, call back, bad line), language rules, and closing. See [prompt best practices](best-practices).

## Automatic sections

Two sections are written for you from the agent’s variables, and marked **auto**:

- **Call details** lists each input the agent may talk about, with its token.
- **Outcome reporting** tells the agent which outputs to report before hanging up, with their types, options and descriptions.

You can edit their wording. When the variables change later, **Refresh** adds lines for new variables and removes lines for deleted ones, and leaves the rest of your wording alone. **Reset** goes back to the generated text. A section you never edited keeps following the variables automatically.

## Tokens and checks

Write `{{order_id}}` wherever a value from the contact’s row belongs. At call time Echo replaces each token with that row’s value. If the prompt uses a token that is not declared as an input, the editor lists it as missing so you can fix it before any call goes out.

## Voice and calling line

Pick a voice from the list; each shows its gender. Leave it on **Default** to use the standard voice. Voice and calling line apply as soon as you change them, with no save needed, and do not disturb a prompt you are part-way through editing.

## Saving, preview and changes

**Preview full prompt** shows the whole prompt exactly as the agent will get it, including unsaved edits, with its length. **Save prompt** stores it. The change is live on the next call, for every campaign that uses the agent.

<Info>
Change prompts between runs where you can. A campaign that is already calling picks up the new prompt on its next call, so results from one list may come from two versions.
</Info>

## Connected platforms

If your workspace has a partner platform connected, the agents list shows a **Sync** action. Syncing is permanent once it succeeds. While it is being delivered the row shows **Syncing**; if it fails after retries it shows **Failed** with the reason, and you can try again.

## Deleting an agent

Delete removes the agent and cannot be undone. Past campaigns keep their results and show the agent as no longer defined.
