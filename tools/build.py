"""Echo site builder: Markdown in content/, static HTML out.

    python tools/build.py            build docs, blog, sitemap, search index, llms.txt (no Markdown copies, no RSS)
    python tools/build.py check      build into memory, report problems, write nothing
    python tools/build.py serve      build, serve on http://127.0.0.1:8000 and rebuild on save

Requires: pip install -r tools/requirements.txt   (markdown, pygments, pyyaml, pillow)
How the content is organised: content/README.md
"""
import datetime, hashlib, textwrap, html, http.server, json, math, os, re, shutil, socketserver, sys, threading, time
from xml.sax.saxutils import escape as xesc

import markdown
import yaml
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

try:
    from PIL import Image
except ImportError:          # images still work, just without width and height
    Image = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content')
E = lambda s: html.escape(str(s), quote=True)
MODE = sys.argv[1] if len(sys.argv) > 1 else 'build'
WRITE = MODE != 'check'
problems, written = [], []


def warn(msg):
    problems.append(msg)


def rd(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def out(rel, text):
    """Write a generated file, only when it changed."""
    path = os.path.join(ROOT, rel)
    if os.path.exists(path) and rd(path) == text:
        return
    written.append(rel)
    if WRITE:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)


def yml(rel):
    return yaml.safe_load(rd(os.path.join(CONTENT, rel))) or {}


def frontmatter(text, where):
    if not text.startswith('---'):
        warn('%s: no frontmatter' % where)
        return {}, text
    end = text.find('\n---', 3)
    meta = yaml.safe_load(text[3:end]) or {}
    return meta, text[end + 4:].lstrip('\n')


def slug(s):
    s = re.sub(r'<[^>]+>', '', s).lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    return re.sub(r'[\s-]+', '-', s).strip('-') or 'section'


def relpath(target, from_dir):
    """target and from_dir are site-root relative, with forward slashes."""
    r = os.path.relpath(target or '.', from_dir or '.').replace('\\', '/')
    if (not target or target.endswith('/')) and not r.endswith('/'):
        r += '/'
    return './' if r in ('.', './') else r


SITE = yml('site.yml')
BASE = SITE['base_url'].rstrip('/') + '/'
TODAY = datetime.date.today().isoformat()


def site_href(h, from_dir):
    """'/docs/x.html' style links from config become relative to the page."""
    if h.startswith('/'):
        path, _, frag = h[1:].partition('#')
        return relpath(path, from_dir) + ('#' + frag if frag else '') if path else relpath('', from_dir) + ('#' + frag if frag else '')
    return h


# ------------------------------------------------------------------ components
class Components:
    """Reads content/components.html. Each <component name=".."> has a <doc>, an <example> and its <html>."""

    def __init__(self, path):
        self.defs = {}
        for m in re.finditer(r'<component\s+([^>]*)>(.*?)</component>', rd(path), re.S):
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            body = m.group(2)
            part = lambda t: (re.search(r'<%s>(.*?)</%s>' % (t, t), body, re.S) or [None, ''])[1].strip('\n')
            self.defs[attrs['name']] = dict(attrs, doc=part('doc').strip(), example=part('example'), html=part('html').strip())

    @staticmethod
    def fill(tpl, props):
        def section(m):
            neg, key, inner = m.group(1) == '^', m.group(2), m.group(3)
            on = bool(props.get(key))
            return inner if on != neg else ''
        tpl = re.sub(r'\{\{([#^])(\w+)\}\}(.*?)\{\{/\2\}\}', section, tpl, flags=re.S)
        tpl = re.sub(r'\{\{\{(\w+)\}\}\}', lambda m: str(props.get(m.group(1), '')), tpl)
        return re.sub(r'\{\{(\w+)\}\}', lambda m: E(props.get(m.group(1), '')) if m.group(1) != 'children' else props.get('children', ''), tpl)


COMP = Components(os.path.join(CONTENT, 'components.html'))
FORMATTER = HtmlFormatter(nowrap=True)
MD_EXT = ['tables', 'attr_list', 'def_list', 'sane_lists', 'footnotes', 'abbr', 'md_in_html']


