---
title: Prompt editor
description: Write an agent’s instructions in sections, use tokens for values from each row, keep the automatic sections in step with the variables, and preview the full prompt.
keywords:
- voice agent prompt editor
- prompt sections
updated: '2026-09-29'
---

An agent’s prompt is a list of **sections**, joined in order. Splitting it this way keeps long prompts easy to read and lets you switch one part off while you test.

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Agents · Dispatch follow-up</span></div><div class="ui-b"><div class="ui-tabs"><span class="on">Prompt</span><span>Input variables (5)</span><span>Output variables (4)</span></div><div class="ui-sec"><div class="ui-sh">Role and goal<em>On · ↑ ↓ · Copy</em></div><div class="ui-code">You are Riya, calling from the purchase team of <u>{{company}}</u>. Your goal is to confirm the dispatch date and quantity for PO <u>{{po_number}}</u>.</div></div><div class="ui-sec"><div class="ui-sh">Read-back rules<em>On · ↑ ↓ · Copy</em></div><div class="ui-code">Repeat every date and quantity back. Save only on a clear yes. A filler is not a yes.</div></div><div class="ui-sec gen"><div class="ui-sh">Call details<em>auto · inputs · Refresh</em></div><div class="ui-code">- Supplier: <u>{{supplier_name}}</u>
- PO number: <u>{{po_number}}</u>
- Open quantity: <u>{{open_qty}}</u></div></div><div class="ui-sec gen"><div class="ui-sh">Outcome reporting<em>auto · outputs · Refresh</em></div><div class="ui-code">Before ending the call, report: dispatch_date, qty_ready, status, next_step.</div></div><div class="ui-row"><span class="ui-btn">+ Add section</span><span class="ui-btn p">Save prompt</span><span class="ui-btn">Preview full prompt</span></div></div><figcaption>The prompt is built from sections. Dashed sections are written for you from the agent’s variables.</figcaption></figure>

## Sections

Each section has a name and a body, and a small toolbar:

| Control | What it does |
| --- | --- |
| ↑ ↓ | Moves the section up or down. |
| On / Off | Skips the section without deleting it. Useful when testing a change. |
| Copy | Copies the section text. |
| Delete section | Removes it. **Add section** adds a new one at the end. |

A good agent usually has these sections: role and goal, opening line, conversation flow, read-back and confirmation rules, common moments (busy, wrong person, call back, bad line), language rules, and closing. See [prompt best practices](best-practices.md).

## Tokens

Write `{{order_id}}` wherever a value from the contact’s row belongs. At call time Echo replaces each token with that row’s value.

If the prompt uses a token that is not declared as an input variable, the editor lists it as missing, so you can fix it before any call goes out.

## Automatic sections

Two sections are written for you from the agent’s variables and marked **auto**:

- **Call details** lists each input the agent may talk about, with its token. Inputs marked as internal context are listed separately, so the agent uses them but never says them.
- **Outcome reporting** tells the agent which outputs to report before hanging up, with their types, options and descriptions.

You can edit their wording. When the variables change, **Refresh** adds lines for new variables and removes lines for deleted ones, and leaves the rest of your wording alone. **Reset** goes back to the generated text. A section you never edited keeps following the variables on its own.

## Preview and save

**Preview full prompt** shows the whole prompt exactly as the agent will get it, including unsaved edits. You can copy it from there. **Save prompt** stores it, and the change is live on the next call for every campaign that uses the agent.

<Info>
Change prompts between runs where you can. A campaign that is already calling picks up the new prompt on its next call, so results from one list may come from two versions.
</Info>
