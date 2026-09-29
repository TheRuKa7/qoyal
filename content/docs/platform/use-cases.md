---
title: Use-case playbooks
description: Ready-to-copy agent designs for common calls. Each lists the sheet columns, the results to capture, the call flow and what to measure.
keywords:
- supplier follow-up playbook
- voice AI use cases
updated: '2026-09-25'
---

Every playbook uses the same building blocks: [inputs and outputs](variables), a prompt written in [sections](agents), and a [campaign](campaigns) per list. Copy one, then adjust the wording and fields to your process.

### Supplier dispatch follow-up

*Operations · outbound · Hinglish*

Confirm when each open purchase order line will ship, and how much.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| supplier_name | shared |
| po_number | spell digits · primary id |
| item | shared |
| open_qty | number |
| due_date | shared |
| supplier_code | internal |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: CONFIRMED, PARTIAL, NEW_DATE, CALL_BACK, WRONG_CONTACT |
| dispatch_date | date after read-back |
| qty_ready | number |
| reason | free text, if late |
| callback_time | free text |
</Column>
</Columns>

**Flow:** introduce, confirm the right contact, ask the dispatch date, ask the quantity, read both back, capture a reason if late, close.

**Measure:** confirmed lines, partial shipments caught, time from call to ERP update.

### Cash on delivery confirmation

*Retail and D2C · outbound · Hindi or English*

Confirm COD orders before dispatch to cut returns.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| customer_name | shared |
| order_id | spell digits · primary id |
| amount | number |
| address_short | shared |
| delivery_window | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: CONFIRMED, CANCEL, CHANGE_ADDRESS, CALL_BACK |
| address_change | free text |
| preferred_slot | free text |
</Column>
</Columns>

**Flow:** greet, confirm the order and amount, confirm they will be available, capture any address change, read it back.

**Measure:** confirmation rate, returns avoided, cancellations caught before dispatch.

### Payment reminders and promise to pay

*Collections · outbound · Hindi*

Remind politely and capture a clear promise to pay.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| customer_name | shared |
| loan_id | spell digits · primary id |
| amount_due | number |
| due_date | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: PROMISE_TO_PAY, PAID, DISPUTE, CALL_BACK, REFUSED |
| promise_date | date after read-back |
| promise_amount | number |
| payment_mode | choice: UPI, BANK, CASH, OTHER |
| dispute_reason | free text |
</Column>
</Columns>

**Flow:** identify the person, state the amount and date, ask when they will pay, read back amount and date, note disputes without arguing.

**Measure:** promises captured, promises kept, disputes flagged for your team.

### Lead qualification

*Sales · outbound · English or Hinglish*

Call new leads within minutes, qualify them and book a meeting.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| lead_name | shared |
| lead_id | primary id |
| source | internal |
| interest | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: QUALIFIED, NOT_NOW, NOT_INTERESTED, WRONG_NUMBER |
| need | free text |
| budget_band | choice |
| timeline | choice: THIS_MONTH, THIS_QUARTER, LATER |
| meeting_slot | free text |
</Column>
</Columns>

**Flow:** thank them for the enquiry, ask need, volume and timeline, offer a meeting slot, confirm it.

**Measure:** speed to first call, qualified rate, meetings booked.

### Interview scheduling

*HR · outbound · English*

Offer interview slots and confirm attendance.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| candidate_name | shared |
| candidate_id | primary id |
| role | shared |
| slot_options | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: BOOKED, RESCHEDULE, NOT_INTERESTED, CALL_BACK |
| slot | free text after read-back |
| notice_period | free text |
</Column>
</Columns>

**Flow:** confirm interest in the role, offer slots, read back the chosen slot, capture notice period.

**Measure:** booked rate, no-shows, time to schedule.

### Where is my order

*Support · inbound · English*

Answer order-status calls and send tracking.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| order_lookup | from your system |
| status_text | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| order_id | spell digits |
| status | choice: RESOLVED, ESCALATED, CALL_BACK |
| tracking_sent | yes or no |
| complaint | free text |
</Column>
</Columns>

**Flow:** ask for the order number, read it back digit by digit, share status, offer tracking, escalate with a call-back when needed.

**Measure:** calls resolved without a person, escalations, repeat callers.

### KYC and contact verification

*Compliance · outbound · Hinglish*

Confirm identity details and chase pending documents.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| customer_name | shared |
| account_id | primary id · internal |
| pending_doc | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| status | choice: VERIFIED, PENDING_DOC, WRONG_PERSON, CALL_BACK |
| doc_eta | date |
| alternate_contact | free text |
</Column>
</Columns>

**Flow:** confirm you are speaking to the right person without revealing details, name the pending document, capture when it will come.

**Measure:** verified rate, documents received by the promised date.

### Feedback and NPS

*Customer experience · outbound · Hinglish*

Collect a rating and one line on what to improve.

<Columns>
<Column>
#### Inputs (sheet columns)

| Key | Notes |
| --- | --- |
| customer_name | shared |
| order_id | primary id |
| delivered_on | shared |
</Column>
<Column>
#### Outputs (results)

| Key | Type and options |
| --- | --- |
| score | number 0 to 10 |
| reason | free text |
| issue | choice: NONE, LATE, DAMAGED, WRONG_ITEM, OTHER |
| follow_up | yes or no |
</Column>
</Columns>

**Flow:** ask for a 0 to 10 score, ask why in one line, offer a follow-up if there was a problem.

**Measure:** response rate, score trend, issues routed to the right team.

## Design your own

Most teams have a call nobody has named here. Answer five questions and you have an agent:

<Steps>
<Step title="Who are you calling, and why?">
This becomes the role and goal section.
</Step>
<Step title="What do you already know about them?">
These are your inputs.
</Step>
<Step title="What must you know when you hang up?">
These are your outputs. Add a status with fixed options.
</Step>
<Step title="What usually goes wrong on this call?">
Write a rule for each: busy, wrong person, dispute, bad line.
</Step>
<Step title="Where does the answer go?">
A download, a report, or your system through the API.
</Step>
</Steps>

Stuck? [Describe the call to us](/#pilot) and we will build the first version with you.
