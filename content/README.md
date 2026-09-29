# Echo content: docs and blog in Markdown

Write Markdown here. `tools/build.py` turns it into the HTML pages under `docs/` and `blog/`.
Never edit the generated `.html` files in `docs/` or `blog/`; they are overwritten on every build.

```
content/
├── README.md                  this guide
├── site.yml                   site name, base URL, top nav, footer (shared by every page)
├── components.html            ALL reusable components, one file (Note, Steps, Tabs, Endpoint ...)
├── snippets/                  shared text, reused with <Snippet file="name.md"/>
│   └── compliance-gate.md
├── docs/
│   ├── docs.yml               sidebar: tabs, groups and page order
│   ├── _templates/            starting points, never built
│   │   ├── guide.md           a task, step by step
│   │   ├── concept.md         an idea explained
│   │   ├── workflow.md        one business workflow (playbook)
│   │   └── api-reference.md   API endpoints, Swagger style
│   ├── platform/              Platform guide (no code)  →  /docs/<page>.html
│   │   ├── index.md           /docs/
│   │   ├── quickstart.md      /docs/quickstart.html
│   │   ├── ...
│   │   └── assets/            images for these pages    →  /docs/assets/
│   └── developers/            Developers (API)          →  /docs/developers/<page>.html
│       ├── index.md
│       ├── ...
│       └── assets/                                      →  /docs/developers/assets/
└── blog/
    ├── blog.yml               blog title, categories, authors, page size, call to action
    ├── _template.md           copy this to start a post
    ├── posts/                 one .md per post          →  /blog/<file-name>.html
    └── assets/                post images               →  /blog/assets/
```

## Build and preview

```bash
pip install -r tools/requirements.txt
python tools/build.py serve     # prints the preview URL, rebuilds when you save
python tools/build.py check     # problems only: broken links, missing images, missing fields
python tools/build.py           # write the site, then commit
```

The preview also shows every component with its Markdown at `/docs/_components.html`, and every
template rendered at `/docs/_preview/`.

## Add a docs page

1. Copy a file from `content/docs/_templates/` into `content/docs/platform/` or `content/docs/developers/`.
   The file name becomes the URL: `sso-setup.md` → `/docs/sso-setup.html`.
2. Fill in the frontmatter: `title`, `description` (under 155 characters), `updated`, and optionally `keywords` (used only to plan the page; never published). Add `status: soon` (and optionally `soon_note`) for anything not in the product yet: the page gets a Coming soon tag and notice.
3. Add the file name (without `.md`) to a group in `content/docs/docs.yml`. The order there is the sidebar order
   and the Previous / Next order. `{page: sso-setup, badge: New}` adds a badge.
4. Run `python tools/build.py check`.

New group: add `- group: Name` with `pages: [...]` in docs.yml. New top tab (a third doc set): add a tab with its
own `folder` and `output`.

## Links and images

- Another page in the same set: `[Campaigns](campaigns)`. The other set: `[Webhooks](../developers/webhooks)`.
- A section: `[Retries](../developers/webhooks#retries)`. Heading ids come from the heading text; set your own with `## Retries {#retries}`.
- The home page or any site path: `[Talk to an expert](/#pilot)`, `[Blog](/blog/)`.
- Images: put them in the set's `assets/` folder, in a folder per page, and link relatively:
  `![Alt text](assets/quickstart/upload.png "Caption")`. With a caption the image gets a frame.
  Width and height are added automatically, and images load lazily.
- The build fails on a broken link or a missing image, so nothing ships broken.

## Components

Use them like HTML tags inside Markdown. Markdown works inside them.

| Component | For |
| --- | --- |
| `<Note>` `<Tip>` `<Info>` `<Warning>` `<Check>` | callouts, optional `title` |
| `<Steps>` + `<Step title>` | numbered procedures |
| `<Tabs>` + `<Tab title>` | alternatives, such as No code / API |
| `<CardGroup cols>` + `<Card title href eyebrow>` | link grids |
| `<Columns>` + `<Column>` | side by side |
| `<Accordion title>` / `<AccordionGroup>` | FAQs and details |
| `<Frame caption>` | screenshots and diagrams |
| `<CodeGroup title>` | several code blocks as tabs: ```` ```bash cURL ```` |
| `<Endpoint method path title>` | one API operation, with |
| `<Params title>` + `<ParamField name type required default>` / `<ResponseField>` | its fields |
| `<RequestExample>` / `<ResponseExample status>` | its samples, shown in the right column |
| `<Update label date tags>` | changelog entries |
| `<Badge tone>` `<Method name/>` `<Term tip>` | inline labels and explained terms |
| `<Snippet file/>` | shared text from `content/snippets/` |

To add or change a component, edit `content/components.html` (its template, docs and example live together)
and its styles in `assets/docs.css`.

## What every page gets automatically

- Title, description, canonical URL, Open Graph and Twitter tags, `og:locale`.
- JSON-LD: TechArticle (docs) or BlogPosting (blog), BreadcrumbList, and FAQPage when the frontmatter has `faq:`.
- "Updated" date, reading time, table of contents, heading anchors, previous and next links.
- A **Copy page** button that copies the page as plain text. No Markdown copies are published, and keywords stay out of the HTML.
- `sitemap.xml`, `robots.txt`, `llms.txt` (titles and summaries only) and `search.json` for the built-in search (Ctrl K or /).
- Syntax highlighting at build time, so pages ship with no highlighting library.

## Blog

1. Copy `content/blog/_template.md` to `content/blog/posts/<post-slug>.md`.
2. Pick `author` and `category` from `content/blog/blog.yml` (add new ones there).
3. Keep `draft: true` while it is reviewed: drafts build with `noindex` and stay off the index, feed and sitemap.
4. Remove `draft` to publish. The index, category pages, pagination, related posts and the home page row update.
