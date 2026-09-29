---
# Guide template: a task the reader completes step by step.
# Copy to content/docs/platform/<page-name>.md, add <page-name> to docs.yml, run: python tools/build.py serve
title: Do something specific                # the H1 and the <title>. Put the main keyword first.
description: One sentence, under 155 characters, that says what the reader can do after this page.
sidebarTitle: Short name                    # optional, a shorter label for the sidebar
keywords: [main keyword, second keyword]    # 2 to 4 phrases people search for
updated: 2026-09-29                         # shown as "Updated" and used in the sitemap
---

One or two sentences on who this is for and when to use it. Use the main keyword naturally here.

<Note title="Before you start">What must already be in place, such as a workspace or a calling line.</Note>

## Step by step

<Steps>
<Step title="First action">
What to click, in **bold**, and what happens.
</Step>
<Step title="Second action">
Next action. Link to related pages like [Campaigns](campaigns) or [Webhooks](../developers/webhooks).
</Step>
</Steps>

![Describe what the screenshot shows](assets/placeholder.svg "Caption: what to look at. Save real screenshots in content/docs/platform/assets/<page-name>/")

<Warning title="This affects real calls">Say plainly when an action dials numbers, costs money or cannot be undone.</Warning>

## Check it worked

<Check>What the reader sees when it worked.</Check>

## Next steps

<CardGroup cols="2">
<Card title="Related page" href="quickstart" eyebrow="Get started">Why they would go there next.</Card>
<Card title="Another page" href="campaigns" eyebrow="Launch">One line.</Card>
</CardGroup>
