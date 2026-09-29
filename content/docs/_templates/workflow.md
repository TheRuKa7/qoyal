---
# Workflow template: one business workflow end to end (a playbook).
title: Workflow name, such as Post-PO acceptance
description: What the workflow achieves, in one sentence.
keywords: [workflow keyword, industry keyword]
updated: 2026-09-29
---

**Problem.** What goes wrong today without the call.

**What the agent does.** One or two sentences.

**Outcome.** What lands in which system, and what it moves.

## Inputs and outputs

<Columns>
<Column>

#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| supplier_name | shared |

</Column>
<Column>

#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: CONFIRMED, CALL_BACK |

</Column>
</Columns>

## Call flow

<Steps>
<Step title="Introduce and confirm the contact">What the agent says first.</Step>
<Step title="Ask and read back">Every value is read back before it is saved.</Step>
<Step title="Close">How the call ends.</Step>
</Steps>

<Snippet file="compliance-gate.md"/>

## Measure

Which numbers to watch, and against which baseline.