class Page:
    """One Markdown file turned into HTML: components, code, headings, links and images."""

    def __init__(self, src, out_rel, meta, body, link_map):
        self.src, self.out_rel, self.meta = src, out_rel, meta
        self.out_dir = os.path.dirname(out_rel)
        self.link_map = link_map
        self.store, self.kinds = {}, {}
        self.toc = []
        self.words = 0
        self.html = self.render(body)

    # placeholders keep code and component HTML away from the Markdown parser
    def keep(self, html_text, inline=False, kind=''):
        key = 'ZZC%dZZ' % len(self.store)
        self.store[key] = html_text
        self.kinds[key] = kind
        return key if inline else '\n\n%s\n\n' % key

    def restore(self, text):
        for _ in range(8):
            new = re.sub(r'<p>(ZZC\d+ZZ)</p>', lambda m: self.store[m.group(1)], text)
            new = re.sub(r'ZZC\d+ZZ', lambda m: self.store[m.group(0)], new)
            if new == text:
                break
            text = new
        return text

    def code(self, lang, info, src):
        title = ''
        m = re.search(r'title="([^"]*)"', info)
        if m:
            title = m.group(1)
        elif info.strip():
            title = info.strip()
        try:
            lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except Exception:
            lexer = TextLexer()
        body = highlight(src, lexer, FORMATTER)
        label = title or {'bash': 'Terminal', 'sh': 'Terminal', 'json': 'JSON', 'python': 'Python', 'js': 'JavaScript',
                          'javascript': 'JavaScript', 'http': 'HTTP', 'yaml': 'YAML', 'md': 'Markdown', 'html': 'HTML'}.get(lang, lang.upper() if lang else 'Text')
        return ('<div class="c-code" data-title="%s"><div class="c-code-h"><span>%s</span>'
                '<button class="c-copy" type="button" aria-label="Copy code">Copy</button></div>'
                '<pre class="hl"><code%s>%s</code></pre></div>') % (E(label), E(label), ' class="language-%s"' % E(lang) if lang else '', body)

    def md(self, text):
        return markdown.markdown(text, extensions=MD_EXT, output_format='html')

    def expand(self, text):
        """Replace registered <Component ...>...</Component> tags, innermost content first."""
        names = '|'.join(sorted(COMP.defs, key=len, reverse=True))
        opener = re.compile(r'<(%s)(\s[^<>]*?)?(/?)>' % names)
        while True:
            m = opener.search(text)
            if not m:
                return text
            name, attr_src, selfclose = m.group(1), m.group(2) or '', m.group(3)
            props = {k: v for k, v in re.findall(r'(\w+)="([^"]*)"', attr_src)}
            for flag in re.findall(r'(?<![\w="])\b(\w+)\b(?!=)', re.sub(r'\w+="[^"]*"', '', attr_src)):
                props[flag] = 'true'
            start, i = m.start(), m.end()
            children = ''
            if not selfclose:
                depth, pat = 1, re.compile(r'<(/?)%s(\s[^<>]*?)?(/?)>' % name)
                for t in pat.finditer(text, i):
                    if t.group(3):
                        continue
                    depth += -1 if t.group(1) else 1
                    if depth == 0:
                        children, end = text[i:t.start()], t.end()
                        break
                else:
                    warn('%s: <%s> is not closed' % (self.src, name))
                    children, end = text[i:], len(text)
            else:
                end = i
            d = COMP.defs[name]
            inner = self.expand(textwrap.dedent(children.strip(chr(10))) if chr(10) in children else children)
            if d.get('inline') == 'true':
                inner_html = self.md(inner.strip())
                inner_html = re.sub(r'^<p>(.*)</p>$', r'\1', inner_html, flags=re.S)
            else:
                inner_html = self.md(inner)
            if name == 'Endpoint':   # examples move to the right-hand column
                ex = [k for k in re.findall(r'ZZC\d+ZZ', inner_html) if self.kinds.get(k) in ('RequestExample', 'ResponseExample')]
                props['examples'] = ''.join(self.restore(k) for k in ex)
                for k in ex:
                    inner_html = inner_html.replace('<p>%s</p>' % k, '').replace(k, '')
                props.setdefault('id', 'ep-' + slug(props.get('title') or props.get('path', '')))
            inner_html = self.restore(inner_html)
            props['children'] = inner_html
            if d.get('tabs') == 'true':
                titles = re.findall(r'data-title="([^"]*)"', inner_html)
                uid = hashlib.md5((self.src + str(start) + inner_html[:80]).encode()).hexdigest()[:6]
                props['tablist'] = ''.join('<button type="button" role="tab" aria-selected="%s" data-i="%d" id="t%s-%d">%s</button>'
                                           % ('true' if k == 0 else 'false', k, uid, k, t) for k, t in enumerate(titles))
            if name == 'Snippet':
                path = os.path.join(CONTENT, 'snippets', props.get('file', ''))
                if not os.path.exists(path):
                    warn('%s: snippet %s is missing' % (self.src, props.get('file')))
                    props['children'] = ''
                else:
                    props['children'] = self.restore(self.md(self.expand(self.protect(rd(path)))))
            rendered = COMP.fill(d['html'], props)
            text = text[:start] + self.keep(rendered, inline=d.get('inline') == 'true', kind=name) + text[end:]

    def protect(self, text):
        # fenced code
        def fence(m):
            lang_info = m.group(2).strip()
            lang, _, info = lang_info.partition(' ')
            return self.keep(self.code(lang.strip().lower(), info, m.group(3)))
        text = re.sub(r'(?m)^(```+)([^\n]*)\n(.*?)\n\1[ \t]*$', fence, text, flags=re.S)
        # inline code, so component names inside backticks stay literal
        text = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', lambda m: self.keep('<code>%s</code>' % E(m.group(1)), inline=True), text)
        return text

    def render(self, body):
        self.words = len(re.findall(r'\w+', re.sub(r'<[^>]+>|```.*?```', ' ', body, flags=re.S)))
        text = self.expand(self.protect(body))
        h = self.restore(self.md(text))
        h = self.headings(h)
        h = re.sub(r'<table>', '<div class="c-table"><table>', h).replace('</table>', '</table></div>')
        h = re.sub(r'<img\s([^>]*)>', self.image, h)
        h = re.sub(r'<p>(<figure class="c-frame.*?</figure>)</p>', r'\1', h, flags=re.S)
        h = re.sub(r'href="([^"]+)"', self.link, h)
        return h

    def headings(self, h):
        seen = set()

        def fix(m):
            lvl, attrs, inner = m.group(1), m.group(2) or '', m.group(3)
            idm = re.search(r'id="([^"]+)"', attrs)
            hid = idm.group(1) if idm else slug(inner)
            base, n = hid, 2
            while hid in seen:
                hid, n = '%s-%d' % (base, n), n + 1
            seen.add(hid)
            attrs = re.sub(r'\s*id="[^"]+"', '', attrs)
            if lvl in '23':
                self.toc.append((int(lvl), hid, re.sub(r'<[^>]+>', '', inner)))
            return '<h%s id="%s"%s>%s<a class="h-anchor" href="#%s" aria-label="Link to this section">#</a></h%s>' % (lvl, hid, attrs, inner, hid, lvl)
        return re.sub(r'<h([234])(\s[^>]*)?>(.*?)</h\1>', fix, h, flags=re.S)

    def image(self, m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        src = attrs.get('src', '')
        if src.startswith(('http', 'data:')):
            return m.group(0)
        disk = os.path.normpath(os.path.join(ROOT, self.out_dir, src))
        w = h = None
        if not os.path.exists(disk):
            warn('%s: image %s not found (expected at %s)' % (self.src, src, os.path.relpath(disk, ROOT)))
        elif Image and not src.endswith('.svg'):
            try:
                with Image.open(disk) as im:
                    w, h = im.size
            except Exception:
                pass
        alt = attrs.get('alt', '')
        if not alt:
            warn('%s: image %s has no alt text' % (self.src, src))
        tag = '<img src="%s" alt="%s"%s loading="lazy" decoding="async">' % (E(src), E(alt), ' width="%d" height="%d"' % (w, h) if w else '')
        cap = attrs.get('title')
        return '<figure class="c-frame">%s<figcaption>%s</figcaption></figure>' % (tag, cap) if cap else tag

    def link(self, m):
        h = html.unescape(m.group(1))
        if re.match(r'^(https?:|mailto:|tel:|#|data:)', h):
            return m.group(0)
        path, _, frag = h.partition('#')
        if h.startswith('/'):
            target = path[1:]
        else:
            src_dir = os.path.dirname(self.src)
            cand = os.path.normpath(os.path.join(src_dir, path)).replace('\\', '/')
            for c in (cand, cand + '.md', cand.rstrip('/') + '/index.md'):
                if c in self.link_map:
                    target = self.link_map[c]
                    break
            else:
                target = os.path.normpath(os.path.join(self.out_dir, path)).replace('\\', '/') if path else self.out_rel
        if target.endswith('.md') and target not in self.link_map.values():
            target = target[:-3] + '.html'
        disk = os.path.join(ROOT, target)
        if path and not (os.path.exists(disk) or target in ALL_OUTPUTS or (target.endswith('/') and (target + 'index.html') in ALL_OUTPUTS)):
            warn('%s: link to %s does not resolve' % (self.src, h))
        r = relpath(target, self.out_dir) if path else ''
        if r.endswith('index.html'):
            r = r[:-10] or './'
        return 'href="%s"' % E(r + ('#' + frag if frag else ''))


ALL_OUTPUTS = set()


# ------------------------------------------------------------------ page chrome
def head(title, desc, canon_rel, out_dir, meta, kind, extra_ld, keywords):
    img = BASE + (meta.get('image_url') or SITE.get('default_image', 'og.png'))
    robots = 'noindex' if meta.get('draft') or meta.get('noindex') else 'index,follow,max-image-preview:large'
    kw = ', '.join(keywords)
    css = relpath('assets/docs.css', out_dir)
    js = relpath('assets/docs.js', out_dir)
    ld = ''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in extra_ld)
    return '''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{kw}<link rel="canonical" href="{c}">
<meta name="robots" content="{r}">
<meta property="og:type" content="{k}">
<meta property="og:site_name" content="{sn}">
<meta property="og:locale" content="{loc}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{c}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#11100F" media="(prefers-color-scheme: dark)">
<script>document.documentElement.classList.add('js');try{{var t=localStorage.getItem('echo-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..850&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<link rel="icon" type="image/png" href="{fav}">
{alt}<script src="{js}" defer></script>
{ld}
</head>'''.format(t=E(title), d=E(desc), c=E(BASE + canon_rel), r=robots, k=kind, sn=E(SITE['site_name']), loc=SITE.get('locale', 'en_IN'),
                  img=E(img), css=css, js=js, fav=relpath('favicon.png', out_dir), ld=ld,
                  kw='', alt='')


