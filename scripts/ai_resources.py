#!/usr/bin/env python3
"""Generate AI representations from sitemap-listed canonical HTML (standard library only).

Adapted from LTS Market's ai_resources.py. HTML is never modified.
Run directly, or use --check to validate freshness without writing files.
"""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raccoon-studio.com.ua'
LANGUAGES = {'uk': 'Українська', 'pl': 'Polski', 'en': 'English'}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SKIP = set('script style nav footer noscript form input select textarea button svg iframe'.split())

class Node:
    def __init__(self, tag='', attrs=(), parent=None, data=''):
        self.tag, self.attrs, self.parent, self.data = tag, dict(attrs), parent, data
        self.children = []

    def all(self, tag=None):
        for child in self.children:
            if tag is None or child.tag == tag:
                yield child
            yield from child.all(tag)

    def text(self):
        return re.sub(r'\s+', ' ', self.raw()).strip()

    def raw(self):
        return self.data + ''.join(c.raw() for c in self.children)

    def has(self, cls):
        return cls in self.attrs.get('class', '').split()


class Parser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.current = self.root
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        node = self.current
        while node.parent:
            if node.tag == tag:
                self.current = node.parent
                return
            node = node.parent

    def handle_data(self, data):
        self.current.children.append(Node(parent=self.current, data=data))


def markdown_url(canonical):
    return canonical + 'index.md' if canonical.endswith('/') else canonical.removesuffix('.html') + '.md'


def excluded(node):
    classes = node.attrs.get('class','').split()
    return (node.tag in SKIP or node.attrs.get('aria-hidden')=='true' or 'hidden' in node.attrs
            or any('breadcrumb' in c for c in classes) or node.has('button')
            or any(node.has(c) for c in ('blog-scene', 'blog-eyebrow', 'hero-label', 'blog-read')))


def render(node, page, images=None):
    if images is None: images=set()
    if node.has('faq-question'): return '\n\n### '+node.text()+'\n\n'
    if excluded(node) or node.tag=='h1': return ''
    if not node.tag: return re.sub(r'\s+',' ',node.data)
    if node.tag=='img':
        src,alt=node.attrs.get('src',''),node.attrs.get('alt','')
        if not src or not alt or src in images: return ''
        images.add(src)
        return '\n\n!['+alt.replace('[','\\[').replace(']','\\]')+']('+urljoin(page['canonical'],src)+')\n\n'
    if node.tag=='table':
        rows=[]
        for row in node.all('tr'):
            cells=[clean(render(c,page,images)).replace('|','\\|').replace('\n','<br>') for c in row.children if c.tag in ['th','td']]
            if cells: rows.append(cells)
        if not rows:return ''
        width=max(map(len,rows)); rows=[r+['']*(width-len(r)) for r in rows]
        lines=['| '+' | '.join(r)+' |' for r in rows]
        lines.insert(1,'| '+' | '.join(['---']*width)+' |')
        return '\n\n'+'\n'.join(lines)+'\n\n'
    body=''.join(render(c,page,images) for c in node.children)
    if node.has('blog-meta'):
        body = ' · '.join(c.text() for c in node.children if c.tag and not excluded(c))
    if node.tag=='a':
        href=node.attrs.get('href','')
        if not href or href.startswith('javascript:'): return body
        if re.search(r'^#{2,6} ', body, re.M):
            return re.sub(r'^(#{2,6}) (.+)$', lambda m: m[1]+' ['+m[2]+']('+urljoin(page['canonical'],href)+')', body, count=1, flags=re.M)
        if '![' in body: return body
        label=re.sub(r'\s+',' ',body).strip()
        return '['+label+']('+urljoin(page['canonical'],href)+')' if label else ''
    if node.tag in ['h2','h3','h4','h5','h6']:
        return '\n\n'+'#'*int(node.tag[1])+' '+body.strip()+'\n\n'
    if node.tag=='summary': return '\n\n### '+body.strip()+'\n\n'
    if node.tag in ['strong','b']: return '**'+body.strip()+'**' if body.strip() else ''
    if node.tag in ['em','i']: return '*'+body.strip()+'*' if body.strip() else ''
    if node.tag=='br': return '\n'
    if node.tag=='li':
        if re.search(r'^#{2,6} ', body, re.M): return '\n\n'+body.strip()+'\n\n'
        return '\n- '+body.strip()+'\n'
    if node.tag=='ol':
        items=[clean(render(c,page,images)).removeprefix('- ') for c in node.children if c.tag=='li']
        return '\n\n'+'\n'.join(f'{i}. {item}' for i,item in enumerate(items,1))+'\n\n'
    if node.tag in ['p','div','section','header','main','article','aside','figure','figcaption','address','details','ul','dl','dt','dd']:
        return '\n\n'+body.strip()+'\n\n' if body.strip() else ''
    return body


