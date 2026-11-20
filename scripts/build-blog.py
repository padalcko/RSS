#!/usr/bin/env python3
"""Build localized static blog pages, reusing the home page chrome.

Content and stable publication dates: scripts/content/blog/.
Add an entry to articles.json and localized Markdown (paragraphs, H2/H3) to publish.
Run after editing shared home page chrome. No runtime dependencies or CMS.
"""
from pathlib import Path
from gtm import inject_gtm
from html import escape as e
import json, math, re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'scripts/content/blog'
BASE = 'https://raccoon-studio.com.ua'
ARTICLES = sorted(json.loads((CONTENT / 'articles.json').read_text()), key=lambda a: a['published'], reverse=True)
COPY = {
 'uk': dict(name='Блог SEO-Єнота', subtitle='SEO, AI, розробка сайтів та автоматизація. Пишемо про те, що перевіряємо на практиці.', categories=['Усі статті','SEO','Штучний інтелект','Автоматизація','Розробка сайтів','Кейси'], search='Пошук статей...', empty='Статей не знайдено. Спробуйте інший запит або категорію.', home='Головна', crumbs='Навігаційний шлях', read='Читати статтю', minutes='хв читання', author='Олександр Падалко', authorLabel='Про автора', cta='Плануєте запуск нового сайту або хочете зрозуміти, чому чинний сайт не отримує трафіку? Raccoon SEO Studio допомагає з технічним SEO, розробкою та оптимізацією сайтів.', button='Обговорити проєкт', services='Послуги студії', image='Ілюстрація запуску сайту: структура сторінки, аналітика та перевірка індексації', mascot='Фірмовий єнот Raccoon SEO Studio в технологічній композиції', pagination='Сторінки блогу', previous='Попередня', next='Наступна', results='Знайдено статей', related='Пов’язані статті'),
 'pl': dict(name='Blog SEO Szopa', subtitle='SEO, AI, tworzenie stron i automatyzacja. Piszemy o tym, co sprawdzamy w praktyce.', categories=['Wszystkie artykuły','SEO','Sztuczna inteligencja','Automatyzacja','Tworzenie stron','Realizacje'], search='Szukaj artykułów...', empty='Nie znaleziono artykułów. Spróbuj innego zapytania lub kategorii.', home='Strona główna', crumbs='Ścieżka nawigacji', read='Czytaj artykuł', minutes='min czytania', author='Oleksandr Padalko', authorLabel='O autorze', cta='Planujesz uruchomienie nowej strony lub chcesz sprawdzić, dlaczego obecna witryna nie zdobywa ruchu? Raccoon SEO Studio zajmuje się technicznym SEO, tworzeniem i optymalizacją stron internetowych.', button='Porozmawiajmy o projekcie', services='Usługi studia', image='Ilustracja uruchomienia strony: struktura strony, analityka i kontrola indeksowania', mascot='Firmowy szop Raccoon SEO Studio w technologicznej kompozycji', pagination='Strony bloga', previous='Poprzednia', next='Następna', results='Znalezione artykuły', related='Powiązane artykuły'),
 'en': dict(name="SEO Raccoon's Blog", subtitle='SEO, AI, web development and automation. We write about what we actually test.', categories=['All articles','SEO','Artificial Intelligence','Automation','Web Development','Case Studies'], search='Search articles...', empty='No articles found. Try another search or category.', home='Home', crumbs='Breadcrumbs', read='Read article', minutes='min read', author='Oleksandr Padalko', authorLabel='About the author', cta='Planning a new website or trying to understand why your existing site gets little organic traffic? Raccoon SEO Studio works with technical SEO, web development and website optimization.', button='Discuss Your Project', services='Studio services', image='Website launch illustration: page structure, analytics and indexing checks', mascot='The Raccoon SEO Studio brand raccoon in a technology composition', pagination='Blog pages', previous='Previous', next='Next', results='Articles found', related='Related articles')
}
KEYS = ['all','seo','ai','automation','development','cases']

