---
title: Voice and calling line
description: Choose the voice an agent speaks with, the calling line its calls use, and the primary id column that ties each call back to your records.
keywords:
- voice agent voice
- calling line
updated: '2026-10-05'
---

These settings sit on the agent’s **Voice** and **Settings** areas. Campaigns that use the agent inherit all of them.

## Voice

Pick a voice from the list. Each shows its gender. Leave it on **Default** to use the standard voice.

Voice changes apply as soon as you pick them, with no save needed, and do not disturb a prompt you are part-way through editing.

<Tip>
Test a new voice in the [call console](testing.md) with a real number before a campaign uses it. Names, numbers and local terms are where voices differ most.
</Tip>

## Voice presets <Badge tone="soon">Coming soon</Badge>

Pick one of four presets instead of choosing models. Each one names the model that listens, the model that thinks and the model that speaks, with a backup for each that takes over within 2.5 seconds if the main one fails.

![Voice section: four presets with a price per minute](assets/voice/agent-voice.webp "Four presets, each with a price per call minute, and the voice picker")

| Preset | For | Listens | Thinks | Speaks | Turn taking | Price per call minute |
| --- | --- | --- | --- | --- | --- | --- |
| **Balanced** (default) | Most calls, natural Indian voice | Sarvam Saaras V4 | Claude Haiku 4.5 | Sarvam Bulbul v3 | LiveKit turn detector | about Rs 2.77 ($0.032) |
| **High intelligence** | Disputes, negotiation, many orders on one call | Sarvam Saaras V4 | Claude Sonnet 5 | Cartesia Sonic | LiveKit turn detector | about Rs 3.99 ($0.045) |
| **Ultra fast** | The lowest delay | ElevenLabs Scribe v2 Realtime | gpt-oss-120b on Groq | Murf Falcon | Krisp Turn v3 | about Rs 1.17 ($0.013) |
| **Cost saver** | High volume, simple calls | Soniox | GPT-6 Luna | Murf Falcon | The model's own | about Rs 0.73 ($0.008) |

Prices are model costs from each vendor's public price page (checked 1 October 2026), before telephony.

![Voice details: each stage, its backup, turn taking, delay and cost](assets/voice/agent-voice-details.webp "Details shows each stage, its backup, turn taking, delay and cost")

<Note>
Bulbul v3 ranked first for listener preference in a blind test on 8 kHz phone audio across 11 Indian languages, and Saaras V4 had the lowest average English word error rate across seven benchmark sets. Delays are being measured in pilot calls.
</Note>

Choose **Custom** to pick each model yourself. Conversation settings (who speaks first, how long a pause ends a turn, interruptions, small acknowledgements, noise filtering, voicemail, silence and length limits) are under **Advanced**.

## Language

The agent speaks the language its prompt tells it to use. Say it in a **language rules** section, for example “Speak Hinglish. Switch to English if the contact does.” Keep dates, amounts and codes in the form your contacts expect.

## Calling line

The calling line is the number and route the agent’s calls go out on. Your account team sets up lines for your workspace and links each agent to one.

<Warning>
Until an agent has a calling line, its campaigns cannot upload a list or place calls. The campaign form tells you when this is the case.
</Warning>

## Primary id column

Choose which input identifies a row in your own system, such as a PO number or order id. The agents list shows it, and results and exports carry it, so every outcome can be matched back to the record that produced it.
