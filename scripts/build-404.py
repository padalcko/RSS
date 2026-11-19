#!/usr/bin/env python3
"""Build the three static error pages with the existing localized site chrome."""
from pathlib import Path
from gtm import inject_gtm
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
COPY = {
 'uk': {
  'label':'RACCOON SYSTEM / ЗВІТ ПРО ПОМИЛКУ','status':'СИСТЕМА ПРАЦЮЄ',
  'title':'Сторінка втекла з репозиторію.',
  'description':'Ми вже шукаємо винного серед комітів. А поки повернімо вас туди, де все працює.',
  'lines':['Перевіряємо маршрут...','Шукаємо сторінку в репозиторії...','Ресурс не знайдено.','Єнота-розробника повідомлено.','Варіанти відновлення доступні.'],
  'success':'Система працює. Помилка лише в маршруті.',
  'home':'На головну','work':'Переглянути кейси','contact':"Зв'язатися зі студією",
  'bottom':'ПОМИЛКА 404 · МАРШРУТ НЕ ЗНАЙДЕНО · ПОВЕРНЕННЯ ДОСТУПНЕ',
  'metaTitle':'404 — Сторінку не знайдено | Raccoon SEO Studio',
  'metaDescription':'Сторінку не знайдено. Поверніться на головну Raccoon SEO Studio або перегляньте наші проєкти.'},
 'pl': {
  'label':'RACCOON SYSTEM / RAPORT BŁĘDU','status':'SYSTEM DZIAŁA',
  'title':'Ta strona uciekła z repozytorium.',
  'description':'Już szukamy winnego wśród commitów. A tymczasem wróćmy tam, gdzie wszystko działa.',
  'lines':['Sprawdzanie ścieżki...','Szukanie strony w repozytorium...','Nie znaleziono zasobu.','Powiadomiono szopa-programistę.','Dostępne opcje powrotu.'],
  'success':'System działa. Problem dotyczy tylko ścieżki.',
  'home':'Strona główna','work':'Zobacz realizacje','contact':'Skontaktuj się ze studiem',
  'bottom':'BŁĄD 404 · NIE ZNALEZIONO ŚCIEŻKI · POWRÓT DOSTĘPNY',
  'metaTitle':'404 — Nie znaleziono strony | Raccoon SEO Studio',
  'metaDescription':'Nie znaleziono strony. Wróć na stronę główną Raccoon SEO Studio lub zobacz nasze realizacje.'},
 'en': {
  'label':'RACCOON SYSTEM / ERROR REPORT','status':'SYSTEM ONLINE',
  'title':'This page escaped the repository.',
  'description':"We're already checking the commits for suspects. Meanwhile, let's get you back to where everything works.",
  'lines':['Checking requested route...','Searching repository...','Resource not found.','Developer raccoon notified.','Recovery options available.'],
  'success':'System operational. Only the route is missing.',
  'home':'Back to homepage','work':'Explore our work','contact':'Contact the studio',
  'bottom':'ERROR 404 · ROUTE NOT FOUND · RECOVERY AVAILABLE',
  'metaTitle':'404 — Page Not Found | Raccoon SEO Studio',
  'metaDescription':'Page not found. Return to Raccoon SEO Studio or explore our latest projects.'}
}

def build():
 for lang,c in COPY.items():
  home='/' if lang=='uk' else f'/{lang}/'
  source=(ROOT/('index.html' if lang=='uk' else f'{lang}/index.html')).read_text()
  header=re.search(r'<header\b.*?</header>',source,re.S)[0]
  # Point language choices to actual localized error documents, never invented translations.
  def options(m):
   s=m[0]
   for l,url in [('uk','/404.html'),('pl','/pl/404.html'),('en','/en/404.html')]:
    s=re.sub(r'href="[^"]+"( class="language-link" lang="'+l+r'")',lambda x:f'href="{url}"'+x[1],s)
   return s
  header=re.sub(r'<div class="language-switch">.*?</div></div>',options,header,flags=re.S)
  footer=re.search(r'<footer\b.*?</footer>',source,re.S)[0].replace('href="#', f'href="{home}#')
  modal=source[source.index('  <div class="js-backdrop'):source.index('  <!-- JS -->')]
  skip=re.search(r'<a[^>]*class="skip-link".*?</a>',source,re.S)[0]
  work=home+'clients.html' if lang!='en' else '/en/#work'
  lines='\n'.join(f'<li style="--line-delay: {700+i*350}ms"><span aria-hidden="true">›</span> {escape(t)}</li>' for i,t in enumerate(c['lines']))
  page=f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex, follow" />
  <title>{escape(c['metaTitle'])}</title>
  <meta name="description" content="{escape(c['metaDescription'],quote=True)}" />
  <link rel="stylesheet" href="/styles/style.css" />
  <link rel="stylesheet" href="/styles/error-404.css" />
  <link rel="icon" href="/images/brand/raccoon-icon-32.png" type="image/png" sizes="32x32" />
  <link rel="icon" href="/images/brand/raccoon-icon-64.png" type="image/png" sizes="64x64" />
  <link rel="shortcut icon" href="/images/brand/raccoon-favicon.ico" />
  <link rel="apple-touch-icon" href="/images/brand/raccoon-icon-180.png" sizes="180x180" />
</head>
<body class="studio-v5 error-page">
{skip}
{header}
<main id="main-content" class="debug-main" tabindex="-1">
  <section class="debug-panel container" aria-labelledby="error-title">
    <div class="debug-topbar"><p class="debug-label"><span class="debug-dot" aria-hidden="true"></span>{c['label']}</p><p class="debug-online"><span aria-hidden="true">&gt;_</span> {c['status']}</p></div>
    <div class="debug-scene">
      <div class="debug-copy"><p class="debug-code" aria-hidden="true">404<span class="debug-code-dot">.</span></p><h1 id="error-title"><span class="visually-hidden">404 — </span>{escape(c['title'])}</h1><p class="debug-description">{escape(c['description'])}</p></div>
      <div class="debug-visual">
        <div class="debug-mascot"><span class="debug-bracket debug-bracket-start" aria-hidden="true"></span><img src="/images/brand/raccoon-logo.webp" width="463" height="512" alt="Raccoon SEO Studio" fetchpriority="high" decoding="async" /><span class="debug-bracket debug-bracket-end" aria-hidden="true"></span><span class="debug-coordinate" aria-hidden="true">RACCOON / DEV.01</span></div>
        <div class="debug-terminal" aria-hidden="true"><div class="debug-terminal-title"><span class="debug-terminal-dots">● ● ●</span><span>raccoon@studio:~$ diagnose /404</span></div><ol class="debug-lines">{lines}</ol><p class="debug-success"><span>✓</span> {escape(c['success'])}</p></div>
      </div>
      <div class="debug-actions"><a class="debug-primary" href="{home}">{c['home']} <span aria-hidden="true">↗</span></a><a class="debug-secondary" href="{work}">{c['work']}</a><a class="debug-contact" href="{home}#contacts">{c['contact']} <span aria-hidden="true">→</span></a></div>
    </div>
    <p class="debug-bottom">{c['bottom']}</p>
  </section>
</main>
{footer}
{modal}
<script src="/script/script.js" defer></script>
</body>
</html>
'''
  (ROOT/('404.html' if lang=='uk' else f'{lang}/404.html')).write_text(inject_gtm(page))

if __name__=='__main__':
 build()
 print('Built UA/PL/EN 404 pages from existing localized header, footer and modal.')
