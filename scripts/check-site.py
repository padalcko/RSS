#!/usr/bin/env python3
"""Static site regression checks. Run from any directory: python3 scripts/check-site.py."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raccoon-studio.com.ua/'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.text = path.read_text()
        self.tags = []
        self.feed(self.text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs), self.getpos()[0]))
    def select(self, tag, **attrs):
        return [a for t, a, _ in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]

pages = {str(p.relative_to(ROOT)): Page(p) for p in ROOT.rglob('*.html')}
indexable = {f: p for f, p in pages.items() if f != '404.html'}
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

def route(file):
    return '/' + file.removesuffix('index.html')

def local_target(url, file):
    parsed = urlsplit(urljoin(BASE + file, url))
    if parsed.netloc != 'raccoon-studio.com.ua' or parsed.scheme not in ('https', 'http'):
        return None, None
    target = unquote(parsed.path).lstrip('/')
    if not target or target.endswith('/'):
        target += 'index.html'
    return target, unquote(parsed.fragment)

titles = []
descriptions = []
image_count = 0
for file, page in pages.items():
    check(len(page.select('h1')) == 1, f'{file}: expected one H1')
    ids = [a['id'] for _, a, _ in page.tags if 'id' in a]
    check(len(ids) == len(set(ids)), f'{file}: duplicate IDs')
    check(len(page.select('main')) == 1, f'{file}: expected one main landmark')
    for tag, attrs, line in page.tags:
        urls = [attrs[k] for k in ('href', 'src') if k in attrs]
        urls += [part.strip().split()[0] for part in attrs.get('srcset', '').split(',') if part.strip()]
        if attrs.get('property') == 'og:image' or attrs.get('name') == 'twitter:image':
            urls.append(attrs.get('content', ''))
        for url in urls:
            target, fragment = local_target(url, file)
            if target is None:
                continue
            check((ROOT / target).is_file(), f'{file}:{line}: missing {url}')
            if fragment and target in pages:
                check(any(a.get('id') == fragment for _, a, _ in pages[target].tags), f'{file}:{line}: missing anchor {url}')
        if tag == 'img':
            image_count += 1
            check('alt' in attrs, f'{file}:{line}: missing image alt')
            check('width' in attrs and 'height' in attrs, f'{file}:{line}: missing image dimensions')
        if tag == 'a' and attrs.get('target') == '_blank':
            check('noopener' in attrs.get('rel', '').split(), f'{file}:{line}: missing noopener')
    if file == '404.html':
        check('noindex' in page.select('meta', name='robots')[0]['content'], '404 must be noindex')
        continue
    title = re.search(r'<title>(.*?)</title>', page.text, re.S).group(1).strip()
    titles.append(title)
    metas = page.select('meta', name='description')
    check(len(metas) == 1 and bool(metas[0].get('content')), f'{file}: missing description')
    descriptions.append(metas[0]['content'])
    expected = BASE.rstrip('/') + route(file)
    check(page.select('link', rel='canonical') == [{'rel': 'canonical', 'href': expected}], f'{file}: wrong canonical')
    lang = 'pl' if file.startswith('pl/') else 'uk'
    check(page.select('html')[0]['lang'] == lang, f'{file}: wrong language')
    root_route = route(file)[3:] if lang == 'pl' else route(file)
    expected_alts = {'uk': BASE.rstrip('/') + root_route, 'pl': BASE.rstrip('/') + '/pl' + root_route, 'x-default': BASE.rstrip('/') + root_route}
    alts = {a['hreflang']: a['href'] for a in page.select('link', rel='alternate') if 'hreflang' in a}
    check(alts == expected_alts, f'{file}: incorrect language alternatives')
    check(page.select('meta', property='og:url')[0]['content'] == expected, f'{file}: incorrect og:url')
    for alt in alts.values():
        target, _ = local_target(alt, file)
        check(target in indexable, f'{file}: missing language page {alt}')
    check(bool(page.select('link', rel='icon', type='image/svg+xml')), f'{file}: missing SVG favicon')
    check('case-placeholder' not in page.text, f'{file}: placeholder screenshot remains')
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page.text, re.S)
    check(bool(blocks), f'{file}: missing JSON-LD')
    for block in blocks:
        try:
            data = json.loads(block)
            wp = next(n for n in data['@graph'] if n['@type'] == 'WebPage')
            check(wp['url'] == expected and wp['inLanguage'] == lang, f'{file}: inconsistent structured data')
        except (ValueError, KeyError, StopIteration) as error:
            errors.append(f'{file}: invalid JSON-LD {error}')

check(len(set(titles)) == len(titles), 'Duplicate page titles')
check(len(set(descriptions)) == len(descriptions), 'Duplicate descriptions')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
tree = ET.parse(ROOT / 'sitemap.xml')
locations = [node.text for node in tree.findall('s:url/s:loc', ns)]
check(set(locations) == {BASE.rstrip('/') + route(f) for f in indexable}, 'Sitemap does not match indexable pages')
check(len(locations) == len(set(locations)), 'Duplicate sitemap URLs')
for node in tree.findall('s:url', ns):
    target, _ = local_target(node.find('s:loc', ns).text, 'index.html')
    expected = {a['hreflang']: a['href'] for a in indexable[target].select('link', rel='alternate') if 'hreflang' in a}
    check({a.attrib['hreflang']: a.attrib['href'] for a in node.findall('x:link', ns)} == expected, 'Sitemap hreflang mismatch')
check('Sitemap: ' + BASE + 'sitemap.xml' in (ROOT / 'robots.txt').read_text(), 'robots sitemap link missing')
manifest = json.loads((ROOT / 'site.webmanifest').read_text())
for icon in manifest['icons']:
    check((ROOT / icon['src'].lstrip('/')).is_file(), 'Missing manifest icon')
ET.parse(ROOT / 'favicon.svg')
css = (ROOT / 'styles/style.css').read_text()
for url in re.findall(r'url\([\'"]?([^\)\'"]+)', css):
    target, _ = local_target(url, 'styles/style.css')
    if target:
        check((ROOT / target).is_file(), f'Missing CSS resource: {url}')
check('prefers-reduced-motion' in css, 'Reduced motion rules missing')
redirects = {}
for line in (ROOT / '_redirects').read_text().splitlines():
    if line and not line.startswith('#'):
        source, target, status = line.split()
        check(source not in redirects, f'Duplicate redirect {source}')
        redirects[source] = target
        check((ROOT / target.lstrip('/')).exists() or target in ['/', '/pl/'], f'Missing redirect target {target}')
for source in redirects:
    visited = set()
    current = source
    while current in redirects:
        check(current not in visited, f'Redirect cycle from {source}')
        if current in visited:
            break
        visited.add(current)
        current = redirects[current]
for file in indexable:
    if file.endswith('index.html'):
        continue
    path = '/' + file
    check(redirects.get(path[:-5]) == path, f'Missing clean URL redirect: {path}')
for file in ['index.html', 'pl/index.html', 'clients.html', 'pl/clients.html']:
    page = pages[file]
    prefix = '/pl' if file.startswith('pl/') else ''
    for slug in ['gloss-garage', 'expres-polish', 'laser-tech-service', 'lts-market']:
        check(bool(page.select('a', href=f'{prefix}/cases/{slug}.html')), f'{file}: missing case {slug}')
        check(any(slug + '-1200.webp' in a.get('src', '') for a in page.select('img')), f'{file}: missing screenshot {slug}')
print(json.dumps({'pages': len(pages), 'indexable': len(indexable), 'images': image_count, 'sitemap_urls': len(locations), 'errors': errors}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