def brand(out_dir):
    return ('<a class="brand" href="{h}" aria-label="{n} home"><img class="clx lt" src="{a}" alt="Cognilix" width="99" height="22">'
            '<img class="clx dk" src="{b}" alt="" aria-hidden="true" width="99" height="22"><span class="bdiv" aria-hidden="true"></span>'
            '<span class="wm">echo</span></a>').format(h=relpath('', out_dir), n=E(SITE['site_name']),
                                                     a=relpath('cognilix.png', out_dir), b=relpath('cognilix-white.png', out_dir))


def header(out_dir, current):
    links = ''.join('<a href="%s"%s>%s</a>' % (E(site_href(l['href'], out_dir)), ' aria-current="page"' if l['href'] == current else '', E(l['label']))
                    for l in SITE['nav'])
    return ('<header class="nav">\n  %s\n  <nav class="links" aria-label="Site">%s</nav>\n'
            '  <button class="d-search-b" type="button" data-search aria-label="Search the docs"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.6" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="m10.5 10.5 3.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span>Search</span><kbd>Ctrl K</kbd></button>\n'
            '  <button class="d-theme" type="button" data-theme-toggle aria-label="Switch colour theme"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5a6.5 6.5 0 1 0 0 13z" fill="currentColor"/><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></button>\n'
            '  <a class="cta" href="%s">%s</a>\n'
            '  <button class="d-menu-b" type="button" data-menu aria-controls="dSide" aria-expanded="false" aria-label="Open the menu"><span></span><span></span></button>\n'
            '</header>') % (brand(out_dir), links, E(site_href(SITE['cta']['href'], out_dir)), E(SITE['cta']['label']))


