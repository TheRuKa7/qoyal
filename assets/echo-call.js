/* Echo calls you: the website's "Try it" and the floating Echo badge ask for a mobile number,
 * show what happens to it in plain words, confirm it with a one-time code, then Echo phones the
 * person for about a minute.
 *
 * Settings, in the page before this file loads:
 *   window.ECHO_CALL = { api: 'https://<echo host>/public/demo', policy: 'legal/demo-calls.html' }
 * With no api the module stays off and the page keeps its in-browser preview, so a visitor never
 * reaches a step that cannot work. Add ?live=phone to the URL to try the whole flow with a test
 * backend in the page (the code is shown on screen and nothing is dialled).
 *
 * API (all JSON; the server enforces the limits, the page only explains them):
 *   POST {api}/otp      {phone, flow, consent: {version, at}}      -> {request_id, resend_after}
 *   POST {api}/verify   {request_id, code}                         -> {token, expires_in}
 *   POST {api}/call     {flow}  (Authorization: Bearer token)      -> {call_id}
 *   GET  {api}/call/:id (Authorization)                            -> {state: dialling|ringing|in_progress|ended|failed, seconds, reason}
 *   POST {api}/call/:id/end (Authorization)                        -> {}
 *   DELETE {api}/session (Authorization)                           -> {}   erase the number now
 * Errors come back as {error: "plain sentence"} with 4xx; 429 means a limit was reached.
 */
