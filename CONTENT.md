# Updating the Echo site

The home page (`index.html`) is edited directly. Docs and blog are written in Markdown and built:

    pip install -r tools/requirements.txt
    python tools/build.py serve   # preview while you write
    python tools/build.py         # build before you commit

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

## Docs and blog

Docs and blog posts are written in Markdown in `content/` and built with `python tools/build.py`.
Everything about them (file structure, sidebar order, components, templates, images, SEO, preview)
is in [content/README.md](content/README.md).

## Forms

`ECHO_CONFIG` at the top of the main script: `PILOT_ENDPOINT` or `PILOT_EMAIL`. The form now also sends
`intent` (`expert` or `platform`). `window.ECHO_DEMO.platformUrl` sets where Try the platform goes.
