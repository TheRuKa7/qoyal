---
title: Core objects
description: Every object the API returns, and what each field means.
keywords:
- API objects
- call object
updated: '2026-09-25'
---

## Agent

<Params>
<ParamField name="id" type="string">Stable id, derived from the name.</ParamField>
<ParamField name="name" type="string"></ParamField>
<ParamField name="description" type="string"></ParamField>
<ParamField name="voice" type="string | null">Null uses the default voice.</ParamField>
<ParamField name="calling_line" type="string | null">Where calls go out. Required to dial.</ParamField>
<ParamField name="primary_id" type="string | null">Key of the input that identifies a contact.</ParamField>
<ParamField name="inputs" type="Input[]"></ParamField>
<ParamField name="outputs" type="Output[]"></ParamField>
<ParamField name="created_at, updated_at" type="timestamp"></ParamField>
</Params>

## Input variable

<Params>
<ParamField name="key" type="string">Token name, used as `{{key}}`.</ParamField>
<ParamField name="type" type="string">See [options](agents#list-options).</ParamField>
<ParamField name="transform" type="string | null">`spell_digits` reads digit by digit.</ParamField>
<ParamField name="sample" type="string">Used in tests and previews.</ParamField>
<ParamField name="share_on_call" type="boolean">False means the agent knows it but never says it.</ParamField>
</Params>

## Output variable

<Params>
<ParamField name="key" type="string">Result column.</ParamField>
<ParamField name="label" type="string"></ParamField>
<ParamField name="type" type="string">`string`, `number`, `boolean` or `enum`.</ParamField>
<ParamField name="options" type="string[]">Allowed values for `enum`.</ParamField>
<ParamField name="description" type="string">Instruction to the agent.</ParamField>
<ParamField name="required" type="boolean"></ParamField>
</Params>

## Call

<Params>
<ParamField name="id" type="string"></ParamField>
<ParamField name="agent" type="string"></ParamField>
<ParamField name="campaign_id" type="string | null">Set when the call came from a campaign.</ParamField>
<ParamField name="direction" type="string">`outbound` or `inbound`.</ParamField>
<ParamField name="to" type="string">E.164.</ParamField>
<ParamField name="status" type="string">`queued`, `in_progress`, `completed`.</ParamField>
<ParamField name="started_at" type="timestamp"></ParamField>
<ParamField name="duration_seconds" type="integer"></ParamField>
<ParamField name="turns" type="integer">0 on a completed call means no audio.</ParamField>
<ParamField name="context" type="object">Inputs the call started with.</ParamField>
<ParamField name="outputs" type="object">What the agent reported.</ParamField>
<ParamField name="summary" type="string">One line.</ParamField>
<ParamField name="transcript" type="Turn[]">`{role, text}`, role is `agent` or `contact`.</ParamField>
<ParamField name="recording_url" type="string"></ParamField>
<ParamField name="analysis" type="Analysis | null"></ParamField>
<ParamField name="metadata" type="object">Your own references.</ParamField>
</Params>

## Campaign

<Params>
<ParamField name="id" type="string"></ParamField>
<ParamField name="name" type="string">Agent name and creation time.</ParamField>
<ParamField name="agent" type="string"></ParamField>
<ParamField name="direction" type="string"></ParamField>
<ParamField name="description" type="string"></ParamField>
<ParamField name="status" type="string">`created`, `ready`, `running`, `completed`, `failed`.</ParamField>
<ParamField name="source" type="string">`dashboard` or `api`.</ParamField>
<ParamField name="contacts_count, dialled_count, captured_count" type="integer"></ParamField>
<ParamField name="created_at" type="timestamp"></ParamField>
</Params>

## Contact

<Params>
<ParamField name="primary_id" type="string">Value of the agent’s primary id input.</ParamField>
<ParamField name="name, phone" type="string"></ParamField>
<ParamField name="status" type="string">`pending`, `dialled`, `captured`, `no_outputs`, `disconnected_early`, `input_validation_failed`.</ParamField>
<ParamField name="validation_error" type="string">Why a row was not dialled.</ParamField>
<ParamField name="call_id" type="string"></ParamField>
<ParamField name="outputs" type="object"></ParamField>
</Params>

## Analysis

<Params>
<ParamField name="executive_summary" type="string"></ParamField>
<ParamField name="priority" type="string">`low`, `medium`, `high`.</ParamField>
<ParamField name="issue_resolved" type="string">`yes`, `partial`, `no`.</ParamField>
<ParamField name="action_items" type="string[]"></ParamField>
</Params>

## Event

<Params>
<ParamField name="id" type="string">Unique. Use it to ignore duplicates.</ParamField>
<ParamField name="type" type="string">`call.completed`, `call.analyzed`, `contact.captured`, `campaign.completed`.</ParamField>
<ParamField name="created_at" type="timestamp"></ParamField>
<ParamField name="data" type="object">The call, contact or campaign.</ParamField>
</Params>
