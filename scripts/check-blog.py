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
  super().__init__(); self.tags=[]; self.blocks=[]; self.cells=[]; self.cell=None; self.capture=None; self.depth=0; self.prose=False; self.prose_depth=0; self.json=[]; self.script=None; self.audio=False; self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs); self.tags.append((tag,a))
  if tag=='aside' and a.get('class')=='blog-audio': self.audio=True
  if self.audio: return
  if tag=='script' and a.get('type')=='application/ld+json': self.script=''
  if 'data-article-intro' in a: self.capture=''
  if 'data-article-body' in a: self.prose=True
  if self.prose and tag in ['p','h2','h3','li']: self.capture=''
  if self.prose and tag in ['th','td']: self.cell=''
 def handle_data(self,data):
  if self.capture is not None:self.capture+=data
  if self.cell is not None:self.cell+=data
  if self.script is not None:self.script+=data
 def handle_endtag(self,tag):
  if self.audio:
   if tag=='aside': self.audio=False
   return
  if self.capture is not None and tag in ['p','h2','h3','li']:self.blocks.append(self.capture);self.capture=None
  if self.cell is not None and tag in ['th','td']:self.cells.append(self.cell);self.cell=None
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
  assert alt=={**{b.language_tag(l,article):b.BASE+b.route(l,article) for l in b.COPY},'x-default':b.BASE+b.route(article.get('xDefaultLang','uk') if article else 'uk',article)}
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
   expected=[re.sub(r'^#\s+','',block) if i==0 else block for i,block in enumerate(b.source(article,lang).split('\n\n'))]
   if article.get('tables'):
    table_blocks=[block for block in expected if block.startswith('| ')]
    expected_cells=[cell.strip() for block in table_blocks for line in block.splitlines() if not re.fullmatch(r'\|[|:\- ]+\|',line) for cell in line.strip().strip('|').split('|')]
    assert p.cells==expected_cells,(route,'table changed')
    expected=[block for block in expected if not block.startswith('| ')]
   expected=[re.sub(r'^#{2,3} ','',block).replace('`','') if article.get('inlineCode') else re.sub(r'^#{2,3} ','',block) for block in expected]
   if article.get('inlineStrong'): expected=[re.sub(r'\*\*(.+?)\*\*',r'\1',block) for block in expected]
   if article.get('inlineEmphasis'): expected=[re.sub(r'\*(.+?)\*',r'\1',block) for block in expected]
   if article.get('orderedLists'):
    expected=[re.sub(r'^\d+\. ', '', line) for block in expected for line in (block.splitlines() if block.startswith('1. ') else [block])]
   if article.get('unorderedLists'):
    expected=[re.sub(r'^- ', '', line) for block in expected for line in (block.splitlines() if block.startswith('- ') else [block])]
   audio=article['translations'][lang].get('audio')
   assert sum(tag=='audio' for tag,a in p.tags)==bool(audio)
   if audio:
    assert schema['associatedMedia']['contentUrl']==b.BASE+audio['src']
    expected_preload='metadata' if article['id']=='geo-optimization-europe' else 'none'
    assert all(a.get('preload')==expected_preload and 'autoplay' not in a for tag,a in p.tags if tag=='audio')
   assert p.blocks==expected,(route,'article changed')
   assert schema['author']['name']==('Raccoon SEO Studio' if article['translations'][lang].get('author')=='Raccoon SEO Studio' else 'Oleksandr Padalko')
   assert schema['datePublished']==article['published'] and schema['dateModified']==article['modified']
  checked+=1
print(f'PASS: {checked} routes; exact article text, local links, canonicals, language switching, hreflang, JSON-LD and sitemap.')
