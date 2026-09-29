"""Keeps docs, blog, sitemap and llms.txt in step. No dependencies beyond Python 3.8.

    python tools/site.py            rewrite navs, pagers, blog index, sitemap.xml and llms.txt
    python tools/site.py --check    report problems only, change nothing

Sources of truth
    docs/nav.json     every docs page, its title and its group, in reading order
    blog/posts.json   every blog post Marketing has published (empty list is fine)

See CONTENT.md for how to add a page, a screenshot or a post.
"""
import datetime, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://theruka7.github.io/qoyal/'
TODAY = datetime.date.today().isoformat()
E = html.escape
CHECK = '--check' in sys.argv
problems, changed = [], []


def rd(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def wr(rel, text):
    path = os.path.join(ROOT, rel)
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
    if old == text:
        return
    changed.append(rel)
    if not CHECK:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)


def site_links(up, current):
    items = [('#topuc', 'Use cases'), ('#how', 'How it works'), ('#roi', 'ROI'), ('docs/', 'Docs'), ('blog/', 'Blog')]
    out = []
    for href, name in items:
        cur = ' aria-current="page"' if href == current else ''
        out.append('<a href="%s%s"%s>%s</a>' % (up, href, cur, name))
    return '<nav class="links" aria-label="Site">' + ''.join(out) + '</nav>'


def fix_chrome(text, up, current):
    """Shared header links and CTA, and old landing anchors that no longer exist."""
    text = re.sub(r'<nav class="links" aria-label="Site">.*?</nav>', lambda m: site_links(up, current), text, count=1, flags=re.S)
    text = text.replace('<a class="cta" href="%s#pilot">Book a pilot</a>' % up, '<a class="cta" href="%s#pilot">Talk to an expert</a>' % up)
    text = re.sub(r'href="((?:\.\./)+)#(?:agents|industries)"', r'href="\1#topuc"', text)
    return text


# ---------------------------------------------------------------- docs
nav = json.loads(rd('docs/nav.json'))
llms_docs = []
sitemap = [SITE]
for key, sec in nav.items():
    base = sec['dir']                       # 'docs/' or 'docs/developers/'
    up = '../' * base.count('/')
    pages = [p for g in sec['groups'] for p in g['pages']]
    llms_docs.append('\n## ' + sec['label'])
    for i, pg in enumerate(pages):
        rel = base + pg['file']
        if not os.path.exists(os.path.join(ROOT, rel)):
            problems.append('%s is in docs/nav.json but the file is missing (copy docs/_template.html)' % rel)
            continue
        text = rd(rel)
        href = lambda f: './' if f == 'index.html' else f
        side = '<nav class="dside" aria-label="%s">' % sec['aria'] + ''.join(
            '<h4>%s</h4>' % E(g['title']) + ''.join(
                '<a href="%s"%s>%s%s</a>' % (href(p['file']), ' aria-current="page"' if p['file'] == pg['file'] else '',
                                             E(p['title']), ' <span class="new">New</span>' if p.get('new') else '')
                for p in g['pages']) for g in sec['groups']) + '</nav>'
        n = len(re.findall(r'<nav class="dside"', text))
        if n != 2:
            problems.append('%s should have 2 sidebars (desktop and mobile menu), found %d' % (rel, n))
        text = re.sub(r'<nav class="dside" aria-label="[^"]*">.*?</nav>', lambda m: side, text, flags=re.S)
        prev = pages[i - 1] if i else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        pager = '<nav class="pager" aria-label="Pages">' + \
            ('<a class="card" href="%s"><small>Previous</small><b>← %s</b></a>' % (href(prev['file']), E(prev['title'])) if prev else '') + \
            ('<a class="card nx" href="%s"><small>Next</small><b>%s →</b></a>' % (href(nxt['file']), E(nxt['title'])) if nxt else '') + '</nav>'
        text = re.sub(r'<nav class="pager" aria-label="Pages">.*?</nav>', lambda m: pager, text, count=1, flags=re.S)
        text = fix_chrome(text, up, 'docs/')
        for src in re.findall(r'<img[^>]+src="([^"]+)"', text):
            if not src.startswith(('http', 'data:')) and not os.path.exists(os.path.normpath(os.path.join(ROOT, base, src))):
                problems.append('%s: screenshot %s is missing' % (rel, src))
        wr(rel, text)
        url = SITE + base + ('' if pg['file'] == 'index.html' else pg['file'])
        sitemap.append(url)
        llms_docs.append('- [%s](%s)' % (pg['title'], url))

# ---------------------------------------------------------------- blog
posts = json.loads(rd('blog/posts.json'))
live = [p for p in posts if not p.get('draft')]
live.sort(key=lambda p: p.get('date', ''), reverse=True)
for p in live:
    for k in ('url', 'title', 'summary', 'date'):
        if not p.get(k):
            problems.append('blog/posts.json: a post is missing "%s"' % k)
    if p.get('url') and not os.path.exists(os.path.join(ROOT, 'blog', p['url'])):
        problems.append('blog/posts.json lists %s but blog/%s does not exist' % (p['url'], p['url']))

idx = rd('blog/index.html')
if live:
    cards = ''.join(
        '<a class="post card" href="%s">%s<small>%s</small><h2>%s</h2><p>%s</p><span class="meta">%s%s</span></a>' % (
            E(p['url']), '<img src="%s" alt="" loading="lazy">' % E(p['image']) if p.get('image') else '',
            E(p.get('category', 'Article')), E(p['title']), E(p['summary']),
            E(p.get('date', '')), ' · %s min read' % p['minutes'] if p.get('minutes') else '') for p in live)
    body = '<div class="posts" id="posts">' + cards + '</div>'
else:
    body = ('<div class="posts" id="posts"></div><div class="bempty card" id="bempty"><b>First articles are on the way.</b>'
            '<p>Guides on running voice AI in procurement, supplier operations and customer support. Until then, the docs cover how Echo works.</p>'
            '<a class="cta" href="../docs/">Read the docs</a></div>')
idx = re.sub(r'<div class="posts" id="posts">.*?</div>(<div class="bempty card" id="bempty">.*?</div>)?(?=\s*</main>)', lambda m: body, idx, count=1, flags=re.S)
ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Echo by Cognilix blog", "url": SITE + 'blog/',
      "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": SITE + 'blog/' + p['url'], "datePublished": p.get('date', '')} for p in live]}
idx = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Blog".*?</script>',
             lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', idx, count=1, flags=re.S)
idx = fix_chrome(idx, '../', 'blog/')
wr('blog/index.html', idx)
sitemap.append(SITE + 'blog/')
sitemap += [SITE + 'blog/' + p['url'] for p in live]
for f in os.listdir(os.path.join(ROOT, 'blog')):
    if f.endswith('.html') and f not in ('index.html', '_template.html'):
        wr('blog/' + f, fix_chrome(rd('blog/' + f), '../', 'blog/'))

# ---------------------------------------------------------------- sitemap and llms.txt
wr('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
   ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, TODAY) for u in sitemap) + '</urlset>\n')
llms = ['# Echo by Cognilix', '> Enterprise Voice AI for B2B operations: supplier and customer calls that confirm POs, dates, quotes and payments, with outcomes written back to the ERP.']
llms += llms_docs
if live:
    llms += ['\n## Blog'] + ['- [%s](%sblog/%s)' % (p['title'], SITE, p['url']) for p in live]
wr('llms.txt', '\n'.join(llms) + '\n')

for p in problems:
    print('PROBLEM', p)
print(('would change: ' if CHECK else 'changed: ') + (', '.join(changed) or 'nothing'))
sys.exit(1 if problems else 0)
