/* Echo docs and blog: tabs, copy, theme, menu, search, scroll-spy. No dependencies. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  var base = (function () { var s = d.querySelector('script[src$="docs.js"]'); return s ? s.getAttribute('src').replace(/assets\/docs\.js$/, '') : ''; })();

  /* tabs and code groups: panels are direct children carrying data-title */
  var syncing = false;
  $$('[data-tabs]').forEach(function (g) {
    var panels = $$(':scope > .c-tab, :scope > .c-code', g), btns = $$(':scope > .c-tabbar button', g);
    function show(i) {
      panels.forEach(function (p, k) { p.classList.toggle('on', k === i); });
      btns.forEach(function (b, k) { b.setAttribute('aria-selected', String(k === i)); b.tabIndex = k === i ? 0 : -1; });
    }
    btns.forEach(function (b, k) {
      b.addEventListener('click', function () {
        show(k);
        if (syncing) return;
        try { localStorage.setItem('echo-tab', b.textContent); } catch (e) {}
        /* keep the same language across every code group on the page */
        syncing = true;
        $$('[data-tabs] .c-tabbar button').forEach(function (o) { if (o !== b && o.textContent === b.textContent) o.click(); });
        syncing = false;
      });
      b.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        var n = (k + (e.key === 'ArrowRight' ? 1 : btns.length - 1)) % btns.length; btns[n].focus(); btns[n].click();
      });
    });
    var pref = null; try { pref = localStorage.getItem('echo-tab'); } catch (e) {}
    var i = btns.map(function (b) { return b.textContent; }).indexOf(pref);
    show(i >= 0 ? i : 0);
  });

  /* copy buttons */
  d.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.c-copy'); if (!b) return;
    var code = b.closest('.c-code').querySelector('pre').innerText;
    (navigator.clipboard ? navigator.clipboard.writeText(code) : Promise.reject()).then(function () {
      b.textContent = 'Copied'; b.classList.add('ok'); setTimeout(function () { b.textContent = 'Copy'; b.classList.remove('ok'); }, 1500);
    }).catch(function () { b.textContent = 'Select and copy'; });
  });

  /* copy the whole page as plain text: title, summary and article */
  $$('[data-copy-page]').forEach(function (b) {
    var label = b.querySelector('span');
    b.addEventListener('click', function () {
      var main = b.closest('main') || d.body, art = main.querySelector('.d-prose'), h1 = main.querySelector('h1'), lede = main.querySelector('.lede');
      var clone = art.cloneNode(true);
      $$('.c-copy, .c-tabbar, .h-anchor, script, style', clone).forEach(function (x) { x.remove(); });
      var txt = [h1 && h1.innerText, lede && lede.innerText, clone.innerText].filter(Boolean).join('\n\n').replace(/\n{3,}/g, '\n\n').trim() + '\n\nSource: ' + location.href.split('#')[0];
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () {
        label.textContent = 'Copied'; b.classList.add('ok'); setTimeout(function () { label.textContent = 'Copy page'; b.classList.remove('ok'); }, 1600);
      }).catch(function () { label.textContent = 'Copy failed'; });
    });
  });

  /* theme */
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var dark = root.getAttribute('data-theme') ? root.getAttribute('data-theme') === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      var next = dark ? 'light' : 'dark'; root.setAttribute('data-theme', next);
      try { localStorage.setItem('echo-theme', next); } catch (e) {}
    });
  });

  /* mobile menu */
  var side = d.getElementById('dSide'), mb = d.querySelector('[data-menu]');
  if (side && mb) {
    mb.addEventListener('click', function () { var o = !side.classList.contains('open'); side.classList.toggle('open', o); mb.setAttribute('aria-expanded', String(o)); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && side.classList.contains('open')) { side.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); mb.focus(); } });
    var cur = side.querySelector('[aria-current="page"]'); if (cur) side.scrollTop = Math.max(0, cur.offsetTop - side.clientHeight / 2);
  } else if (mb) mb.hidden = true;

  /* table of contents follows the reader */
  var toc = $$('.d-toc a[href^="#"]');
  if (toc.length && 'IntersectionObserver' in window) {
    var map = {}, vis = {};
    toc.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) { vis[x.target.id] = x.isIntersecting; });
      var first = Object.keys(map).filter(function (id) { return vis[id]; })[0];
      if (first) toc.forEach(function (a) { a.classList.toggle('on', a === map[first]); });
    }, { rootMargin: '-70px 0px -65% 0px' });
    Object.keys(map).forEach(function (id) { var h = d.getElementById(id); if (h) io.observe(h); });
  }

  /* search: loads search.json on first open */
  var dlg = d.getElementById('dSearch'); if (!dlg) return;
  var input = dlg.querySelector('input'), list = dlg.querySelector('.d-search-r'), data = null, sel = 0, last = null;
  function esc(s) { var x = d.createElement('div'); x.textContent = s; return x.innerHTML; }
  function open() {
    last = d.activeElement; dlg.hidden = false; input.value = ''; list.innerHTML = ''; input.focus();
    if (!data) fetch(base + 'search.json').then(function (r) { return r.json(); }).then(function (j) { data = j; run(); }).catch(function () { list.innerHTML = '<li class="d-search-f">Search is unavailable offline.</li>'; });
  }
  function close() { dlg.hidden = true; if (last && last.focus) last.focus(); }
  function run() {
    if (!data) return;
    var q = input.value.trim().toLowerCase(); if (!q) { list.innerHTML = ''; return; }
    var words = q.split(/\s+/);
    var hits = data.map(function (it) {
      var t = it.t.toLowerCase(), x = it.x.toLowerCase(), s = 0;
      for (var i = 0; i < words.length; i++) { var w = words[i]; if (t.indexOf(w) >= 0) s += 3; else if (x.indexOf(w) >= 0) s += 1; else return null; }
      return { it: it, s: s + (t.indexOf(q) >= 0 ? 4 : 0) };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    var re = new RegExp('(' + words.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
    list.innerHTML = hits.length ? hits.map(function (h, k) {
      return '<li><a href="' + base + h.it.u + '" role="option" aria-selected="' + (k === 0) + '"><small>' + esc(h.it.s) + '</small><b>' + esc(h.it.t).replace(re, '<mark>$1</mark>') + '</b><span>' + esc(h.it.x).replace(re, '<mark>$1</mark>') + '</span></a></li>';
    }).join('') : '<li class="d-search-f">No results. Try fewer words.</li>';
    sel = 0;
  }
  function move(n) {
    var a = $$('a', list); if (!a.length) return;
    sel = (sel + n + a.length) % a.length;
    a.forEach(function (x, k) { x.setAttribute('aria-selected', String(k === sel)); });
    a[sel].scrollIntoView({ block: 'nearest' });
  }
  input.addEventListener('input', run);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') { var a = $$('a', list)[sel]; if (a) location.href = a.href; }
  });
  $$('[data-search]').forEach(function (b) { b.addEventListener('click', open); });
  $$('[data-search-close]', dlg).forEach(function (b) { b.addEventListener('click', close); });
  d.addEventListener('keydown', function (e) {
    if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) { e.preventDefault(); dlg.hidden ? open() : close(); }
    else if (e.key === '/' && dlg.hidden && !/input|textarea|select/i.test((d.activeElement || {}).tagName || '')) { e.preventDefault(); open(); }
    else if (e.key === 'Escape' && !dlg.hidden) close();
  });
})();