def clean(text):
    text=re.sub(r'[ \t]+\n','\n',text)
    text=re.sub(r'\n[ \t]+','\n',text)
    return re.sub(r'\n{3,}','\n\n',text).strip()



def local_path(url):
    path = ROOT / unquote(urlsplit(url).path).lstrip('/')
    assert path.resolve().is_relative_to(ROOT), url
    return path / 'index.html' if urlsplit(url).path.endswith('/') else path


def discover():
    urls = [n.text for n in ET.parse(ROOT/'sitemap.xml').findall('{*}url/{*}loc')]
    assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
    pages = []
    for url in sorted(urls):
        assert url.startswith(BASE+'/') and url.endswith(('/', '.html')), url
        path = local_path(url)
        assert not set(path.relative_to(ROOT).parts) & {'scripts', 'docs', '.git'}, path
        tree = Parser(path.read_text()).root
        nodes = list(tree.all())
        meta = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content', '') for n in nodes if n.tag == 'meta'}
        assert 'noindex' not in meta.get('robots', '').lower(), url
        assert [n.attrs.get('href') for n in nodes if n.tag == 'link' and n.attrs.get('rel') == 'canonical'] == [url], url
        lang = next(n.attrs['lang'] for n in nodes if n.tag == 'html')
        assert lang in LANGUAGES, url
        h1 = list(tree.all('h1')); main = list(tree.all('main'))
        assert len(h1) == len(main) == 1, url
        assert meta.get('description') and next(tree.all('title')).text(), url
        for key in ('og:title', 'og:description', 'og:url', 'og:image', 'og:type', 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'):
            assert meta.get(key), (url, key)
        schemas = []
        for n in tree.all('script'):
            if n.attrs.get('type') == 'application/ld+json':
                data = json.loads(n.raw())
                schemas.extend(data.get('@graph', [data]))
        ids = [n['@id'] for n in schemas if '@id' in n]
        assert len(ids) == len(set(ids)), (url, 'duplicate schema IDs')
        types = [n.get('@type') for n in schemas]
        article = 'BlogPosting' in types or 'Article' in types
        if any('breadcrumb' in n.attrs.get('class', '') for n in nodes):
            assert types.count('BreadcrumbList') == 1, url
        if path.relative_to(ROOT).as_posix() in ('index.html', 'pl/index.html', 'en/index.html'):
            assert types.count('Organization') == 1, url
        alts = {n.attrs['hreflang'].split('-')[0] if n.attrs['hreflang'] != 'x-default' else 'x-default': n.attrs['href'] for n in tree.all('link') if 'hreflang' in n.attrs}
        assert {'uk', 'pl', 'x-default'} <= alts.keys(), url
        if '/blog/' in url or url in (BASE+'/', BASE+'/pl/', BASE+'/en/'):
            assert 'en' in alts, url
        pages.append(dict(path=path, tree=tree, main=main[0], meta=meta, lang=lang,
                          canonical=url, title=h1[0].text(), md=markdown_url(url),
                          article=article, schemas=schemas, alternates=alts))
    lookup = {p['canonical']: p for p in pages}
    for p in pages:
        for lang, url in p['alternates'].items():
            assert url in lookup and p['canonical'] in lookup[url]['alternates'].values(), (p['canonical'], url)
            assert lang == 'x-default' or lookup[url]['lang'] == lang, url
        # Validate links and fragments in source, including links retained in Markdown.
        for node in p['tree'].all():
            for attr in ('href', 'src'):
                value = node.attrs.get(attr)
                if not value: continue
                url = urljoin(p['canonical'], value)
                parsed = urlsplit(url)
                if parsed.netloc != urlsplit(BASE).netloc or parsed.scheme not in ('http', 'https'): continue
                target = local_path(url)
                assert target.is_file(), (p['canonical'], value)
                if parsed.fragment and target.suffix == '.html':
                    target_tree = lookup.get(url.split('#')[0], {}).get('tree') or Parser(target.read_text()).root
                    assert any(n.attrs.get('id') == unquote(parsed.fragment) for n in target_tree.all()), (url, 'missing fragment')
    return pages


def markdown(page):
    labels = {'uk': ('Мова', 'Канонічна HTML-сторінка'), 'pl': ('Język', 'Kanoniczna strona HTML'), 'en': ('Language', 'Canonical HTML page')}[page['lang']]
    return (f'# {page["title"]}\n\n{labels[0]}: {LANGUAGES[page["lang"]]}\n\n'
            f'{labels[1]}: {page["canonical"]}\n\n> {page["meta"]["description"]}\n\n'
            + clean(render(page['main'], page)) + '\n')


def outputs(pages):
    generated = {p['path'].with_suffix('.md'): markdown(p) for p in pages}
    llms = '''# Raccoon SEO Studio

Raccoon SEO Studio — вебстудія, що спеціалізується на розробці сайтів, технічному SEO, AI-автоматизації та інтеграції цифрових інструментів для бізнесу.

Website: https://raccoon-studio.com.ua/

Languages: Ukrainian, Polish, English.

Основні напрямки:

- Website Development
- Technical SEO
- SEO Optimization
- AI Automation
- Business Process Automation
- n8n Integrations
- Website Performance Optimization
- Analytics Integration

## Pages / Сторінки / Strony

'''
    for p in pages:
        llms += f'- [{p["lang"]} — {p["title"]}]({p["canonical"]}) — [Markdown]({p["md"]})\n'
    llms += f'\n## AI resources\n\n- [Full text]({BASE}/llms-full.txt)\n- [Catalogue]({BASE}/ai-catalog.json)\n'
    generated[ROOT/'llms.txt'] = llms
    generated[ROOT/'llms-full.txt'] = '# Raccoon SEO Studio\n\n' + '\n---\n\n'.join(
        re.sub(r'^(#{1,6}) ', lambda m: '#' * min(len(m[1])+1, 6) + ' ', markdown(p), flags=re.M) for p in pages)
    catalog = dict(name='Raccoon SEO Studio', url=BASE+'/', type='Web Development and SEO Studio',
                   languages=list(LANGUAGES), services=[], articles=[], pages=[], contact={})
    for p in pages:
        entry = dict(name=p['title'], description=p['meta']['description'], language=p['lang'], url=p['canonical'], markdown=p['md'])
        catalog['pages'].append(entry)
        if p['article']: catalog['articles'].append(entry.copy())
        services = next((n for n in p['main'].all() if n.attrs.get('id') == 'services'), None)
        if services:
            for item in services.all('li'):
                heading = next(item.all('h2'), None)
                if heading:
                    catalog['services'].append(dict(name=heading.text(), description=' '.join(n.text() for n in item.all('p')), language=p['lang'], url=p['canonical']+'#services'))
        if p['canonical'] == BASE+'/':
            org = next(n for n in p['schemas'] if n.get('@type') == 'Organization')
            catalog['contact'] = {key: org[key] for key in ('email', 'telephone', 'address', 'contactPoint', 'sameAs') if key in org}
    generated[ROOT/'ai-catalog.json'] = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    begin, end = '# BEGIN GENERATED AI HEADERS', '# END GENERATED AI HEADERS'
    headers = begin + '\n# Generated by scripts/ai_resources.py; HTML remains canonical.\n'
    for p in pages:
        headers += (f'\n{urlsplit(p["md"]).path}\n  Content-Type: text/markdown; charset=utf-8\n'
                    f'  Link: <{p["canonical"]}>; rel="canonical"\n  X-Robots-Tag: noindex\n')
    for filename, mime in [('llms.txt', 'text/plain'), ('llms-full.txt', 'text/plain'), ('ai-catalog.json', 'application/json')]:
        headers += f'\n/{filename}\n  Content-Type: {mime}; charset=utf-8\n'
    headers += end + '\n'
    existing = (ROOT/'_headers').read_text()
    generated[ROOT/'_headers'] = re.sub(re.escape(begin)+r'.*?'+re.escape(end)+r'\n?', lambda m: headers, existing, flags=re.S) if begin in existing else existing+'\n'+headers
    return generated


def build(check=False):
    pages = discover()
    generated = outputs(pages)
    catalog = json.loads(generated[ROOT/'ai-catalog.json'])
    assert len(catalog['pages']) == len(pages)
    assert len({p['url'] for p in catalog['articles']}) == len(catalog['articles'])
    for p in pages:
        md = generated[p['path'].with_suffix('.md')]
        assert len(re.findall(r'^# ', md, re.M)) == 1, p['canonical']
        assert p['canonical'] in md and LANGUAGES[p['lang']] in md
    for path, content in generated.items():
        if path.suffix not in ('.md', '.txt'): continue
        for url in re.findall(r'\]\((https://raccoon-studio\.com\.ua/[^)]*)\)', content):
            target = local_path(url)
            assert target in generated or target.is_file(), (path, url)
    stale = [str(p.relative_to(ROOT)) for p, text in generated.items() if not p.exists() or p.read_text() != text]
    # Do not delete hand-maintained or orphaned representations silently.
    for path in ROOT.rglob('*.md'):
        if path in generated or any(part.startswith('.') or part in ('scripts', 'docs') for part in path.relative_to(ROOT).parts): continue
        if re.search(r'^(Канонічна HTML-сторінка|Kanoniczna strona HTML|Canonical HTML page):', path.read_text(), re.M):
            raise ValueError(f'Orphan generated Markdown requires review: {path}')
    if check and stale: raise SystemExit('Stale AI resources: '+', '.join(stale))
    if not check:
        for path, text in generated.items():
            if str(path.relative_to(ROOT)) in stale: path.write_text(text)
    print(f'PASS: {len(pages)} Markdown pages; AI JSON, metadata, hreflang, source links and fragments valid; '+('outputs fresh.' if check else f'{len(stale)} files updated.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
