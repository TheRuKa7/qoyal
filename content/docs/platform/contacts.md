---
title: Upload and map contacts
description: Download the template for an agent, fill it, upload it, and confirm which column feeds each input before any call goes out.
sidebarTitle: Upload and map contacts
keywords:
- upload call list
- map spreadsheet columns
updated: '2026-09-29'
---

## Fill the template

On the campaign page, press **Template** to download a spreadsheet with exactly the columns this agent needs. Fill one row per person. Keep phone numbers as 10 digits or with the country code.

## Upload and map columns

Press **Upload data** and choose your filled sheet (.xlsx). Echo reads it and proposes which column feeds which input, using real values from your first rows so you can see it is right.

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Campaigns · Dispatch follow-up · Confirm columns</span></div><div class="ui-b"><div class="ui-note">1 column matched by position, not by name: <b>open_qty</b>. Check it especially.</div><div class="ui-t"><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>Agent input</span><span>Column in your sheet</span><span>First rows</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>phone *</span><span>Contact no. (by name)</span><span>98765 43210 · 91234 56789</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>supplier_name *</span><span>Supplier (by name)</span><span>Mehta Packaging · Vijay Steel</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>po_number *</span><span>PO No (by name)</span><span>4471 · 5120</span></div><div style="grid-template-columns:1fr 1.2fr 1.6fr"><span>open_qty</span><span>Column D (by position)</span><span>14 · 20</span></div></div><div class="ui-row"><span class="ui-btn">Cancel</span><span class="ui-btn p">Confirm and start 148 calls</span></div></div><figcaption>Echo proposes a mapping using real values from your sheet. Nothing is dialled until you confirm.</figcaption></figure>

- Columns matched **by position** rather than by name are flagged. Check those especially.
- Two inputs reading the **same column** are flagged. It is allowed, but almost always a mistake.
- **Required** inputs must be mapped before you can continue.

You can use your own sheet with different headers. Map its columns here instead of renaming them.

## Rows that are not called

Rows with a problem, such as a missing required value, are stored as **Input validation failed** and are not called. Hover the status in the contacts list to see the reason, fix the row, and upload it in a new campaign.
