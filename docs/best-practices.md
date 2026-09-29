---
title: Prompt best practices
description: How to write prompts that sound human, stay on task and capture reliable data.
keywords:
- voice agent prompt best practices
- read-back confirmation
updated: '2026-09-25'
---

## A structure that works

1. **Role and goal**: who the agent is, who it calls for, and the one thing the call must achieve.
2. **Opening**: name, company and reason in the first sentence.
3. **Flow**: the questions, in order, one at a time.
4. **Rules**: read-back, what counts as a yes, what never to say.
5. **Common moments**: how to handle each, briefly.
6. **Closing**: thank them, say what happens next, end the call.

Keep each section short. Several small sections are easier to test and switch off than one long one.

## Confirm, don’t assume

- Read back every date, amount, quantity and reference before reporting it.
- Treat “ok”, “hmm” and similar as “go on”, never as agreement.
- When the caller corrects a value, replace it and read it back again.
- Read reference numbers digit by digit (use the **Spell digits** transform).

## Handle the common moments

| Moment | A good rule |
| --- | --- |
| “Who is this?” | Give name, company and reason. Offer to stop calling. |
| Busy | Ask for a better time, capture it as a call-back, end politely. |
| Wrong person | Ask for the right contact, capture it, do not share details. |
| Bad line | Slow down, repeat once, shorter. |
| Dispute or objection | Note it and the reference; do not argue. |
| Wants a human | Offer a call back from the team, capture a time. |

## Language and tone

Say which languages to use and to follow the caller if they switch. Ask for short sentences and one question at a time. Use the caller’s name sparingly. Avoid jargon the caller would not use.

## Iterate with evidence

1. Test each change in the [call console](testing) with the test script.
2. Run a small list first and listen to ten calls.
3. Look at **Inconclusive** and **No audio** in the [funnel](monitoring); they show where calls go wrong.
4. Change one section at a time so you know what helped.