def footer(out_dir):
    cols = ''.join('<div><h4>%s</h4>%s</div>' % (E(c['title']), ''.join(
        '<a href="%s"%s>%s</a>' % (E(site_href(l['href'], out_dir)), ' rel="noopener" target="_blank"' if l['href'].startswith('http') else '', E(l['label']))
        for l in c['links'])) for c in SITE['footer']['columns'])
    return ('<footer class="d-foot"><div class="d-foot-in"><div class="d-foot-b">%s<p>%s</p></div>%s</div>'
            '<div class="d-foot-bot"><span>%s</span><span>%s</span></div></footer>') % (
        brand(out_dir), E(SITE['footer']['blurb']), cols, E(SITE['footer']['note']), E(SITE['footer']['copyright']))


def search_dialog():
    return ('<div class="d-search" id="dSearch" role="dialog" aria-modal="true" aria-label="Search" hidden>'
            '<div class="d-search-bg" data-search-close></div><div class="d-search-box">'
            '<input type="search" placeholder="Search docs and articles" aria-label="Search" autocomplete="off" spellcheck="false">'
            '<ul class="d-search-r" role="listbox"></ul><p class="d-search-f"><kbd>Enter</kbd> open <kbd>Esc</kbd> close</p></div></div>')


def fmt_date(iso):
    try:
        return datetime.date.fromisoformat(str(iso)).strftime('%d %b %Y').lstrip('0')
    except Exception:
        return str(iso)


# ------------------------------------------------------------------ docs
def build_docs():
    cfg = yml('docs/docs.yml')
    pages, link_map = [], {}
    for tab in cfg['tabs']:
        src_dir = 'content/docs/' + tab['folder']
        for group in tab['groups']:
            for entry in group['pages']:
                name = entry if isinstance(entry, str) else entry['page']
                src = '%s/%s.md' % (src_dir, name)
                out_rel = tab['output'] + ('index.html' if name == 'index' else name + '.html')
                pages.append(dict(tab=tab, group=group['group'], name=name, src=src, out=out_rel,
                                  badge=None if isinstance(entry, str) else entry.get('badge')))
                link_map[src] = out_rel
                ALL_OUTPUTS.add(out_rel)
        # assets folder next to the Markdown is copied beside the HTML
        a_src = os.path.join(ROOT, src_dir, 'assets')
        if os.path.isdir(a_src) and WRITE:
            dst = os.path.join(ROOT, tab['output'], 'assets')
            shutil.copytree(a_src, dst, dirs_exist_ok=True)
    listed = {p['src'] for p in pages}
    for tab in cfg['tabs']:
        folder = os.path.join(ROOT, 'content/docs', tab['folder'])
        for f in os.listdir(folder):
            if f.endswith('.md') and not f.startswith('_') and 'content/docs/%s/%s' % (tab['folder'], f) not in listed:
                warn('content/docs/%s/%s is not in docs.yml, so it is not in the sidebar or built' % (tab['folder'], f))
    built = []
    for p in pages:
        path = os.path.join(ROOT, p['src'])
        if not os.path.exists(path):
            warn('%s is listed in docs.yml but missing (copy a file from content/docs/_templates/)' % p['src'])
            continue
        meta, body = frontmatter(rd(path), p['src'])
        for k in ('title', 'description'):
            if not meta.get(k):
                warn('%s: frontmatter needs %s' % (p['src'], k))
        if len(meta.get('description', '')) > 170:
            warn('%s: description is %d characters, search engines show about 155' % (p['src'], len(meta['description'])))
        pg = Page(p['src'], p['out'], meta, body, link_map)
        built.append((p, meta, pg))
    for i, (p, meta, pg) in enumerate(built):
        tab = p['tab']
        out_dir = os.path.dirname(p['out'])
        soon = str(meta.get('status', '')).lower() in ('soon', 'coming-soon', 'coming soon')
        title = meta['title']
        full_title = title if p['name'] == 'index' else '%s · %s' % (title, tab['title_suffix'])   # section home pages carry their own name
        kws = meta.get('keywords', []) + cfg.get('keywords', [])
        updated = str(meta.get('updated', TODAY))
        crumbs = [('Home', ''), ('Docs', 'docs/')] + ([(tab['label'], tab['output'])] if tab['output'] != 'docs/' else []) + [(title, p['out'])]
        ld = [{"@context": "https://schema.org", "@type": "TechArticle", "headline": title, "description": meta.get('description', ''),
               "dateModified": updated, "inLanguage": "en-IN", "url": BASE + p['out'],
               "author": {"@type": "Organization", "name": SITE['org']}, "publisher": {"@type": "Organization", "name": SITE['org'], "url": SITE['org_url']}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": k + 1, "name": n, "item": BASE + u} for k, (n, u) in enumerate(crumbs)]}]
        if meta.get('faq'):
            ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in meta['faq']]})
        side = sidebar(cfg, built, p, out_dir)
        prev = built[i - 1] if i and built[i - 1][0]['tab'] is tab else None
        nxt = built[i + 1] if i + 1 < len(built) and built[i + 1][0]['tab'] is tab else None
        pager = '<nav class="d-pager" aria-label="Previous and next">%s%s</nav>' % (
            '<a href="%s"><small>Previous</small><b>%s</b></a>' % (relpath(prev[0]['out'], out_dir).replace('index.html', '') or './', E(prev[1].get('sidebarTitle', prev[1]['title']))) if prev else '<span></span>',
            '<a class="nx" href="%s"><small>Next</small><b>%s</b></a>' % (relpath(nxt[0]['out'], out_dir).replace('index.html', '') or './', E(nxt[1].get('sidebarTitle', nxt[1]['title']))) if nxt else '')
        toc = ''.join('<a class="l%d" href="#%s">%s</a>' % (lvl, hid, E(t)) for lvl, hid, t in pg.toc)
        crumb = ' / '.join('<a href="%s">%s</a>' % (relpath(u, out_dir) if u else relpath('', out_dir), E(n)) for n, u in crumbs[:-1]) + ' / ' + E(p['group'])
        mins = max(1, round(pg.words / 220))
        page = head(full_title, meta.get('description', ''), p['out'].replace('index.html', ''), out_dir, meta, 'article', ld, kws) + '''
<body class="d-body">
<a class="skip" href="#content">Skip to content</a>
{hdr}
<div class="d-shell">
<aside class="d-side" id="dSide" aria-label="Documentation">{side}</aside>
<main class="d-main" id="content">
<p class="crumb">{crumb}</p>
<p class="kick">{group}{soon_tag}</p>
<h1>{title}</h1>
<p class="lede">{desc}</p>
<div class="d-meta"><span>Updated {upd}</span><span>{mins} min read</span><button class="d-copy" type="button" data-copy-page><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="5" y="5" width="8.5" height="8.5" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M3 10.5V3.6C3 3.3 3.3 3 3.6 3h6.9" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg><span>Copy page</span></button></div>
{soon_note}<article class="d-prose">
{body}
</article>
{pager}
</main>
<aside class="d-toc" aria-label="On this page">{toc}</aside>
</div>
{foot}
{search}
</body>
</html>
'''.format(hdr=header(out_dir, '/docs/'), side=side, crumb=crumb, group=E(p['group']), title=E(title), desc=E(meta.get('description', '')),
           upd=fmt_date(updated), mins=mins, body=pg.html, pager=pager,
           soon_tag='<span class="d-soon">Coming soon</span>' if soon else '',
           soon_note=('<aside class="c-callout c-soon" role="note"><p class="c-callout-t">Coming soon</p><p>%s</p></aside>\n' % E(
               meta.get('soon_note') or 'This is not in the product yet. The page shows how it will work so you can plan for it. Ask your account team for early access.')) if soon else '',
           toc='<b>On this page</b>' + toc if toc else '', foot=footer(out_dir), search=search_dialog())
        out(p['out'], page)
        SEARCH.extend(search_entries(pg, p['out'], title, tab['label']))
        SITEMAP.append((p['out'].replace('index.html', ''), updated))
        LLMS.setdefault(tab['label'], []).append((title, BASE + p['out'].replace('index.html', ''), meta.get('description', '')))
    DOC_LINKS.update(link_map)
    return built


