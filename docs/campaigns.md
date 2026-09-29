---
title: Campaigns
description: 'Run an agent against a list: create the campaign, fill the template, confirm the columns, and collect results.'
keywords:
- outbound calling campaign
- upload call list
updated: '2026-09-25'
---

## Create a campaign

Go to **Campaigns → New campaign**.

- **Agent**: the agent to run. The campaign takes its voice and calling line from it.
- **Campaign type**: outbound (Echo calls the list) or inbound (Echo answers).
- **Description**: say which list this is, such as “Q3 open POs, chased once by email already”. Campaigns are named after the agent and the time, so this is where the run gets explained.

Before you create it, the form shows the **input columns** the list needs and the fields that will be **captured per call**. If the agent has no calling line yet, it tells you here.

## Fill the template

On the campaign page, press **Template** to download a spreadsheet with exactly the columns this agent needs. Fill one row per person. Keep phone numbers as 10 digits or with the country code.

## Upload and map columns

Press **Upload data** and choose your filled sheet (.xlsx). Echo reads it and proposes which column feeds which input, using real values from your first rows so you can see it is right.

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Campaigns · Dispatch follow-up · Confirm columns</span></div><div class="ui-b"><div class="ui-note">1 column matched by position, not by name: <b>open_qty</b>. Check it especially.</div><div class="ui-t"><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>Agent input</span><span>Column in your sheet</span><span>First rows</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>phone *</span><span>Contact no. (by name)</span><span>98765 43210 · 91234 56789</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>supplier_name *</span><span>Supplier (by name)</span><span>Mehta Packaging · Vijay Steel</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>po_number *</span><span>PO No (by name)</span><span>4471 · 5120</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>open_qty</span><span>Column D (by position)</span><span>14 · 20</span></div></div><div class="ui-row"><span class="ui-btn">Cancel</span><span class="ui-btn p">Confirm and start 148 calls</span></div></div><figcaption>Echo proposes a mapping using real values from your sheet. Nothing is dialled until you confirm.</figcaption></figure>

- Columns matched **by position** rather than by name are flagged. Check those especially.
- Two inputs reading the **same column** are flagged. It is allowed, but almost always a mistake.
- **Required** inputs must be mapped before you can continue.

You can use your own sheet with different headers. Map its columns here instead of renaming them.

## Start calling

Confirming the mapping stores the list and starts dialling. There is no separate save step, so the mapping screen is your last check. If a list was stored but not dialled, **Run campaign** starts it, after a confirmation that shows how many real numbers will be called.

Rows with a problem, such as a missing required value, are stored as **Input validation failed** and are not called.

<Info>
One campaign takes one list. To call another list, create another campaign, so every result stays tied to the list that produced it.
</Info>

## Watch it run

While a campaign is running, the page refreshes on its own. The tiles show contacts, captured results, output variables and status. The **Contacts** tab lists every number with its status; open one to see its captured outputs, transcript and recording.

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Campaigns · Dispatch follow-up · Contacts</span></div><div class="ui-b"><div class="ui-tiles" style="grid-template-columns:repeat(4,minmax(0,1fr))"><div><small>Contacts</small><b>148</b></div><div><small>Captured</small><b>96</b></div><div><small>Output variables</small><b>4</b></div><div><small>Status</small><b>running</b></div></div><div class="ui-split"><div class="ui-col"><small>Contacts</small><div class="ui-row" style="justify-content:space-between"><span>+91 98765 43210</span><span class="ui-tag ok">Captured</span></div><div class="ui-row" style="justify-content:space-between"><span>+91 91234 56789</span><span class="ui-tag busy">Dialled</span></div><div class="ui-row" style="justify-content:space-between"><span>+91 99887 76655</span><span class="ui-tag bad">No answer</span></div><div class="ui-row" style="justify-content:space-between"><span>+91 90000 11122</span><span class="ui-tag busy">Disconnected, partial</span></div><div class="ui-row" style="justify-content:space-between"><span>+91 98111 22233</span><span class="ui-tag bad">Input validation failed</span></div><div class="ui-row" style="justify-content:space-between"><span>+91 97000 33344</span><span class="ui-tag">Pending</span></div></div><div class="ui-col"><small>Mehta Packaging · PO 4471</small><div class="ui-kv"><b>status</b><span>PARTIAL</span><b>dispatch_date</b><span>28 Sep</span><b>qty_ready</b><span>10</span><b>next_step</b><span>Follow-up 27 Sep</span></div><div class="ui-turn"><small>agent</small>PO 4471: 14 cartons. Dispatch kab tak ho jayega?</div><div class="ui-turn me"><small>contact</small>28 ko, par abhi sirf 10 ready hain.</div><div class="ui-row"><span class="ui-btn">▶ Recording 1:52</span><span class="ui-btn">Download audio</span></div></div></div></div><figcaption>Every contact shows its call status. Open one to see what was captured, the transcript and the recording.</figcaption></figure>

Once the first results arrive, a **Responses** tab shows one row per contact with every output as a column. Select rows to download their audio or analyse them together.

## Statuses

| Campaign status | Meaning |
| --- | --- |
| Ready | The list is stored and ready to dial. |
| Running | Calls are going out. |
| Completed | Dialling has finished. |
| Failed | Dialling could not complete. The page says why. |

| Contact status | Meaning |
| --- | --- |
| Pending | Not called yet. |
| Dialled | Called, waiting for the result. |
| Captured | Outputs reported. |
| No answer | Ended without outputs. |
| Disconnected, partial | Dropped early; partial outputs kept. |
| Input validation failed | Not called; hover for the reason. |

## Results and exports

| Download | What you get |
| --- | --- |
| Results | A formatted spreadsheet of every captured response. |
| Export CSV | The same responses as CSV, for your own tools. Also available in one click from the campaigns list. |
| Transcripts + audio | Every transcript and recording from the campaign, in one archive. |
| Per contact | Play or download a single recording from the contact’s detail. |

## Managing campaigns

- The campaigns list shows each run’s agent, contacts, captured count, status and date.
- Campaigns created from your own systems through the API carry a small tag with their source.
- **Delete** removes the campaign, its list and every captured result. It asks first, and says how many results would be lost.
