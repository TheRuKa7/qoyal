/* Echo demo sheet: sample call player and a one-minute live call.
 *
 * What is here
 *   - DemoSheet   the dialog. Opens from any element with data-demo="<flow id>".
 *                 Reads the flow's copy from the matching use case card (li[data-demo]).
 *   - RecPlayer   plays a sample recording with a level meter. No transcript.
 *   - LiveCall    a one-minute call UI: mic permission, connecting, live, ended.
 *                 It does not carry audio itself. It hands the mic stream to a transport.
 *
 * Content lives in the page, in <script type="application/json" id="demoManifest">:
 *   { "poacc": { "rec": "assets/calls/post-po-acceptance.mp3", "live": true }, ... }
 *   rec   path to a recording, or null while it is not cleared for publishing
 *   live  true when a live agent can take a web call for this flow
 *
 * Transports. Live calls stay hidden until one is registered:
 *   EchoDemo.registerTransport('webrtc', function (opts) {
 *     return {
 *       connect: function (ctx) {  // ctx: {flow, stream, maxSeconds, onState, onRemoteLevel, onEnd}
 *         // create the RTCPeerConnection or SDK room, add ctx.stream tracks,
 *         // play remote audio, call ctx.onRemoteLevel(0..1) as the agent speaks,
 *         // call ctx.onEnd('remote') if the agent hangs up. Resolve once audio flows.
 *         return Promise.resolve();
 *       },
 *       setMuted: function (muted) {},
 *       disconnect: function () {}
 *     };
 *   });
 *   window.ECHO_DEMO = { transport: 'webrtc' };   // before this file loads, or call EchoDemo.useTransport('webrtc')
 * Add ?live=mock to the URL to preview the live flow with a silent test transport.
 *
 * Analytics: every step fires a DOM event 'echo:demo' with {type, flow, ...} and pushes to window.dataLayer.
 */