DOC_LINKS = {}


def sidebar(cfg, built, cur, out_dir):
    tabs = ''.join('<a class="d-tab%s" href="%s"%s><span>%s</span><small>%s</small></a>' % (
        ' on' if t is cur['tab'] else '', relpath(t['output'], out_dir), ' aria-current="true"' if t is cur['tab'] else '', E(t['label']), E(t.get('badge', '')))
        for t in cfg['tabs'])
    groups, last = '', None
    for p, meta, _ in built:
        if p['tab'] is not cur['tab']:
            continue
        if p['group'] != last:
            groups += ('</div>' if last else '') + '<div class="d-grp"><h4>%s</h4>' % E(p['group'])
            last = p['group']
        tab_soon = str(cur['tab'].get('badge', '')).lower() == 'coming soon'   # the whole tab is marked, so pages need no badge
        badge = p.get('badge') or meta.get('badge') or ('Soon' if not tab_soon and str(meta.get('status', '')).lower() in ('soon', 'coming-soon', 'coming soon') else None)
        href = relpath(p['out'], out_dir)
        if href.endswith('index.html'):
            href = href[:-10] or './'
        groups += '<a href="%s"%s>%s%s</a>' % (href, ' aria-current="page"' if p is cur else '', E(meta.get('sidebarTitle', meta['title'])),
                                              ' <span class="d-badge%s">%s</span>' % (' soon' if badge == 'Soon' else '', E(badge)) if badge else '')
    return '<nav class="d-tabs" aria-label="Documentation sets">%s</nav><nav class="d-nav" aria-label="Pages">%s</div></nav>' % (tabs, groups)


def search_entries(pg, url, title, section):
    items, h = [], pg.html
    parts = re.split(r'<h2 id="([^"]+)">', h)
    first = re.sub(r'<[^>]+>', ' ', parts[0])
    items.append({'t': title, 's': section, 'u': url, 'x': re.sub(r'\s+', ' ', first).strip()[:220]})
    for k in range(1, len(parts), 2):
        hid, rest = parts[k], parts[k + 1]
        head_txt = re.sub(r'<[^>]+>|#$', '', rest.split('</h2>')[0]).strip().rstrip('#')
        body = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', rest.split('</h2>', 1)[-1])).strip()
        items.append({'t': title + ' › ' + head_txt, 's': section, 'u': url + '#' + hid, 'x': body[:220]})
    return items


