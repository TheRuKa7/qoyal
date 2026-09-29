---
title: 'Quickstart: your first campaign'
description: Build a voice agent, test it and call your first list. About fifteen minutes once your workspace and calling line are set up.
sidebarTitle: Quickstart
keywords:
- voice campaign quickstart
- first outbound call
updated: '2026-09-29'
---

## Before you start

- A workspace with your team in it. Your account team creates it and invites you during onboarding, before this guide starts.
- A **calling line** for your agent. This is the number and route Echo dials from, set up with you during onboarding.
- A short list of people to call, in a spreadsheet, and the answers you need from each of them.

## Step by step

<Steps>
<Step title="Sign in and pick your workspace">
Sign in with the account your admin set up for you. If you belong to more than one workspace, choose the one you want to work in.
</Step>
<Step title="Create an agent">
Go to **Agents → New agent**. Give it a name such as “Order payment follow-up”, a one-line description, and pick its calling line. Start from a blank agent or from a copy of one that already works.
</Step>
<Step title="Declare what it needs and what it must find out">
On **Input variables**, add the columns each call needs, such as `customer_name` and `order_id`. On **Output variables**, add what the agent must report, such as `status` and `promised_date`. See [Input and output variables](variables).
</Step>
<Step title="Write the prompt">
On the **Prompt** tab, add sections for the agent’s role, goal, flow and rules. Use `{{order_id}}` tokens wherever a value from the sheet belongs. Add a language rule, such as "Speak Hinglish and follow the caller if they switch" (see [Language and tone](best-practices#language-and-tone)). Press **Preview full prompt**, then **Save prompt**.

<Warning>Saved changes are used from the next call, including calls in campaigns that already use this agent. Test a change in the Call console before you save it on a live agent.</Warning>
</Step>
<Step title="Test it">
Open the **Call console**, pick the agent, press **Use samples**, and start a call from your browser. Try the happy path, a correction, and “call me later”. Then ring your own phone to hear it on a real line.
</Step>
<Step title="Create a campaign">
Go to **Campaigns → New campaign**, pick the agent, choose outbound or inbound, and add a description of the list. Download the **Template**: it already has one column per input.
</Step>
<Step title="Upload your list and confirm">
Start with 20 to 50 rows. Fill in the template and press **Upload data**. Echo proposes a column mapping and nothing is dialled yet. Check it, then confirm.

<Warning title="Confirming starts real calls">Every row that passes the compliance checks is dialled within the campaign's calling hours. Listen to the first calls before you upload the full list.</Warning>
</Step>
<Step title="Watch the results">
Contacts move from Pending to Dialled to Captured as calls finish. Open any contact for the transcript and recording, and download everything as a spreadsheet when you are done.
</Step>
</Steps>

## Checklist before you go live

- Every `{{token}}` in the prompt is declared as an input. The editor warns you when one is missing.
- Values that must never be spoken, such as internal codes, are marked as internal.
- Every output has a clear description, and status-like outputs use a fixed list of options.
- You have tested a correction, a refusal, a busy caller and a bad line.
- The agent has a calling line. Without one, campaigns cannot upload or dial.
- You started with a small list, and you listened to the first calls.

<Snippet file="compliance-gate.md"/>

## Next steps

Read the [prompt best practices](best-practices), copy a design from the [use-case playbooks](use-cases), or learn how to read the [dashboard](monitoring).