(function () {
  'use strict';
  var d = document, CFG = window.ECHO_CALL || {};
  var PREVIEW = /[?&]live=phone\b/.test(location.search);
  if (!CFG.api && !PREVIEW) return;
  var POLICY = CFG.policy || 'legal/demo-calls.html', CONSENT_VERSION = '2026-10-19', MAX = CFG.maxSeconds || 60;
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function track(type, extra) { try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: 'echo_call_' + type }, extra || {})); } catch (e) {} }

  /* ---------- backends ---------- */
  var real = {
    post: function (path, body, token) {
      return fetch(CFG.api.replace(/\/$/, '') + path, { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, token ? { Authorization: 'Bearer ' + token } : {}), body: JSON.stringify(body || {}) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (b) { if (!r.ok) throw new Error(b.error || (r.status === 429 ? 'You have reached the limit of demo calls for today.' : 'Something went wrong. Try again in a minute.')); return b; }); });
    },
    get: function (path, token) {
      return fetch(CFG.api.replace(/\/$/, '') + path, { headers: { Authorization: 'Bearer ' + token } }).then(function (r) { return r.json(); });
    },
    del: function (path, token) { return fetch(CFG.api.replace(/\/$/, '') + path, { method: 'DELETE', headers: { Authorization: 'Bearer ' + token } }); }
  };
  var mockCall = null;
  var mock = {
    post: function (path, body) {
      return new Promise(function (res, rej) {
        setTimeout(function () {
          if (path === '/otp') return res({ request_id: 'preview', resend_after: 30 });
          if (path === '/verify') return body.code === '246810' ? res({ token: 'preview-token', expires_in: 1800 }) : rej(new Error('That code is not right. Check the text and try again.'));
          if (path === '/call') { mockCall = { t0: Date.now() }; return res({ call_id: 'preview-call' }); }
          if (/\/end$/.test(path)) { if (mockCall) mockCall.ended = true; return res({}); }
          res({});
        }, 650);
      });
    },
    get: function () {
      var c = mockCall || { t0: Date.now() }, s = (Date.now() - c.t0) / 1000;
      var state = c.ended || s > 5.5 + MAX ? 'ended' : s < 1.5 ? 'dialling' : s < 5.5 ? 'ringing' : 'in_progress';
      return Promise.resolve({ state: state, seconds: Math.max(0, Math.round(s - 5.5)) });
    },
    del: function () { return Promise.resolve(); }
  };
  var api = PREVIEW && !CFG.api ? mock : real;

  /* ---------- session: a verified number stays usable for 30 minutes in this tab ---------- */
  var S = { token: '', phone: '', exp: 0 };
  try { var saved = JSON.parse(sessionStorage.getItem('echo-call') || '{}'); if (saved.exp > Date.now()) S = saved; } catch (e) {}
  function keep() { try { sessionStorage.setItem('echo-call', JSON.stringify(S)); } catch (e) {} }
  function forget() { S = { token: '', phone: '', exp: 0 }; try { sessionStorage.removeItem('echo-call'); } catch (e) {} }
  function masked(p) { return '+91 ' + p.slice(0, 2) + '••• ••' + p.slice(-3); }

  /* ---------- the dialog ---------- */
  var MARK = '<svg class="ec-mark" viewBox="-16 -16 96 96" aria-hidden="true"><path class="ec-g ec-g1" d="M-4.4 57.75A45.5 45.5 0 0 1 46.78 -8.95"/><path class="ec-g ec-g2" d="M2.53 53.75A37.5 37.5 0 0 1 44.71 -1.22"/>' +
    '<rect width="64" height="64" rx="15" fill="#047857"/><path d="M9.45 49.75A29.5 29.5 0 0 1 42.64 6.51" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".32"/>' +
    '<path d="M16.38 45.75A21.5 21.5 0 0 1 40.56 14.23" fill="none" stroke="#fff" stroke-width="4.4" stroke-linecap="round" opacity=".62"/><path d="M22.5 35H47.5M47.5 35A12.5 12.5 0 1 0 44.29 43.36" fill="none" stroke="#fff" stroke-width="6.4" stroke-linecap="round"/></svg>';
  var box = d.createElement('div');
  box.className = 'ec'; box.hidden = true; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ecTitle');
  box.innerHTML =
    '<div class="ec-bg" data-ec-close></div><div class="ec-box">' +
    '<button class="ec-x" type="button" data-ec-close aria-label="Close">×</button>' +
    '<div class="ec-head">' + MARK + '<div><p class="ec-k" id="ecK">Echo calls you</p><h2 id="ecTitle">Get a call from Echo</h2><p class="ec-sub" id="ecSub"></p></div></div>' +
    '<div class="ec-flows" id="ecFlows" role="radiogroup" aria-label="Which call"></div>' +
    /* step 1: number and notice */
    '<form class="ec-step" id="ecNum" novalidate>' +
    '<label class="ec-l" for="ecPhone">Your mobile number</label>' +
    '<div class="ec-phone"><span class="ec-cc">+91</span><input id="ecPhone" inputmode="numeric" autocomplete="tel-national" maxlength="10" placeholder="98765 43210" aria-describedby="ecNote" required></div>' +
    '<ul class="ec-note" id="ecNote"><li><b>One call, now.</b> Echo calls this number once, for about a minute.</li><li><b>Nothing is recorded.</b> No audio and no transcript are kept.</li>' +
    '<li><b>Used for this call only.</b> No sales calls, messages or lists. The number is deleted within 24 hours.</li></ul>' +
    '<p class="ec-more"><a href="' + POLICY + '" target="_blank" rel="noopener">How we handle your number</a> <span>· one page, plain words</span></p>' +
    '<button class="ec-go" type="submit">Confirm and send code</button>' +
    '<p class="ec-fine">By confirming you agree to one call from an AI agent on this number. It says it is an AI when it starts.</p>' +
    '</form>' +
    /* step 2: code */
    '<form class="ec-step" id="ecCode" hidden novalidate>' +
    '<label class="ec-l" for="ecOtp">Enter the 6 digit code sent to <b id="ecTo"></b></label>' +
    '<input class="ec-otp" id="ecOtp" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="••••••" required>' +
    '<p class="ec-row"><button type="button" class="ec-link" id="ecResend" disabled>Resend code</button><button type="button" class="ec-link" id="ecChange">Use another number</button></p>' +
    '<p class="ec-hint" id="ecHint" hidden></p>' +
    '<button class="ec-go" type="submit">Verify and call me</button>' +
    '</form>' +
    /* step 3: the call */
    '<div class="ec-step ec-calling" id="ecCall" hidden>' +
    '<div class="ec-live">' + MARK + '</div>' +
    '<p class="ec-state" id="ecState" aria-live="polite">Calling you</p><p class="ec-time mono" id="ecTime"></p>' +
    '<p class="ec-sub" id="ecCallSub"></p>' +
    '<button class="ec-end" type="button" id="ecEnd">End the call</button>' +
    '</div>' +
    /* step 4: done */
    '<div class="ec-step" id="ecDone" hidden>' +
    '<h3 id="ecDoneH">That was Echo.</h3><p class="ec-sub" id="ecDoneP">Want it on your own calls? Our team sets up a pilot on your list in two weeks.</p>' +
    '<div class="ec-acts"><a class="ec-go" href="#pilot" data-ec-close>Talk to an expert</a><button type="button" class="ec-link" id="ecAgain">Try another call</button><button type="button" class="ec-link" id="ecErase">Delete my number now</button></div>' +
    '</div>' +
    '<p class="ec-err" id="ecErr" role="alert" hidden></p>' +
    (PREVIEW && !CFG.api ? '<p class="ec-preview">Preview: no text is sent and nothing is dialled. Use code 246810.</p>' : '') +
    '<p class="ec-alt"><button type="button" class="ec-link" id="ecBrowser">Or try it in your browser instead</button></p>' +
    '</div>';
  d.body.appendChild(box);
  var st = { flow: null, trigger: null, req: '', callId: '', poll: 0, resendAt: 0, tick: 0 };
  function show(id) { ['ecNum', 'ecCode', 'ecCall', 'ecDone'].forEach(function (s) { $('#' + s, box).hidden = s !== id; }); err(''); }
  function err(m) { var e = $('#ecErr', box); e.textContent = m || ''; e.hidden = !m; }
  function busy(form, on) { var b = $('.ec-go', form); if (b) { b.disabled = on; b.classList.toggle('busy', on); } }

  /* the calls a visitor can pick: read from the hero list, so the copy lives in one place */
  function flows() {
    return Array.prototype.map.call(d.querySelectorAll('button[data-demo]'), function (b) {
      var t = $('.at b', b), s = $('.at small', b);
      return { id: b.getAttribute('data-demo'), title: t ? t.textContent : b.getAttribute('data-demo'), sub: s ? s.textContent : '' };
    }).filter(function (f, i, a) { return a.findIndex(function (x) { return x.id === f.id; }) === i; });
  }
  function setFlow(id) {
    var list = flows(), f = list.find(function (x) { return x.id === id; }) || list[0];
    st.flow = f;
    $('#ecSub', box).textContent = f ? f.title + (f.sub ? ' · ' + f.sub : '') : '';
    Array.prototype.forEach.call(box.querySelectorAll('.ec-flow'), function (b) { b.setAttribute('aria-checked', String(b.dataset.id === (f && f.id))); });
  }
  function open(flowId, trigger, pick) {
    st.trigger = trigger;
    var fl = $('#ecFlows', box);
    fl.innerHTML = pick ? flows().map(function (f) { return '<button type="button" role="radio" class="ec-flow" data-id="' + f.id + '">' + f.title + '</button>'; }).join('') : '';
    fl.hidden = !pick;
    setFlow(flowId);
    if (S.token && S.exp > Date.now()) { show('ecNum'); $('#ecPhone', box).value = S.phone; startCall(); }
    else show('ecNum');
    box.hidden = false; d.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(function () { box.classList.add('on'); (S.token ? $('#ecEnd', box) : $('#ecPhone', box)).focus({ preventScroll: true }); });
    track('open', { flow: st.flow && st.flow.id, via: pick ? 'badge' : 'try' });
  }
  function close() {
    if (box.hidden) return;
    if (st.callId && !$('#ecCall', box).hidden) endCall('closed');
    box.classList.remove('on'); box.hidden = true; d.documentElement.style.overflow = '';
    clearInterval(st.tick); if (st.trigger && st.trigger.focus) st.trigger.focus({ preventScroll: true });
  }
  box.addEventListener('click', function (e) {
    if (e.target.closest('[data-ec-close]')) { if (e.target.closest('a[href^="#"]')) { close(); return; } e.preventDefault(); close(); }
    var f = e.target.closest('.ec-flow'); if (f) setFlow(f.dataset.id);
  });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });

  /* step 1 -> 2 */
  $('#ecPhone', box).addEventListener('input', function (e) { e.target.value = e.target.value.replace(/\D/g, '').slice(0, 10); });
  $('#ecNum', box).addEventListener('submit', function (e) {
    e.preventDefault();
    var p = $('#ecPhone', box).value;
    if (!/^[6-9]\d{9}$/.test(p)) { err('Enter a 10 digit Indian mobile number.'); return; }
    busy(e.target, true); err('');
    api.post('/otp', { phone: '+91' + p, flow: st.flow && st.flow.id, consent: { version: CONSENT_VERSION, at: new Date().toISOString() } }).then(function (r) {
      st.req = r.request_id; S.phone = p; $('#ecTo', box).textContent = masked(p);
      show('ecCode'); $('#ecOtp', box).value = ''; $('#ecOtp', box).focus(); countdown(r.resend_after || 30);
      track('otp_sent', { flow: st.flow && st.flow.id });
    }).catch(function (x) { err(x.message); }).then(function () { busy(e.target, false); });
  });
  function countdown(sec) {
    var b = $('#ecResend', box); st.resendAt = Date.now() + sec * 1000; b.disabled = true;
    clearInterval(st.rt); st.rt = setInterval(function () {
      var left = Math.ceil((st.resendAt - Date.now()) / 1000);
      if (left <= 0) { clearInterval(st.rt); b.disabled = false; b.textContent = 'Resend code'; } else b.textContent = 'Resend code in ' + left + ' s';
    }, 250);
  }
  $('#ecResend', box).addEventListener('click', function () { $('#ecNum', box).requestSubmit ? $('#ecNum', box).requestSubmit() : $('#ecNum', box).dispatchEvent(new Event('submit')); });
  $('#ecChange', box).addEventListener('click', function () { forget(); show('ecNum'); $('#ecPhone', box).focus(); });
  /* step 2 -> 3 */
  $('#ecOtp', box).addEventListener('input', function (e) { e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6); if (e.target.value.length === 6) $('#ecCode .ec-go', box).focus(); });
  $('#ecCode', box).addEventListener('submit', function (e) {
    e.preventDefault();
    var code = $('#ecOtp', box).value; if (code.length !== 6) { err('Enter all 6 digits.'); return; }
    busy(e.target, true);
    api.post('/verify', { request_id: st.req, code: code }).then(function (r) {
      S.token = r.token; S.exp = Date.now() + (r.expires_in || 1800) * 1000; keep(); track('verified');
      startCall();
    }).catch(function (x) { err(x.message); }).then(function () { busy(e.target, false); });
  });
  /* the call */
  var LABEL = { dialling: 'Calling you', ringing: 'Your phone is ringing', in_progress: 'On the call', ended: 'Call ended', failed: 'The call did not go through' };
  function startCall() {
    show('ecCall'); var live = $('.ec-live', box); live.className = 'ec-live dialling';
    $('#ecState', box).textContent = LABEL.dialling; $('#ecTime', box).textContent = '';
    $('#ecCallSub', box).textContent = 'Calling ' + masked(S.phone) + '. Pick up to talk to ' + ((st.flow && st.flow.sub.split(' · ')[0]) || 'the agent') + '.';
    api.post('/call', { flow: st.flow && st.flow.id }, S.token).then(function (r) {
      st.callId = r.call_id; track('call_start', { flow: st.flow && st.flow.id });
      clearInterval(st.poll); st.poll = setInterval(poll, 1000); poll();
    }).catch(function (x) { if (/expired|sign in|token/i.test(x.message)) { forget(); show('ecNum'); } else { show('ecDone'); $('#ecDoneH', box).textContent = 'We could not call you.'; $('#ecDoneP', box).textContent = x.message; } });
  }
  function poll() {
    api.get('/call/' + st.callId, S.token).then(function (c) {
      var live = $('.ec-live', box); live.className = 'ec-live ' + c.state;
      $('#ecState', box).textContent = LABEL[c.state] || c.state;
      $('#ecTime', box).textContent = c.state === 'in_progress' ? fmt(c.seconds) + ' of ' + fmt(MAX) : '';
      if (c.state === 'ended' || c.state === 'failed') {
        clearInterval(st.poll); st.callId = ''; track('call_end', { state: c.state, seconds: c.seconds });
        show('ecDone'); $('#ecDoneH', box).textContent = c.state === 'failed' ? 'The call did not go through.' : 'That was Echo.';
        $('#ecDoneP', box).textContent = c.state === 'failed' ? (c.reason || 'Your phone may be switched off or busy. Try again in a minute.') : 'Want it on your own calls? Our team sets up a pilot on your list in two weeks.';
        $('.ec-acts .ec-go', box).focus();
      }
    }).catch(function () {});
  }
  function fmt(s) { s = Math.max(0, s | 0); return Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2); }
  function endCall(why) { if (!st.callId) return; api.post('/call/' + st.callId + '/end', {}, S.token).catch(function () {}); track('call_hangup', { why: why }); }
  $('#ecEnd', box).addEventListener('click', function () { endCall('button'); $('#ecState', box).textContent = 'Ending the call'; });
  $('#ecAgain', box).addEventListener('click', function () { var pick = flows(); $('#ecFlows', box).hidden = false; $('#ecFlows', box).innerHTML = pick.map(function (f) { return '<button type="button" role="radio" class="ec-flow" data-id="' + f.id + '">' + f.title + '</button>'; }).join(''); setFlow(st.flow && st.flow.id); startCall(); });
  $('#ecErase', box).addEventListener('click', function () {
    var t = S.token; forget(); if (t) api.del('/session', t).catch(function () {});
    $('#ecDoneP', box).textContent = 'Your number is deleted. Thanks for trying Echo.'; this.hidden = true; track('erase');
  });
  $('#ecBrowser', box).addEventListener('click', function () { var id = st.flow && st.flow.id, t = st.trigger; close(); if (window.echoOpenTry) window.echoOpenTry(id, t); });

  /* "Try it" buttons and the floating badge open this, before the page's own handlers */
  d.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('button[data-demo], [data-try], #badge');
    if (!t || t.closest('.ec')) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    var isBadge = t.id === 'badge';
    open(isBadge ? (flows()[0] || {}).id : (t.getAttribute('data-demo') || t.getAttribute('data-try')), t, isBadge);
  }, true);
  var badge = d.getElementById('badge');
  if (badge) { badge.setAttribute('aria-label', 'Get a call from Echo'); var tip = $('.tip', badge); if (tip) tip.textContent = 'Get a call from Echo'; }
  window.EchoCall = { open: open, close: close };
})();