(function () {
  'use strict';
  var d = document;
  var CFG = window.ECHO_DEMO || {};
  var MAX = CFG.maxSeconds || 60;
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sheet = d.getElementById('demo');
  if (!sheet) return;
  function $(s, c) { return (c || d).querySelector(s); }
  function emit(type, extra) {
    var detail = Object.assign({ type: type, flow: state.id }, extra || {});
    try { d.dispatchEvent(new CustomEvent('echo:demo', { detail: detail })); } catch (e) {}
    try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: 'echo_demo_' + type }, detail)); } catch (e) {}
  }
  var manifest = {};
  try { manifest = JSON.parse((d.getElementById('demoManifest') || {}).textContent || '{}'); } catch (e) {}

  /* ---------- transports ---------- */
  var transports = {}, active = null;
  function registerTransport(name, factory) { transports[name] = factory; if (CFG.transport === name) active = name; refreshLive(); }
  function useTransport(name) { active = transports[name] ? name : null; refreshLive(); }
  registerTransport('mock', function () {
    var t0 = 0, raf = 0, muted = false, stop = false;
    return {
      mock: true,
      connect: function (ctx) {
        return new Promise(function (res) {
          setTimeout(function () {
            t0 = performance.now();
            (function tick(now) {
              if (stop) return;
              var s = (now - t0) / 1000, talking = (s % 7) < 3.6;
              ctx.onRemoteLevel(talking ? 0.35 + 0.35 * Math.abs(Math.sin(s * 9)) * Math.abs(Math.sin(s * 2.3)) : 0.04);
              raf = requestAnimationFrame(tick);
            })(performance.now());
            res();
          }, 1100);
        });
      },
      setMuted: function (m) { muted = m; },
      disconnect: function () { stop = true; cancelAnimationFrame(raf); }
    };
  });
  if (/[?&]live=mock\b/.test(location.search)) active = 'mock';

  /* ---------- sheet ---------- */
  var state = { id: null, trigger: null, card: null };
  var el = {
    k: $('#dmK'), t: $('#dmT'), lang: $('#dmLang'), tabs: $('#dmTabs'),
    tabRec: $('#dmTabRec'), tabLive: $('#dmTabLive'), paneRec: $('#dmRec'), paneLive: $('#dmLive'),
    p: $('#dmP'), a: $('#dmA'), o: $('#dmO'), end: $('#dmEnd'), endH: $('#dmEndH'), body: $('#dmBody')
  };
  function flowOf(id) { return manifest[id] || {}; }
  function liveReady(id) { return !!(active && flowOf(id).live); }
  function refreshLive() {
    var on = !!active;
    Array.prototype.forEach.call(d.querySelectorAll('[data-demo-live]'), function (b) {
      b.hidden = !(on && flowOf(b.getAttribute('data-demo-live')).live);
    });
    if (state && state.id) el.tabLive.hidden = !liveReady(state.id);
  }
  function open(id, trigger, mode) {
    /* no recording and no live call for this flow yet: go straight to the interactive preview */
    if (mode === 'rec' && !flowOf(id).rec && !(active && flowOf(id).live) && window.echoOpenTry && d.getElementById('try')) { window.echoOpenTry(id, trigger); return true; }
    var card = d.querySelector('li[data-demo="' + id + '"]');
    if (!card) return false;
    state.id = id; state.trigger = trigger; state.card = card;
    var c = card.dataset;
    el.k.textContent = c.group || '';
    el.t.textContent = c.title || '';
    el.lang.textContent = c.lang || '';
    el.p.textContent = c.problem || '';
    el.a.textContent = c.does || '';
    el.o.textContent = c.outcome || '';
    el.end.hidden = true; el.body.hidden = false;
    el.tabLive.hidden = !liveReady(id);
    rec.load(flowOf(id).rec || null, id);
    live.reset();
    tab(mode === 'live' && liveReady(id) ? 'live' : 'rec');
    sheet.hidden = false;
    d.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(function () { sheet.classList.add('on'); });
    (mode === 'live' && liveReady(id) ? el.tabLive : $('.dm-x', sheet)).focus({ preventScroll: true });
    emit('open', { mode: mode || 'rec' });
    return true;
  }
  function close() {
    if (sheet.hidden) return;
    rec.stop(); live.hangup('closed');
    sheet.classList.remove('on');
    sheet.hidden = true;
    d.documentElement.style.overflow = '';
    if (state.trigger && state.trigger.focus) state.trigger.focus({ preventScroll: true });
    emit('close');
  }
  function tab(which) {
    var isLive = which === 'live';
    el.tabRec.setAttribute('aria-selected', String(!isLive));
    el.tabLive.setAttribute('aria-selected', String(isLive));
    el.paneRec.hidden = isLive; el.paneLive.hidden = !isLive;
    if (isLive) rec.stop(); else live.hangup('tab');
  }
  function finish(kind) {
    el.endH.textContent = kind === 'live' ? 'That was a live Echo call.' : 'Put this agent on your calls.';
    el.body.hidden = true; el.end.hidden = false;
    $('button, a', el.end).focus({ preventScroll: true });
    emit('end', { via: kind });
  }

  /* ---------- level bars (shared by both panes) ---------- */
  function Bars(canvas) {
    var ctx = canvas.getContext('2d'), n = 44, v = new Array(n).fill(0.06), seed = [];
    for (var i = 0; i < n; i++) seed.push(0.12 + 0.5 * Math.abs(Math.sin(i * 1.7) * Math.cos(i * 0.43)));
    function size() {
      var r = canvas.getBoundingClientRect(), dp = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, r.width * dp); canvas.height = Math.max(1, r.height * dp);
    }
    function draw(level, progress, idle) {
      if (!canvas.width) size();
      var w = canvas.width, h = canvas.height, bw = w / n, cs = getComputedStyle(canvas);
      var on = cs.getPropertyValue('--bar-on').trim() || '#c8102e', off = cs.getPropertyValue('--bar-off').trim() || '#bbb';
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < n; i++) {
        var target = idle ? seed[i] : Math.min(1, level * (0.55 + 0.9 * Math.random()));
        v[i] += (target - v[i]) * (idle ? 1 : 0.35);
        var bh = Math.max(h * 0.06, v[i] * h * 0.9);
        ctx.fillStyle = progress != null ? (i / n <= progress ? on : off) : on;
        ctx.globalAlpha = progress != null ? 1 : 0.35 + 0.65 * v[i];
        ctx.fillRect(i * bw + bw * 0.22, (h - bh) / 2, bw * 0.56, bh);
      }
      ctx.globalAlpha = 1;
    }
    window.addEventListener('resize', function () { canvas.width = 0; });
    return { draw: draw };
  }
  function fmt(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2); }

  /* ---------- RecPlayer ---------- */
  var rec = (function () {
    var box = el.paneRec, btn = $('.dm-play', box), time = $('.dm-time', box), note = $('.dm-note', box);
    var bars = Bars($('canvas', box)), audio = new Audio(), ac = null, an = null, buf = null, raf = 0, src = null;
    audio.preload = 'none';
    function level() {
      if (!an) return audio.paused ? 0 : 0.5;
      an.getByteTimeDomainData(buf);
      var m = 0; for (var i = 0; i < buf.length; i++) m = Math.max(m, Math.abs(buf[i] - 128));
      return Math.min(1, m / 70);
    }
    function loop() {
      var p = audio.duration ? audio.currentTime / audio.duration : 0;
      bars.draw(RM ? 0.3 : level(), p, false);
      time.textContent = fmt(audio.currentTime) + (audio.duration ? ' / ' + fmt(audio.duration) : '');
      if (!audio.paused) raf = requestAnimationFrame(loop);
    }
    function ui(playing) { btn.setAttribute('aria-pressed', String(playing)); btn.setAttribute('aria-label', playing ? 'Pause sample call' : 'Play sample call'); box.classList.toggle('playing', playing); }
    audio.addEventListener('play', function () { ui(true); cancelAnimationFrame(raf); loop(); });
    audio.addEventListener('pause', function () { ui(false); });
    audio.addEventListener('ended', function () { ui(false); emit('rec_complete'); finish('rec'); });
    audio.addEventListener('error', function () { if (src) { box.classList.add('none'); note.textContent = 'This recording could not load. Talk to an expert to hear the agent on a call.'; } });
    btn.addEventListener('click', function () {
      if (!src) return;
      if (audio.paused) {
        try {
          if (!ac && window.AudioContext) {
            ac = new AudioContext(); an = ac.createAnalyser(); an.fftSize = 512; buf = new Uint8Array(an.fftSize);
            ac.createMediaElementSource(audio).connect(an); an.connect(ac.destination);
          }
          if (ac && ac.state === 'suspended') ac.resume();
        } catch (e) { an = null; }
        audio.play().then(function () { emit('rec_play'); }).catch(function () {});
      } else audio.pause();
    });
    $('canvas', box).addEventListener('click', function (e) {
      if (!audio.duration) return;
      var r = e.currentTarget.getBoundingClientRect();
      audio.currentTime = audio.duration * (e.clientX - r.left) / r.width; loop();
    });
    return {
      load: function (path, id) {
        this.stop(); src = path;
        box.classList.toggle('none', !path);
        btn.disabled = !path;
        if (path) { audio.src = path; note.textContent = 'Sample call' + (el.lang.textContent ? ' · ' + el.lang.textContent : ''); time.textContent = '0:00'; }
        else { audio.removeAttribute('src'); note.textContent = 'The sample recording for this flow is on its way. Talk to an expert to hear the agent on a call today.'; time.textContent = ''; }
        var pv = $('.dm-preview', box);   /* the older scripted preview, offered only while a recording is missing */
        pv.hidden = !!path || !d.getElementById('try');
        pv.setAttribute('data-try', id);
        requestAnimationFrame(function () { bars.draw(0, path ? 0 : null, true); });
      },
      stop: function () { if (!audio.paused) audio.pause(); try { audio.currentTime = 0; } catch (e) {} cancelAnimationFrame(raf); }
    };
  })();

  /* ---------- LiveCall ---------- */
  var live = (function () {
    var box = el.paneLive, go = $('.dm-go', box), st = $('.dm-st', box), tm = $('.dm-clock', box), ring = $('.dm-ring circle.fg', box);
    var mute = $('.dm-mute', box), hang = $('.dm-hang', box), badge = $('.dm-test', box), me = $('.dm-me i', box);
    var bars = Bars($('canvas', box)), C = 2 * Math.PI * 46;
    var s = null;  // {phase, stream, t, timer, raf, remote, local, an, buf}
    ring.style.strokeDasharray = C;
    function phase(p, msg) {
      box.setAttribute('data-phase', p);
      if (msg != null) st.textContent = msg;
      if (s) s.phase = p;
      emit('live_' + p);
    }
    function tickDraw() {
      if (!s || s.phase !== 'live') return;
      var left = Math.max(0, MAX - (performance.now() - s.t) / 1000);
      tm.textContent = fmt(left);
      ring.style.strokeDashoffset = C * (1 - left / MAX);
      var loc = 0;
      if (s.an) { s.an.getByteTimeDomainData(s.buf); for (var i = 0; i < s.buf.length; i++) loc = Math.max(loc, Math.abs(s.buf[i] - 128)); loc = Math.min(1, loc / 60); }
      me.style.transform = 'scaleX(' + (s.muted ? 0 : loc) + ')';
      bars.draw(RM ? 0.25 : s.remote, null, false);
      if (left <= 0) { hangup('timeout'); return; }
      s.raf = requestAnimationFrame(tickDraw);
    }
    function start() {
      if (!liveReady(state.id) || (s && s.phase !== 'ended')) return;
      s = { phase: 'idle', remote: 0, muted: false };
      var run = s;
      phase('mic', 'Allow the microphone to start');
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { phase('error', 'This browser cannot open the microphone. Hear the sample call instead.'); return; }
      navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } }).then(function (stream) {
        if (run !== s) { stream.getTracks().forEach(function (t) { t.stop(); }); return; }
        s.stream = stream;
        try { var ac = new AudioContext(); s.ac = ac; s.an = ac.createAnalyser(); s.an.fftSize = 512; s.buf = new Uint8Array(512); ac.createMediaStreamSource(stream).connect(s.an); } catch (e) {}
        phase('connecting', 'Connecting to the agent');
        s.tr = transports[active]({ flow: state.id });
        badge.hidden = !s.tr.mock;
        return s.tr.connect({
          flow: state.id, stream: stream, maxSeconds: MAX,
          onState: function (m) { if (run === s && s.phase === 'live') st.textContent = m; },
          onRemoteLevel: function (v) { if (run === s) s.remote = v; },
          onEnd: function (why) { if (run === s) hangup(why || 'remote'); }
        }).then(function () {
          if (run !== s) return;
          s.t = performance.now();
          phase('live', s.tr.mock ? 'Test mode: no audio. The live agent plugs in here.' : 'You are on the call. Speak normally.');
          tickDraw();
        });
      }).catch(function (e) {
        if (run !== s) return;
        var denied = e && (e.name === 'NotAllowedError' || e.name === 'SecurityError');
        phase('error', denied ? 'Microphone blocked. Allow it in the address bar, or hear the sample call.' : 'Could not connect just now. Please try again in a minute.');
        cleanup();
      });
    }
    function cleanup() {
      if (!s) return;
      cancelAnimationFrame(s.raf);
      try { s.tr && s.tr.disconnect(); } catch (e) {}
      if (s.stream) s.stream.getTracks().forEach(function (t) { t.stop(); });
      try { s.ac && s.ac.close(); } catch (e) {}
    }
    function hangup(why) {
      if (!s || s.phase === 'ended' || s.phase === 'idle') return;
      var was = s.phase, secs = s.t ? Math.round((performance.now() - s.t) / 1000) : 0;
      cleanup(); phase('ended', '');
      emit('live_hangup', { why: why, seconds: secs });
      if (was === 'live' && why !== 'closed' && why !== 'tab') finish('live');
      else reset();
    }
    function reset() {
      if (s && s.phase !== 'ended') cleanup();
      s = null; box.setAttribute('data-phase', 'idle');
      st.textContent = 'Up to ' + Math.round(MAX / 60) + ' minute. Your browser will ask for the microphone.';
      tm.textContent = fmt(MAX); ring.style.strokeDashoffset = 0; badge.hidden = true;
      mute.setAttribute('aria-pressed', 'false'); mute.textContent = 'Mute';
      requestAnimationFrame(function () { bars.draw(0, null, true); });
    }
    go.addEventListener('click', start);
    hang.addEventListener('click', function () { hangup('user'); });
    mute.addEventListener('click', function () {
      if (!s || s.phase !== 'live') return;
      s.muted = !s.muted;
      if (s.stream) s.stream.getAudioTracks().forEach(function (t) { t.enabled = !s.muted; });
      try { s.tr.setMuted(s.muted); } catch (e) {}
      mute.setAttribute('aria-pressed', String(s.muted)); mute.textContent = s.muted ? 'Unmute' : 'Mute';
    });
    return { reset: reset, hangup: hangup };
  })();

  /* ---------- wiring ---------- */
  d.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-demo],[data-demo-live]');
    if (b && !b.matches('li')) {
      var id = b.getAttribute('data-demo') || b.getAttribute('data-demo-live');
      if (open(id, b, b.hasAttribute('data-demo-live') ? 'live' : 'rec')) e.preventDefault();
      return;
    }
    var card = e.target.closest && e.target.closest('li[data-demo]');
    if (card && !e.target.closest('a,button')) open(card.getAttribute('data-demo'), card, 'rec');
  });
  d.addEventListener('keydown', function (e) {   /* cards: Enter or Space opens the sheet unless the page already turns keys into clicks */
    var card = e.target.closest && e.target.closest('li[data-demo] .hx');
    if (card && (e.key === 'Enter' || e.key === ' ') && e.target === card && !e.defaultPrevented) { e.preventDefault(); open(card.parentNode.getAttribute('data-demo'), card, 'rec'); }
  });
  el.tabRec.addEventListener('click', function () { tab('rec'); });
  el.tabLive.addEventListener('click', function () { tab('live'); });
  el.tabs.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var t = e.target === el.tabRec && !el.tabLive.hidden ? el.tabLive : el.tabRec; t.click(); t.focus();
  });
  Array.prototype.forEach.call(sheet.querySelectorAll('[data-dm-close]'), function (b) { b.addEventListener('click', close); });
  $('.dm-again', sheet).addEventListener('click', function () { el.end.hidden = true; el.body.hidden = false; live.reset(); rec.stop(); });
  function formFor(intent) {
    var i = d.querySelector('#pilotForm input[name=intent]'), h = d.querySelector('#pilotForm h3');
    if (i) i.value = intent;
    if (h) h.textContent = intent === 'platform' ? 'Get access to the platform' : 'Talk to an expert';
  }
  $('.dm-expert', sheet).addEventListener('click', function (e) {
    e.preventDefault(); var id = state.id; close();
    var sel = d.querySelector('#pilotForm select[name=usecase]'), map = CFG.usecaseMap || {};
    if (sel && map[id]) sel.value = map[id];
    formFor('expert');
    var p = d.getElementById('pilot'); if (p) p.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
    emit('cta', { cta: 'expert', flow: id });
  });
  $('.dm-platform', sheet).addEventListener('click', function (e) {
    var id = state.id, url = CFG.platformUrl || '';
    emit('cta', { cta: 'platform', flow: id });
    if (url && url.charAt(0) !== '#') return;   // a real URL: let the link open
    e.preventDefault(); close();
    formFor('platform');
    var p = d.getElementById('pilot'); if (p) p.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
  });
  if (CFG.platformUrl && CFG.platformUrl.charAt(0) !== '#') $('.dm-platform', sheet).href = CFG.platformUrl;
  $('.dm-preview', sheet).addEventListener('click', function () { close(); });   /* the page's [data-try] handler opens the preview */
  sheet.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { close(); return; }
    if (e.key !== 'Tab') return;
    var f = Array.prototype.filter.call(sheet.querySelectorAll('button,a[href],canvas[tabindex]'), function (x) { return x.offsetParent !== null && !x.disabled; });
    if (!f.length) return;
    if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  });

  window.EchoDemo = { open: open, close: close, registerTransport: registerTransport, useTransport: useTransport, manifest: manifest };
  refreshLive();
})();