def home(lang): return '/' if lang == 'uk' else f'/{lang}/'
def route(lang, article=None): return home(lang)+'blog/'+(article['translations'][lang]['slug']+'/' if article else '')
def language_tag(lang,article=None): return (article or {}).get('hreflang',{}).get(lang,lang)
def source(article,lang): return (CONTENT/article['translations'][lang]['source']).read_text().strip()
def words(article,lang): return len(re.findall(r"[^\W_]+(?:[’'’-][^\W_]+)*", source(article,lang)))
def minutes(article,lang): return max(1,math.ceil(words(article,lang)/200))
def date_label(date,lang):
 y,m,d=date.split('-')
 return f'{d}.{m}.{y}' if lang != 'en' else f'{d}/{m}/{y}'

def breadcrumbs(lang,article=None):
 c=COPY[lang]; items=[(c['home'],home(lang)),(c['name'],route(lang))]
 if article: items.append((article['translations'][lang]['title'],route(lang,article)))
 html='<nav class="blog-breadcrumbs" aria-label="'+c['crumbs']+'"><ol>'
 html+=''.join('<li>'+ (f'<a href="{url}">{e(name)}</a>' if i<len(items)-1 else f'<span aria-current="page">{e(name)}</span>')+'</li>' for i,(name,url) in enumerate(items))+'</ol></nav>'
 schema={'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+url} for i,(name,url) in enumerate(items)]}
 return html,schema

def localized_visual(article, lang):
 return {**article, **{k: v for k, v in article["translations"][lang].items() if k in ("image", "socialImage")}}

def card(article,lang,link_title=None):
 article=localized_visual(article,lang)
 t=article['translations'][lang]; c={**COPY[lang], 'author':t.get('author',COPY[lang]['author'])}
 excerpt=t.get('excerpt',t['description'])
 author=f"<span>{c['author']}</span>"
 html=f'''<li class="blog-card" data-category="{article['category']}" data-search="{e(t['title']+' '+excerpt,quote=True)}"><a href="{route(lang,article)}"><img src="{article['image']}" alt="{e(t.get('imageAlt',c['image']))}" width="{article.get('imageWidth',1200)}" height="{article.get('imageHeight',675)}" loading="lazy" decoding="async"><div class="blog-card-copy"><span class="blog-category">{c['categories'][KEYS.index(article['category'])]}</span><h2>{e(link_title or t['title'])}</h2><p>{e(excerpt)}</p><p class="blog-meta">{author}<time datetime="{article['published']}">{date_label(article['published'],lang)}</time><span>{minutes(article,lang)} {c['minutes']}</span></p><span class="blog-read">{c['read']} <span aria-hidden="true">↗</span></span></div></a></li>'''

 return re.sub(r'<img[^>]*>', '', html, count=1) if not article['image'] else html

def listing(lang):
 c=COPY[lang]; bc,_=breadcrumbs(lang)
 filters=''.join(f'<button type="button" data-category="{key}" aria-pressed="{str(i==0).lower()}">{e(label)}</button>' for i,(key,label) in enumerate(zip(KEYS,c['categories'])))
 return f'''<section class="blog-hero"><div class="container">{bc}<div class="blog-hero-grid"><div><p class="blog-eyebrow">RACCOON SEO STUDIO</p><h1>{e(c['name'])}</h1><p class="blog-subtitle">{e(c['subtitle'])}</p></div><div class="blog-scene"><div class="blog-window" aria-hidden="true"><span>● ● ●</span><div>&lt;seo /&gt;<br>↗</div></div><img src="/images/brand/raccoon-logo.webp" width="463" height="512" alt="{c['mascot']}" fetchpriority="high" decoding="async"></div></div></div></section>
<section class="section blog-listing"><div class="container" data-blog><div class="blog-tools" hidden><label class="blog-search"><span>{c['search']}</span><input type="search" placeholder="{c['search']}" aria-controls="blog-results" autocomplete="off"></label><div class="blog-filters" role="group" aria-label="{e(c['categories'][0])}">{filters}</div></div><p class="blog-count" aria-live="polite" data-label="{c['results']}"></p><ul id="blog-results" class="blog-grid">{''.join(card(a,lang) for a in ARTICLES if lang in a['translations'])}</ul><p class="blog-empty" hidden>{c['empty']}</p><nav class="blog-pagination" aria-label="{c['pagination']}" hidden><button type="button" data-page="previous">{c['previous']}</button><span aria-live="polite"></span><button type="button" data-page="next">{c['next']}</button></nav></div></section>'''

def article_body(article,lang):
 article=localized_visual(article,lang)
 t=article['translations'][lang]; c={**COPY[lang], 'author':t.get('author',COPY[lang]['author'])}; bc,_=breadcrumbs(lang,article)
 blocks=source(article,lang).split('\n\n')
 intro=blocks.pop(0)
 body='\n'.join(f'<h3>{e(b[4:])}</h3>' if b.startswith('### ') else f'<h2>{e(b[3:])}</h2>' if b.startswith('## ') else f'<p>{e(b)}</p>' for b in blocks)
 related=[a for a in ARTICLES if a['id']!=article['id'] and a['category']==article['category'] and lang in a['translations'] and ('relatedIds' not in article or a['id'] in article['relatedIds'])][:3]
 if article.get('inlineCode'): body=re.sub(r'`([^`]+)`',r'<code>\1</code>',body)
 if article.get('inlineStrong'): body=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',body)
 cta_button=(f"<a class=\"nav-cta\" style=\"color: var(--white)\" href=\"{home(lang)}#contacts\">{e(t.get('button',c['button']))}</a>" if article.get('contactLink') else f"<button type=\"button\" class=\"nav-cta js-open-modal\">{e(t.get('button',c['button']))}</button>")
 cta_heading=f"<h2>{e(t['ctaTitle'])}</h2>" if t.get('ctaTitle') else ''
 cta_html=f'<aside class="blog-cta">{cta_heading}<p>{e(t.get("cta",c["cta"]))}</p><div>{cta_button}<a href="{home(lang)}#services">{c["services"]}</a></div></aside>' if article.get('showCta',True) else ''
 related_html=f'<section class="blog-related"><h2>{c["related"]}</h2><ul class="blog-grid">'+''.join(card(a,lang,t.get('relatedTitles',{}).get(a['id'])) for a in related)+'</ul></section>' if related else ''
 if t.get('serviceLinkText'):
  text=e(t['serviceLinkText'])
  body=body.replace(text, f'<a href="{home(lang)}#services">{text}</a>', 1)
 html=f'''<div class="container blog-article-container">{bc}<article><header class="blog-article-heading"><p class="blog-category">{c['categories'][KEYS.index(article['category'])]}</p><h1>{e(t['title'])}</h1><p class="blog-intro" data-article-intro>{e(intro)}</p><div class="blog-meta"><span>{c['author']}</span><time datetime="{article['published']}">{date_label(article['published'],lang)}</time><span>{minutes(article,lang)} {c['minutes']}</span></div></header><img class="blog-article-image" src="{article['image']}" alt="{e(t.get('imageAlt',c['image']))}" width="{article.get('imageWidth',1200)}" height="{article.get('imageHeight',675)}" fetchpriority="high" decoding="async"><div class="blog-prose" data-article-body>{body}</div><aside class="blog-author"><h2>{c['authorLabel']}</h2><p>{c['author']}</p><p>Frontend Developer / SEO Engineer</p><p>Raccoon SEO Studio</p></aside></article>{cta_html}{related_html}</div>'''

 return re.sub(r'<img class="blog-article-image"[^>]*>', '', html) if not article['image'] else html

def semantic_html(html):
 """Normalize publication semantics without rewriting existing content or chrome."""
 def publication(m):
  card=m[0]
  if '<article>' not in card:
   card=re.sub(r'(<li\b[^>]*>)',r'\1<article>',card,count=1)
   card=card.replace('</li>','</article></li>')
  return card
 html=re.sub(r'<li\s+class="blog-card".*?</li>',publication,html,flags=re.S)
 def related(m):
  return re.sub(r'(<article>.*?</article>)',lambda card:card[0].replace('<h2>','<h3>').replace('</h2>','</h3>'),m[0],flags=re.S)
 html=re.sub(r'<section class="blog-related">.*?</section>',related,html,flags=re.S)
 html=re.sub(r'(<nav class="blog-pagination"[^>]*>.*?)<span aria-live="polite">',r'\1<span aria-live="polite" aria-current="page">',html,flags=re.S)
 return html

def build_page(lang,article=None):
 c=COPY[lang]; url=BASE+route(lang,article); t=article['translations'][lang] if article else None
 title=t.get('seoTitle',t['title']) if t else c['name']+' | Raccoon SEO Studio'
 description=t['description'] if t else c['subtitle']
 visual=article or next(a for a in ARTICLES if a['id']=='website-launch')
 visual=localized_visual(visual,lang)
 social=BASE+visual['socialImage'] if visual['socialImage'] else ''
 image_alt=visual['translations'][lang].get('imageAlt',c['image'])
 original=(ROOT/(home(lang).strip('/')+'/' if lang!='uk' else '')/'index.html').read_text()
 header=re.search(r'<header\b.*?</header>',original,re.S)[0]
 for target in COPY:
  header=re.sub(r'href="[^"]+"( class="language-link" lang="'+target+r'")',lambda m:'href="'+route(target,article)+'"'+m[1],header)
 header=header.replace(f'class="nav-link" href="{route(lang)}"',f'class="nav-link active" href="{route(lang)}"'+(' aria-current="page"' if not article else ''))
 footer=re.search(r'<footer\b.*?</footer>',original,re.S)[0].replace('href="#',f'href="{home(lang)}#')
 modal=original[original.index('  <div class="js-backdrop'):original.index('  <!-- JS -->')]
 skip=re.search(r'<a[^>]*class="skip-link".*?</a>',original,re.S)[0]
 # Keep existing font, CSS, favicon and manifest declarations from the source page.
 common='\n'.join(re.findall(r'<link\b(?=[^>]*(?:rel="(?:stylesheet|preconnect|icon|shortcut icon|apple-touch-icon|manifest)"))[^>]*>',original,re.S))
 publisher={'@type':'Organization','@id':BASE+'/#organization','name':'Raccoon SEO Studio','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/images/brand/raccoon-icon-512.png'}}
 _,bc=breadcrumbs(lang,article)
 author={'@type':'Person','name':'Oleksandr Padalko','jobTitle':'Frontend Developer / SEO Engineer','worksFor':{'@id':BASE+'/#organization'}}
 schema={'@type':'BlogPosting' if article else 'Blog','@id':url+'#'+('article' if article else 'blog'),'url':url,'name':title,'description':description,'inLanguage':lang,'publisher':{'@id':BASE+'/#organization'}}
 if article: schema.update(headline=t['title'],author=author,datePublished=article['published'],dateModified=article['modified'],image=social,wordCount=words(article,lang),articleSection=c['categories'][KEYS.index(article['category'])],mainEntityOfPage={'@type':'WebPage','@id':url},isPartOf={'@type':'Blog','@id':BASE+route(lang)+'#blog','name':c['name']})
 else: schema['blogPost']=[{'@type':'BlogPosting','headline':a['translations'][lang]['title'],'url':BASE+route(lang,a),'author':author,'datePublished':a['published'],'dateModified':a['modified'],**({'image':BASE+localized_visual(a,lang)['socialImage']} if localized_visual(a,lang)['socialImage'] else {})} for a in ARTICLES if lang in a['translations']]
 if article and not social: schema.pop('image',None)
 alternates='\n'.join(f'<link rel="alternate" hreflang="{language_tag(l,article)}" href="{BASE+route(l,article)}">' for l in COPY)+f'\n<link rel="alternate" hreflang="x-default" href="{BASE+route("uk",article)}">'
 locale={'uk':'uk_UA','pl':'pl_PL','en':'en_GB'}
 og_locales='\n'.join(f'<meta property="og:locale:alternate" content="{value}">' for l,value in locale.items() if l!=lang)
 html=f'''<!DOCTYPE html>
<html lang="{lang}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}">
<meta name="author" content="Oleksandr Padalko"><meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">{alternates}
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:site_name" content="Raccoon SEO Studio"><meta property="og:locale" content="{locale[lang]}">{og_locales}
<meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social}"><meta property="og:image:width" content="{visual.get('imageWidth',1200)}"><meta property="og:image:height" content="{visual.get('imageHeight',675)}"><meta property="og:image:alt" content="{e(image_alt)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title,quote=True)}"><meta name="twitter:description" content="{e(description,quote=True)}"><meta name="twitter:image" content="{social}"><meta name="twitter:image:alt" content="{e(image_alt)}">
{common}
<link rel="stylesheet" href="/styles/blog.css"><meta name="theme-color" content="#4D5AE5">
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':[publisher,bc,schema]},ensure_ascii=False)}</script>
</head><body class="studio-v5 blog-page">
{skip}
{header}
<main id="main-content" tabindex="-1">{article_body(article,lang) if article else listing(lang)}</main>
{footer}
{modal}
<script src="/script/script.js" defer></script>
{'' if article else '<script src="/script/blog.js" defer></script>'}
</body></html>
'''
 if not social:
  html=re.sub(r'<meta (?:property="og:image[^"]*"|name="twitter:image[^"]*")[^>]*>', '', html)
  html=html.replace('content="summary_large_image"', 'content="summary"')
 out=ROOT/route(lang,article).strip('/')/'index.html'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(inject_gtm(semantic_html(html)))


