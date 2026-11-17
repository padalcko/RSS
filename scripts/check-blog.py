#!/usr/bin/env python3
"""Focused checks for generated blog routes, metadata, links and exact article copy."""
from pathlib import Path
import importlib.util, json, re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

spec=importlib.util.spec_from_file_location('blog',Path(__file__).with_name('build-blog.py'))
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.tags=[]; self.blocks=[]; self.capture=None; self.depth=0; self.prose=False; self.prose_depth=0; self.json=[]; self.script=None; self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs); self.tags.append((tag,a))
  if tag=='script' and a.get('type')=='application/ld+json': self.script=''
  if 'data-article-intro' in a: self.capture=''
  if 'data-article-body' in a: self.prose=True
  if self.prose and tag in ['p','h2','h3']: self.capture=''
 def handle_data(self,data):
  if self.capture is not None:self.capture+=data
  if self.script is not None:self.script+=data
 def handle_endtag(self,tag):
  if self.capture is not None and tag in ['p','h2','h3']:self.blocks.append(self.capture);self.capture=None
  if tag=='div' and self.prose:self.prose=False
  if tag=='script' and self.script is not None:self.json.append(json.loads(self.script));self.script=None

sitemap=ET.fromstring((b.ROOT/'sitemap.xml').read_text()); urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
checked=0
for article in [None]+b.ARTICLES:
 for lang in b.COPY:
  route=b.route(lang,article); path=b.ROOT/route.strip('/')/'index.html'; text=path.read_text(); p=Page(text)
  assert sum(t=='h1' for t,a in p.tags)==1,route
  canonical=[a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='canonical'];assert canonical==[b.BASE+route]
  alt={a['hreflang']:a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='alternate'}
  assert alt=={**{l:b.BASE+b.route(l,article) for l in b.COPY},'x-default':b.BASE+b.route('uk',article)}
  languages={a['lang']:a['href'] for t,a in p.tags if t=='a' and a.get('class')=='language-link'}
  assert languages=={l:b.route(l,article) for l in b.COPY}
  assert urls.count(b.BASE+route)==1
  graph=p.json[0]['@graph']; schema=graph[-1]
  assert schema['url']==b.BASE+route and graph[1]['@type']=='BreadcrumbList'
  assert not any(a.get('content','').startswith('noindex') for t,a in p.tags)
  for tag,a in p.tags:
   url=a.get('src',a.get('href',''))
   if not url.startswith('/') or url.startswith('//'):continue
   target=url.split('#')[0]; dest=b.ROOT/target.lstrip('/')
   assert dest.exists(),(route,url)
   if '#' in url:
    content=(dest/'index.html' if dest.is_dir() else dest).read_text()
    assert f'id="{url.split("#")[1]}"' in content,(route,url)
  if article:
   expected=[re.sub(r'^#{2,3} ','',block) for block in b.source(article,lang).split('\n\n')]
   assert p.blocks==expected,(route,'article changed')
   assert schema['author']['name']=='Oleksandr Padalko'
   assert schema['datePublished']==article['published'] and schema['dateModified']==article['modified']
  checked+=1
print(f'PASS: {checked} routes; exact article text, local links, canonicals, language switching, hreflang, JSON-LD and sitemap.')