# ------------------------------------------------------------------ blog
def build_blog():
    cfg = yml('blog/blog.yml')
    folder = os.path.join(CONTENT, 'blog', 'posts')
    posts, link_map = [], {}
    for f in sorted(os.listdir(folder)):
        if not f.endswith('.md') or f.startswith('_'):
            continue
        src = 'content/blog/posts/' + f
        meta, body = frontmatter(rd(os.path.join(ROOT, src)), src)
        s = meta.get('slug') or f[:-3]
        out_rel = 'blog/%s.html' % s
        link_map[src] = out_rel
        ALL_OUTPUTS.add(out_rel)
        posts.append([src, out_rel, meta, body])
    a_src = os.path.join(CONTENT, 'blog', 'assets')
    if os.path.isdir(a_src) and WRITE:
        shutil.copytree(a_src, os.path.join(ROOT, 'blog', 'assets'), dirs_exist_ok=True)
    authors = cfg.get('authors', {})
    live = []
    for src, out_rel, meta, body in posts:
        for k in ('title', 'description', 'date', 'author', 'category'):
            if not meta.get(k):
                warn('%s: frontmatter needs %s' % (src, k))
        if meta.get('author') and meta['author'] not in authors:
            warn('%s: author %s is not in blog.yml' % (src, meta['author']))
        if meta.get('category') and meta['category'] not in cfg.get('categories', {}):
            warn('%s: category %s is not in blog.yml' % (src, meta['category']))
        pg = Page(src, out_rel, meta, body, link_map)
        if not meta.get('draft'):
            live.append((src, out_rel, meta, pg))
        else:
            write_post(cfg, authors, src, out_rel, meta, pg, [])
    live.sort(key=lambda x: str(x[2].get('date', '')), reverse=True)
    for item in live:
        src, out_rel, meta, pg = item
        related = [x for x in live if x is not item and (x[2].get('category') == meta.get('category') or set(x[2].get('tags', [])) & set(meta.get('tags', [])))][:3]
        write_post(cfg, authors, src, out_rel, meta, pg, related)
    # index, category pages, pagination, feed
    per = cfg.get('per_page', 9)
    def listing(items, out_dir, title, lede, canon, cat=None, page_no=1, pages=1):
        used = {x[2].get('category') for x in live}
        cats = '' if not used else '<nav class="b-cats" aria-label="Categories"><a href="%s"%s>All</a>%s</nav>' % (
            relpath('blog/', out_dir), '' if cat else ' aria-current="page"',
            ''.join('<a href="%s"%s>%s</a>' % (relpath('blog/category/%s/' % k, out_dir), ' aria-current="page"' if k == cat else '', E(v['label']))
                    for k, v in cfg.get('categories', {}).items() if k in used))
        cards = ''.join(card(x, out_dir, authors, cfg) for x in items)
        if not items:
            cards = ('<div class="b-empty"><b>%s</b><p>%s</p><a class="cta" href="%s">%s</a></div>' % (
                E(cfg['empty']['title']), E(cfg['empty']['text']), E(site_href(cfg['empty']['href'], out_dir)), E(cfg['empty']['label'])))
        nav = ''
        if pages > 1:
            base = 'blog/' if not cat else 'blog/category/%s/' % cat
            link = lambda n: relpath(base if n == 1 else base + 'page/%d/' % n, out_dir)
            nav = '<nav class="b-pages" aria-label="Pages">%s<span>Page %d of %d</span>%s</nav>' % (
                '<a href="%s" rel="prev">Newer</a>' % link(page_no - 1) if page_no > 1 else '<span></span>', page_no, pages,
                '<a href="%s" rel="next">Older</a>' % link(page_no + 1) if page_no < pages else '<span></span>')
        ld = [{"@context": "https://schema.org", "@type": "Blog", "name": cfg['title'], "url": BASE + canon,
               "blogPost": [{"@type": "BlogPosting", "headline": x[2]['title'], "url": BASE + x[1], "datePublished": str(x[2].get('date'))} for x in items]}]
        m = {'noindex': not items}
        return head(title, lede, canon, out_dir, m, 'website', ld, cfg.get('keywords', [])) + '''
<body class="b-body">
<a class="skip" href="#content">Skip to content</a>
{hdr}
<main class="b-main" id="content">
<p class="crumb"><a href="{home}">Home</a> / Blog</p>
<p class="kick">{kick}</p>
<h1>{h1}</h1>
<p class="lede">{lede}</p>
{cats}
<div class="b-grid">{cards}</div>
{nav}
</main>
{foot}
{search}
</body>
</html>
'''.format(hdr=header(out_dir, '/blog/'), home=relpath('', out_dir), kick=E(cfg['kicker']), h1=E(title if cat else cfg['heading']), lede=E(lede),
           cats=cats, cards=cards, nav=nav, foot=footer(out_dir), search=search_dialog())
    def paged(items, base, title, lede, cat=None):
        pages = max(1, math.ceil(len(items) / per))
        for n in range(1, pages + 1):
            rel = base + ('' if n == 1 else 'page/%d/' % n)
            ALL_OUTPUTS.add(rel + 'index.html')
            out(rel + 'index.html', listing(items[(n - 1) * per:n * per], rel.rstrip('/'), title, lede, rel, cat, n, pages))
    paged(live, 'blog/', cfg['title'], cfg['description'])
    SITEMAP.append(('blog/', TODAY))
    for k, v in cfg.get('categories', {}).items():
        items = [x for x in live if x[2].get('category') == k]
        if not items:          # no empty category pages
            continue
        paged(items, 'blog/category/%s/' % k, '%s · %s' % (v['label'], cfg['title']), v['description'], k)
        if items:
            SITEMAP.append(('blog/category/%s/' % k, TODAY))
    for src, out_rel, meta, pg in live:
        SITEMAP.append((out_rel, str(meta.get('updated', meta.get('date')))))
        LLMS.setdefault('Blog', []).append((meta['title'], BASE + out_rel, meta.get('description', '')))
    # the home page shows the latest three posts from this file
    out('blog/posts.json', json.dumps([{'url': os.path.basename(x[1]), 'title': x[2]['title'], 'summary': x[2].get('description', ''),
                                        'category': cfg['categories'].get(x[2].get('category'), {}).get('label', ''), 'date': str(x[2]['date']),
                                        'image': 'assets/' + x[2]['image'] if x[2].get('image') else ''} for x in live[:3]], indent=1, ensure_ascii=False) + '\n')
    return live


