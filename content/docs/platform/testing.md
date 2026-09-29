---
title: Call console
description: Talk to any agent before it talks to anyone else. Test from your browser, or ring a real phone.
keywords:
- test a voice agent
- call console
updated: '2026-09-25'
---

## Browser or phone

| Channel | Use it for |
| --- | --- |
| Browser mic | Fast iteration on the prompt. Use headphones: on speakers the agent hears itself and stops to listen. |
| Phone | Hearing the agent on a real line, with real network delay and audio quality. Type a 10-digit Indian number and Echo adds +91; the call uses the agent’s own calling line. |

## Set up a test call

<Steps>
<Step title="Pick a channel">
Browser mic, or a phone channel if your workspace has one.
</Step>
<Step title="Pick the agent">
The console runs agents directly, so no campaign is needed.
</Step>
<Step title="Pick a voice">
Leave it on default, or try another voice for this call only. The agent’s saved voice does not change.
</Step>
<Step title="Start">
Press **Start call** for the browser, or **Call** to ring the number.
</Step>
</Steps>

<figure class="ui"><div class="ui-bar"><i></i><i></i><i></i><span>Echo · Call console</span></div><div class="ui-b"><div class="ui-row"><span class="ui-kv"><b>Channel</b><span>Browser mic</span><b>Agent</b><span>Where is my order</span><b>Voice</b><span>Default</span></span><span class="ui-tag busy" style="margin-left:auto">Live · 00:42</span></div><div class="ui-split"><div class="ui-col"><small>Transcript</small><div class="ui-turn"><small>agent</small>Hi, this is Meera from support. Could you tell me your order number?</div><div class="ui-turn me"><small>you</small>It’s 88213.</div><div class="ui-turn"><small>agent</small>Thanks. 8, 8, 2, 1, 3: it’s out for delivery, reaching you by 6 pm today.</div></div><div class="ui-col"><small>Activity</small><div class="ui-ev"><span>10:04</span><i></i><span>call started · agent ready</span></div><div class="ui-ev"><span>10:04</span><i></i><span>caller speaking</span></div><div class="ui-ev"><span>10:05</span><i class="w"></i><span>outputs reported</span></div><small style="margin-top:6px">Captured outputs</small><div class="ui-kv"><b>order</b><span>88213</span><b>status</b><span>RESOLVED</span><b>tracking_sent</b><span>yes</span></div></div></div></div><figcaption>Test an agent from your browser or on a real phone. The transcript, events and captured outputs update live.</figcaption></figure>

## Call details

If the agent has inputs, the console shows one field per input. **Use samples** fills them with the agent’s sample values; **Clear** empties them. Internal inputs are marked. Anything you leave empty is passed to the agent as “(not provided)”.

These values are used for this call only and are discarded when it ends. Nothing is stored.

## During the call

- A live timer and the number of turns.
- The **transcript**, labelled you (or caller) and agent, as it happens.
- An **activity** panel with call events, such as the agent reporting its outputs.
- **Captured outputs**, filled in as soon as the agent reports them. Declared outputs that were not reported show as “-”, and anything reported but not declared is listed too, so a mismatch between prompt and variables is easy to spot.

## After the call

The transcript stays on screen until you start the next call. Browser calls have a recording you can play and download. Every test call also appears in the [call log](monitoring), with the same analysis tools as a real one.

## A test script

Run each agent through these before its first campaign:

- The happy path, answered fully.
- A correction: give one value, then change it.
- A filler: say “ok” or “hmm” when asked to confirm.
- Busy: “I’m in a meeting, call me at 4”.
- Wrong person, and “who is this?”.
- A bad line: “hello? hello?”.
- A switch between Hindi and English mid sentence.
- A refusal, and a request for a human.

After each, check the captured outputs are what your team would have written down.
