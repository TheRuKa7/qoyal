# Updating the Echo site

Static site, no build step. After any docs or blog change run:

    python tools/site.py          # sidebars, previous/next, blog index, sitemap.xml, llms.txt
    python tools/site.py --check  # report problems only

## Use cases and demos (index.html)

Each use case card is an `li[data-demo="<id>"]` in `#t10`. Its copy lives in the card's
`data-title`, `data-group`, `data-lang`, `data-problem`, `data-does` and `data-outcome`.
The demo sheet reads those, so edit the card and the sheet follows.

Recordings and live availability live in one place, `<script id="demoManifest">` near the end of index.html:

    "poacc": { "rec": "assets/calls/post-po-acceptance.mp3", "live": true }

- `rec`: path to an MP3 (mono, 64 to 96 kbps, under 2 MB). `null` shows "on its way" plus an interactive preview link.
- `live`: this flow gets a Try live button once a live transport is registered (below).
- Recordings must be cleared first: no real names, phone numbers, company names, PO or invoice numbers, and consent on file.

## Live web demos (WebRTC)

The UI is built: mic permission, connecting, a 1 minute countdown, mute, end, then Talk to an expert / Try the platform.
It carries no audio itself. Register a transport and name it in `window.ECHO_DEMO.transport`:

    EchoDemo.registerTransport('webrtc', function () {
      return {
        connect: function (ctx) { /* ctx.flow, ctx.stream (mic), ctx.maxSeconds,
                                     ctx.onRemoteLevel(0..1), ctx.onEnd(reason), ctx.onState(text)
                                     resolve once audio flows */ },
        setMuted: function (muted) {},
        disconnect: function () {}
      };
    });

The contract is documented at the top of `assets/echo-demo.js`. The server side (session token, the agent,
the 60 second cap enforced on the server) is not built yet. Add `?live=mock` to the page URL to walk through the UI
with a silent test transport. Every step fires an `echo:demo` DOM event and a `dataLayer` push for analytics.

## Docs

1. Copy `docs/_template.html` to `docs/<page>.html` (or `docs/developers/<page>.html`).
2. Add `{"file": "<page>.html", "title": "Page title"}` to the right group in `docs/nav.json`.
   Add `"new": true` for a New badge in the sidebar. New groups are fine too.
3. Screenshots: `docs/img/<page>/<screen>.png`, about 1600 px wide, inside `<figure class="shot">`.
   No screenshot yet? `<figure class="shot pending"><div class="shot-ph">Screenshot: name</div>...`
4. Run `python tools/site.py`. It warns about missing files and missing screenshots.

## Blog

The blog ships empty. Marketing adds posts:

1. Copy `blog/_template.html` to `blog/<slug>.html`, fill it in, set robots to `index,follow`.
2. Images in `blog/img/<slug>/`.
3. Add an entry to `blog/posts.json`:
   `{"url": "<slug>.html", "title": "", "summary": "", "category": "Guide", "date": "2026-10-01", "minutes": 6, "image": "img/<slug>/cover.png"}`
   `"draft": true` keeps it off the index and the home page.
4. Run `python tools/site.py`. The home page shows the latest three posts once any exist.

## Forms

`ECHO_CONFIG` at the top of the main script: `PILOT_ENDPOINT` or `PILOT_EMAIL`. The form now also sends
`intent` (`expert` or `platform`). `window.ECHO_DEMO.platformUrl` sets where Try the platform goes.