def card(x, out_dir, authors, cfg):
    src, out_rel, meta, pg = x
    img = meta.get('image')
    return ('<a class="b-card" href="{h}">{img}<small>{c}</small><h2>{t}</h2><p>{d}</p><span class="b-meta">{a} · <time datetime="{iso}">{date}</time> · {m} min read</span></a>').format(
        h=relpath(out_rel, out_dir), t=E(meta['title']), d=E(meta.get('description', '')), c=E(cfg['categories'].get(meta.get('category'), {}).get('label', '')),
        a=E(authors.get(meta.get('author'), {}).get('name', '')), iso=meta.get('date'), date=fmt_date(meta.get('date')), m=max(1, round(pg.words / 220)),
        img='<img src="%s" alt="" loading="lazy" decoding="async">' % E(relpath('blog/assets/' + img, out_dir)) if img else '')


def write_post(cfg, authors, src, out_rel, meta, pg, related):
    out_dir = 'blog'
    au = authors.get(meta.get('author'), {})
    cat = cfg['categories'].get(meta.get('category'), {}).get('label', '')
    img = ('blog/assets/' + meta['image']) if meta.get('image') else None
    meta = dict(meta, image_url=img)
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": meta['title'], "description": meta.get('description', ''),
           "datePublished": str(meta.get('date')), "dateModified": str(meta.get('updated', meta.get('date'))),
           "author": {"@type": "Person", "name": au.get('name', '')} if au else {"@type": "Organization", "name": SITE['org']},
           "publisher": {"@type": "Organization", "name": SITE['org'], "url": SITE['org_url']}, "mainEntityOfPage": BASE + out_rel,
           **({"image": BASE + img} if img else {})}]
    toc = ''.join('<a class="l%d" href="#%s">%s</a>' % (lvl, hid, E(t)) for lvl, hid, t in pg.toc)
    rel = ''.join(card(x, out_dir, authors, cfg) for x in related)
    page = head('%s · %s' % (meta['title'], cfg['title']), meta.get('description', ''), out_rel, out_dir, meta, 'article', ld, meta.get('keywords', [])) + '''
<body class="b-body">
<a class="skip" href="#content">Skip to content</a>
{hdr}
<main class="b-main b-post" id="content">
<p class="crumb"><a href="../">Home</a> / <a href="./">Blog</a> / {cat}</p>
<p class="kick">{cat}</p>
<h1>{t}</h1>
<p class="lede">{d}</p>
<p class="d-meta"><span>{au}</span><span>Published <time datetime="{iso}">{date}</time></span>{upd}<span>{m} min read</span></p>
{cover}
<div class="b-art">
<article class="d-prose">
{body}
</article>
<aside class="d-toc b-toc" aria-label="On this page">{toc}</aside>
</div>
<aside class="b-cta"><b>{ctat}</b><a class="cta" href="{ctah}">{ctal}</a></aside>
{related}
</main>
{foot}
{search}
</body>
</html>
'''.format(hdr=header(out_dir, '/blog/'), cat=E(cat), t=E(meta['title']), d=E(meta.get('description', '')), au=E(au.get('name', '')),
           iso=meta.get('date'), date=fmt_date(meta.get('date')), m=max(1, round(pg.words / 220)),
           upd='<span>Updated %s</span>' % fmt_date(meta['updated']) if meta.get('updated') and str(meta['updated']) != str(meta.get('date')) else '',
           cover='<img class="b-cover" src="%s" alt="%s" decoding="async">' % (E('assets/' + meta['image']), E(meta.get('image_alt', ''))) if meta.get('image') else '',
           body=pg.html, toc='<b>On this page</b>' + toc if toc else '', ctat=E(cfg['cta']['title']), ctah=E(site_href(cfg['cta']['href'], out_dir)),
           ctal=E(cfg['cta']['label']), related='<section class="b-rel"><h2>Related</h2><div class="b-grid">%s</div></section>' % rel if rel else '',
           foot=footer(out_dir), search=search_dialog())
    out(out_rel, page)