def build():
 import sys
 if '--semantics' in sys.argv:
  for lang in COPY:
   for path in (ROOT/route(lang).strip('/')).rglob('*.html'):
    path.write_text(semantic_html(path.read_text()))
  print('Updated blog semantics from the shared generator; content and chrome retained.')
  return
 selected=next((a for a in ARTICLES if a['id']==sys.argv[1]),None) if len(sys.argv)>1 else None
 for lang in COPY:
  if selected:
   path=ROOT/route(lang).strip('/')/'index.html'
   existing=path.read_text()
   if route(lang,selected) not in existing:
    existing=re.sub(r'(<ul\b[^>]*id="blog-results"[^>]*>)',lambda m:m[0]+card(selected,lang),existing,count=1)
    def add_schema(m):
     data=json.loads(m[1])
     for item in data.get('@graph',[]):
      if item.get('@type')=='Blog':
       item['blogPost'].insert(0,{'@type':'BlogPosting','headline':selected['translations'][lang]['title'],'url':BASE+route(lang,selected),'author':{'@type':'Person','name':'Oleksandr Padalko'},'datePublished':selected['published'],'dateModified':selected['modified'],**({'image':BASE+localized_visual(selected,lang)['socialImage']} if localized_visual(selected,lang)['socialImage'] else {})})
     return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
    existing=re.sub(r'<script type="application/ld\+json">(.*?)</script>',add_schema,existing,flags=re.S)
    path.write_text(semantic_html(existing))
   build_page(lang,selected)
  else:
   build_page(lang)
   for article in ARTICLES:
    if lang in article['translations']: build_page(lang,article)
 # Preserve existing sitemap bytes outside this generated block.
 path=ROOT/'sitemap.xml'; sitemap=path.read_text()
 sitemap=re.sub(r'\s*<!-- BLOG START -->.*?<!-- BLOG END -->','',sitemap,flags=re.S)
 entries=[]
 for article in [None]+ARTICLES:
  for lang in COPY:
   links=''.join(f'<xhtml:link rel="alternate" hreflang="{language_tag(l,article)}" href="{BASE+route(l,article)}" />' for l in COPY)
   links+=f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE+route("uk",article)}" />'
   entries.append(f'  <url><loc>{BASE+route(lang,article)}</loc>'+ (f'<lastmod>{article["modified"]}</lastmod>' if article else '')+links+'</url>')
 sitemap=sitemap.replace('</urlset>','  <!-- BLOG START -->\n'+'\n'.join(entries)+'\n  <!-- BLOG END -->\n</urlset>'); path.write_text(sitemap)
 print('Built 3 blog indexes and',sum(len(a['translations']) for a in ARTICLES),'article pages.')

if __name__=='__main__':
 build()
 from ai_resources import build as build_ai
 build_ai()