# ------------------------------------------------------------------ components gallery (internal)
def build_gallery():
    items = ''
    for name, d in COMP.defs.items():
        ex = d['example']
        pg = Page('content/docs/platform/_components.md', 'docs/_components.html', {}, ex, DOC_LINKS)
        items += ('<section class="g-item" id="%s"><h2>%s</h2><p>%s</p><div class="g-demo">%s</div>'
                  '<div class="c-code"><div class="c-code-h"><span>Markdown</span><button class="c-copy" type="button">Copy</button></div><pre class="hl"><code>%s</code></pre></div></section>') % (
            name, name, E(d['doc']), pg.html, E(ex.strip()))
    nav = ''.join('<a href="#%s">%s</a>' % (n, n) for n in COMP.defs)
    out('docs/_components.html', head('Components · Echo docs (internal)', 'Every reusable component for Markdown pages.', 'docs/_components.html', 'docs', {'noindex': True}, 'website', [], []) + '''
<body class="d-body"><a class="skip" href="#content">Skip to content</a>{hdr}
<div class="d-shell"><aside class="d-side" id="dSide"><nav class="d-nav"><div class="d-grp"><h4>Components</h4>{nav}</div></nav></aside>
<main class="d-main" id="content"><p class="kick">Internal</p><h1>Components</h1><p class="lede">Everything you can use inside a Markdown page. Defined in content/components.html.</p>
<article class="d-prose">{items}</article></main><aside class="d-toc"></aside></div>{foot}{search}</body></html>
'''.format(hdr=header('docs', '/docs/'), nav=nav, items=items, foot=footer('docs'), search=search_dialog()))


def build_previews():
    """Templates rendered as they will look (internal, noindex). Their placeholder links are not checked."""
    global problems
    keep = list(problems)
    tdir = os.path.join(CONTENT, 'docs', '_templates')
    items = [('content/docs/_templates/' + f, f[:-3]) for f in sorted(os.listdir(tdir)) if f.endswith('.md')] + [('content/blog/_template.md', 'blog-post')]
    rows = ''.join('<a href="_preview-%s.html">%s</a>' % (n, E(n)) for _, n in items)
    for src, name in items:
        meta, body = frontmatter(rd(os.path.join(ROOT, src)), src)
        rel = 'docs/_preview-%s.html' % name
        pseudo = 'content/docs/%s/_preview.md' % ('developers' if name == 'api-reference' else 'platform')   # links resolve like a real page
        pg = Page(pseudo, rel, meta, body, DOC_LINKS)
        out(rel, head('Template: %s' % name, meta.get('description', ''), rel, 'docs', {'noindex': True}, 'website', [], []) + '''
<body class="d-body"><a class="skip" href="#content">Skip to content</a>{hdr}
<div class="d-shell"><aside class="d-side" id="dSide"><nav class="d-nav"><div class="d-grp"><h4>Templates</h4>{rows}</div></nav></aside>
<main class="d-main" id="content"><p class="kick">Template preview · {src}</p><h1>{t}</h1><p class="lede">{d}</p>
<article class="d-prose">{b}</article></main><aside class="d-toc"></aside></div>{foot}{search}</body></html>
'''.format(hdr=header('docs', '/docs/'), rows=rows, src=E(src), t=E(meta.get('title', '')), d=E(meta.get('description', '')), b=pg.html,
           foot=footer('docs'), search=search_dialog()))
    problems = keep


# ------------------------------------------------------------------ run
SEARCH, SITEMAP, LLMS, LLMS_FULL = [], [], {}, []


def run():
    global problems, written, SEARCH, SITEMAP, LLMS, LLMS_FULL
    problems, written, SEARCH, SITEMAP, LLMS, LLMS_FULL = [], [], [], [], {}, []
    ALL_OUTPUTS.clear()
    ALL_OUTPUTS.update({'index.html', 'docs/api.html'})
    SITEMAP.append(('', TODAY))
    build_docs()
    build_blog()
    build_gallery()
    build_previews()
    out('search.json', json.dumps(SEARCH, ensure_ascii=False, separators=(',', ':')))
    out('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (xesc(BASE + u), d) for u, d in SITEMAP) + '</urlset>\n')
    llms = ['# %s' % SITE['site_name'], '> %s' % SITE['summary'], '']
    for sec, rows in LLMS.items():
        llms += ['## %s' % sec] + ['- [%s](%s): %s' % r for r in rows] + ['']
    out('llms.txt', '\n'.join(llms))
    sub = re.sub(r'^https?://[^/]+/', '', BASE)
    out('robots.txt', 'User-agent: *\nAllow: /\nDisallow: /%sdocs/_\nDisallow: /%sblog/_\nSitemap: %ssitemap.xml\n' % (sub, sub, BASE))
    for p in problems:
        print('  !', p)
    print('%s %d file(s), %d problem(s)' % ('would write' if not WRITE else 'wrote', len(written), len(problems)))
    return not problems


def snapshot():
    sig = []
    for base, _, files in os.walk(CONTENT):
        for f in files:
            p = os.path.join(base, f)
            sig.append((p, os.path.getmtime(p)))
    for f in ('tools/build.py', 'assets/docs.css', 'assets/docs.js'):
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            sig.append((p, os.path.getmtime(p)))
    return sorted(sig)


if __name__ == '__main__':
    ok = run()
    if MODE == 'serve':
        port = int(os.environ.get('PORT', 8000))
        os.chdir(os.path.dirname(ROOT))
        prefix = os.path.basename(ROOT)

        class H(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        srv = socketserver.ThreadingTCPServer(('127.0.0.1', port), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        print('Preview: http://127.0.0.1:%d/%s/docs/   (blog: /%s/blog/, components: /%s/docs/_components.html). Ctrl+C to stop.' % (port, prefix, prefix, prefix))
        last = snapshot()
        try:
            while True:
                time.sleep(0.8)
                now = snapshot()
                if now != last:
                    last = now
                    print(time.strftime('%H:%M:%S'), 'rebuilding')
                    try:
                        COMP = Components(os.path.join(CONTENT, 'components.html'))
                        SITE.update(yml('site.yml'))
                        run()
                    except Exception as e:
                        print('  ! build failed:', e)
        except KeyboardInterrupt:
            srv.shutdown()
    sys.exit(0 if ok else 1)
