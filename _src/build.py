# -*- coding: utf-8 -*-
"""Generator dema EXEVER v5. Uruchom: python _src/build.py (z katalogu exever)."""
import os, json, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://impulseo-pl.github.io/exever/'
IMG = os.path.join(ROOT, 'img')
TEL1, TEL1H = '601 681 185', '+48601681185'
TEL2, TEL2H = '500 629 172', '+48500629172'
MAIL = 'biuro@exever.pl'

# ---------- obrazy ----------
def variants(name):
    out = []
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.append((int(m.group(1)), f, w, h))
    if not out:
        raise SystemExit('brak obrazu ' + name)
    return sorted(out)

def pic(p, name, alt, sizes='100vw', lazy=True, cls='', high=False):
    v = variants(name)
    big = v[-1]
    mid = [x for x in v if x[0] >= 1000] or [big]
    src = mid[0]
    srcset = ', '.join(f'{p}img/{f} {w}w' for _, f, w, h in v)
    a = f'<img src="{p}img/{src[1]}" srcset="{srcset}" sizes="{sizes}" width="{src[2]}" height="{src[3]}" alt="{alt}"'
    if lazy: a += ' loading="lazy" decoding="async"'
    if high: a += ' fetchpriority="high"'
    if cls: a += f' class="{cls}"'
    return a + '>'

def full(name):
    return variants(name)[-1][1]

# ---------- wspólne ----------
NAV = [('domy-szkieletowe/', 'Domy szkieletowe'), ('instalacje/', 'Instalacje'),
       ('realizacje/', 'Realizacje'), ('o-firmie/', 'O firmie'), ('kontakt/', 'Kontakt')]

ORG = {
    "@type": "HomeAndConstructionBusiness",
    "@id": BASE + "#firma",
    "name": "EXEVER sp. z o.o.",
    "alternateName": "EXEVER",
    "description": "Domy szkieletowe z drewna od projektu do odbioru oraz instalacje elektryczne, sanitarne, grzewcze i teletechniczne. Ustka i Koszalin, od 2010 roku.",
    "url": BASE,
    "logo": BASE + "img/sygnet.png",
    "image": BASE + "img/og.jpg",
    "telephone": TEL1H,
    "email": MAIL,
    "foundingDate": "2010-02-23",
    "vatID": "PL5862250418",
    "identifier": [{"@type": "PropertyValue", "propertyID": "KRS", "value": "0000349698"},
                   {"@type": "PropertyValue", "propertyID": "REGON", "value": "220961999"}],
    "address": {"@type": "PostalAddress", "streetAddress": "ul. Grunwaldzka 18", "postalCode": "76-270",
                "addressLocality": "Ustka", "addressRegion": "pomorskie", "addressCountry": "PL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 54.5804384, "longitude": 16.8703415},
    "department": {"@type": "HomeAndConstructionBusiness", "name": "EXEVER – oddział Koszalin", "telephone": TEL1H,
                   "address": {"@type": "PostalAddress", "streetAddress": "ul. Przemysłowa 6c",
                               "addressLocality": "Koszalin", "addressRegion": "zachodniopomorskie", "addressCountry": "PL"}},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=EXEVER+Grunwaldzka+18+Ustka",
    "sameAs": ["https://www.oferteo.pl/exever-spolka-z-ograniczona-odpowiedzialnoscia/firma/4053523"],
    "contactPoint": [{"@type": "ContactPoint", "telephone": TEL1H, "email": MAIL, "contactType": "customer service",
                      "areaServed": "PL", "availableLanguage": "pl"},
                     {"@type": "ContactPoint", "telephone": TEL2H, "contactType": "sales", "areaServed": "PL", "availableLanguage": "pl"}],
    "knowsAbout": ["domy szkieletowe", "domy kanadyjskie", "konstrukcje drewniane", "instalacje elektryczne",
                   "instalacje odgromowe", "fotowoltaika", "instalacje wodno-kanalizacyjne", "instalacje grzewcze",
                   "kotłownie gazowe", "kotłownie na pellet", "pompy ciepła", "instalacje teletechniczne", "automatyka budynkowa"],
    "areaServed": [{"@type": "Country", "name": "Polska"},
                   {"@type": "AdministrativeArea", "name": "województwo pomorskie"},
                   {"@type": "AdministrativeArea", "name": "województwo zachodniopomorskie"}],
    "employee": [{"@type": "Person", "name": "Krzysztof Kowalski", "jobTitle": "Prezes zarządu, project manager"},
                 {"@type": "Person", "name": "Damian Michalik", "jobTitle": "Project manager"}],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Usługi", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": BASE + u}} for n, u in [
            ("Domy szkieletowe z drewna pod klucz", "domy-szkieletowe/"), ("Instalacje elektryczne", "instalacje/#elektryczne"),
            ("Instalacje fotowoltaiczne", "instalacje/#elektryczne"), ("Instalacje sanitarne i grzewcze", "instalacje/#sanitarne"),
            ("Kotłownie gazowe i na pellet", "instalacje/#sanitarne"), ("Pompy ciepła", "instalacje/#sanitarne"),
            ("Instalacje teletechniczne i monitoring", "instalacje/#teletechnika"), ("Automatyka budynkowa", "instalacje/#teletechnika")]]}
}
SITE = {"@type": "WebSite", "@id": BASE + "#witryna", "url": BASE, "name": "EXEVER", "alternateName": "EXEVER sp. z o.o.",
        "inLanguage": "pl-PL", "publisher": {"@id": BASE + "#firma"}}
ORG_REF = {"@id": BASE + "#firma"}

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "@id": BASE + items[-1][0] + "#okruszki", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (u, n) in enumerate(items)]}

TODAY = '2026-09-28'
_CSS = None
def css(p):
    """Cały CSS wklejony do <head> (zminifikowany) – zero blokującego żądania, ścieżki fontów względem strony."""
    global _CSS
    if _CSS is None:
        c = open(os.path.join(ROOT, 'assets', 'styles.css'), encoding='utf-8').read()
        c = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
        c = re.sub(r'\s+', ' ', c)
        c = re.sub(r'\s*([{};,>])\s*', r'\1', c).replace(';}', '}')
        _CSS = c.strip()
    return _CSS.replace('url(../fonts/', f'url({p}fonts/')

def head(p, path, title, desc, og='og.jpg', ogalt='Dom szkieletowy EXEVER z elewacją z desek', ld=None, preload=None,
         ptype='WebPage', name=None, img=None):
    graph = [ORG, SITE] + [x for x in (ld or []) if x is not ORG]
    page = {"@type": ptype, "@id": BASE + path + "#strona", "url": BASE + path, "name": title, "description": desc,
            "inLanguage": "pl-PL", "isPartOf": {"@id": BASE + "#witryna"}, "about": {"@id": BASE + "#firma"},
            "dateModified": TODAY,
            "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "img/" + (full(img) if img else og)}}
    if path:
        page["breadcrumb"] = {"@id": BASE + path + "#okruszki"}
    graph.insert(0, page)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(',', ':'))
    pre = ''
    if preload:
        v = variants(preload[0])
        pre = (f'<link rel="preload" as="image" href="{p}img/{[x for x in v if x[0]>=1000][0][1]}" '
               f'imagesrcset="{", ".join(f"{p}img/{f} {w}w" for _, f, w, h in v)}" imagesizes="{preload[1]}" fetchpriority="high">\n')
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- DEMO: przy wdrożeniu usunąć noindex i podmienić adresy na domenę klienta -->
<meta name="robots" content="noindex, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{BASE}{path}">
<link rel="alternate" hreflang="pl" href="{BASE}{path}">
<link rel="alternate" hreflang="x-default" href="{BASE}{path}">
<meta name="theme-color" content="#ffffff">
<meta name="color-scheme" content="light">
<meta name="format-detection" content="telephone=no">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="geo.region" content="PL-22">
<meta name="geo.placename" content="Ustka">
<meta name="geo.position" content="54.5804384;16.8703415">
<meta name="ICBM" content="54.5804384, 16.8703415">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="EXEVER">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}img/{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogalt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}img/{og}">
<meta name="twitter:image:alt" content="{ogalt}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="sitemap" type="application/xml" href="{p}sitemap.xml">
<link rel="preload" href="{p}fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}fonts/source-sans.woff2" as="font" type="font/woff2" crossorigin>
{pre}<script>document.documentElement.className='js'</script>
<style>{css(p)}</style>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
'''

def header(p, cur):
    links = '\n'.join(
        f'      <a href="{p}{u}"{" aria-current=\"page\"" if u == cur else ""}>{n}</a>' for u, n in NAV)
    return f'''<div class="topbar">
  <div class="wrap">
    <div><span>ul. Grunwaldzka 18, Ustka</span><span>oddział: ul. Przemysłowa 6c, Koszalin</span></div>
    <div><span><a href="mailto:{MAIL}">{MAIL}</a></span><span><a href="tel:{TEL2H}">{TEL2}</a></span></div>
  </div>
</div>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{p or './'}" aria-label="EXEVER – strona główna"><img src="{p}img/logo.png" width="535" height="120" alt="EXEVER"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav class="menu" id="menu" aria-label="Menu główne">
{links}
      <a class="head-tel" href="tel:{TEL1H}">{TEL1}</a>
    </nav>
  </div>
</header>
<main id="tresc">
'''

def footer(p):
    return f'''</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="{p}img/logo-biale.png" width="535" height="120" alt="EXEVER" loading="lazy">
        <p>Domy szkieletowe z drewna i instalacje w budynkach. Ustka i Koszalin, od 2010 roku.</p>
      </div>
      <div>
        <h3>Oferta</h3>
        <ul>
          <li><a href="{p}domy-szkieletowe/">Domy szkieletowe</a></li>
          <li><a href="{p}instalacje/#elektryczne">Instalacje elektryczne</a></li>
          <li><a href="{p}instalacje/#sanitarne">Instalacje sanitarne i grzewcze</a></li>
          <li><a href="{p}instalacje/#teletechnika">Teletechnika i automatyka</a></li>
          <li><a href="{p}realizacje/">Realizacje</a></li>
        </ul>
      </div>
      <div>
        <h3>Firma</h3>
        <ul>
          <li><a href="{p}o-firmie/">O firmie</a></li>
          <li><a href="{p}kontakt/">Kontakt</a></li>
          <li><a href="{p}polityka-prywatnosci/">Polityka prywatności</a></li>
          <li><a href="{p}zrodla-zdjec.html">Źródła zdjęć</a></li>
        </ul>
      </div>
      <div>
        <h3>Kontakt</h3>
        <p><a href="tel:{TEL1H}">{TEL1}</a> · <a href="tel:{TEL2H}">{TEL2}</a><br><a href="mailto:{MAIL}">{MAIL}</a><br>ul. Grunwaldzka 18, 76-270 Ustka<br>ul. Przemysłowa 6c, Koszalin</p>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 EXEVER sp. z o.o. · NIP 586 225 04 18 · REGON 220961999 · KRS 0000349698</span>
      <span>Strona: Impulseo</span>
    </div>
  </div>
</footer>

<nav class="mbar" aria-label="Szybki kontakt">
  <a href="tel:{TEL1H}">Zadzwoń</a>
  <a href="{p}kontakt/">Zapytaj o wycenę</a>
</nav>

<script src="{p}assets/app.js" defer></script>
</body>
</html>
'''

def crumbs(p, name):
    return f'<nav class="crumbs" aria-label="Jesteś tutaj"><ol><li><a href="{p}">EXEVER</a></li><li aria-current="page">{name}</li></ol></nav>'

def phero(p, name, h1, lead, actions='', img=None, alt=''):
    """Nagłówek podstrony: biały, tekst; pod nim zdjęcie na całą szerokość (LCP)."""
    a = f'\n    <div class="actions">{actions}</div>' if actions else ''
    fig = f'\n<div class="wide-img">{pic(p, img, alt, "100vw", lazy=False, high=True)}</div>' if img else ''
    return f'''<section class="phead{'' if img else ' line'}">
  <div class="wrap">
    {crumbs(p, name)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>{a}
  </div>
</section>{fig}'''

def cta(p, h='Masz działkę albo projekt? Porozmawiajmy.', t='Pierwsza konsultacja w sprawie domu jest bezpłatna. Doradzimy, zanim cokolwiek podpiszesz.', temat='dom'):
    return f'''<section class="cta">
  <div class="wrap">
    <div data-in="l">
      <h2>{h}</h2>
      <p>{t}</p>
    </div>
    <div class="cta-side" data-in="r">
      <a class="cta-tel" href="tel:{TEL1H}">{TEL1}</a>
      <a class="cta-tel" href="tel:{TEL2H}">{TEL2}</a>
      <p><a href="mailto:{MAIL}">{MAIL}</a> · Ustka, ul. Grunwaldzka 18</p>
      <div class="actions"><a class="btn btn-main" href="{p}kontakt/?temat={temat}">Napisz zapytanie</a></div>
    </div>
  </div>
</section>
'''

# ---------- treści współdzielone ----------
STEPS_A = [('Bezpłatna konsultacja', 'Poznajemy Twoje potrzeby i oczekiwania, doradzamy najlepsze rozwiązania.'),
           ('Dobór lub stworzenie projektu', 'Pomagamy wybrać gotowy projekt albo projektujemy dom od podstaw – dopasowany do działki i stylu życia.'),
           ('Wycena i zakres prac', 'Przedstawiamy szczegółową ofertę z podziałem na etapy realizacji.'),
           ('Umowa', 'Podpisujemy przejrzystą umowę, w której jasno określamy terminy, zakres i koszty.'),
           ('Formalności w urzędzie', 'Pomagamy uzyskać pozwolenie na budowę albo przeprowadzamy procedurę zgłoszenia.')]
STEPS_B = [('Prace przygotowawcze', 'Wyrównujemy teren i wykonujemy fundamenty pod dom szkieletowy.'),
           ('Montaż konstrukcji', 'Wznosimy konstrukcję szkieletową, montujemy dach, okna i drzwi.'),
           ('Instalacje i ocieplenie', 'Wykonujemy wszystkie instalacje i ocieplamy budynek zgodnie z normami.'),
           ('Wykończenie wnętrz i elewacji', 'Prace wykończeniowe wewnątrz i na zewnątrz – w standardzie, który wybierzesz.'),
           ('Odbiór i dokumentacja', 'Odbiór techniczny i przekazanie gotowego domu z pełną dokumentacją.')]

def steps():
    def col(title, items, start, side):
        lis = '\n'.join(f'          <li><span>{start+i}</span><div><b>{a}</b><p>{b}</p></div></li>' for i, (a, b) in enumerate(items))
        return f'      <div data-in="{side}">\n        <h3>{title}</h3>\n        <ol>\n{lis}\n        </ol>\n      </div>'
    return f'''    <div class="steps">
{col('Zanim ruszy budowa', STEPS_A, 1, 'l')}
{col('Budowa i odbiór', STEPS_B, 6, 'r')}
    </div>'''

OFERTEO = 'https://www.oferteo.pl/exever-spolka-z-ograniczona-odpowiedzialnoscia/firma/4053523'
def reviews():
    return f'''    <div class="reviews">
      <figure class="review" data-in="l">
        <blockquote>„Szybko, solidnie, pełna komunikacja. Serwis gwarancyjny i pogwarancyjny.”</blockquote>
        <figcaption>B. · ocena 5/5 w serwisie <a href="{OFERTEO}" rel="noopener">Oferteo.pl</a></figcaption>
      </figure>
      <figure class="review" data-in="r">
        <blockquote>„Szybka, fajna obsługa, bardzo porządny wykonawca.”</blockquote>
        <figcaption>M. Ł. · ocena 5/5 w serwisie <a href="{OFERTEO}" rel="noopener">Oferteo.pl</a></figcaption>
      </figure>
    </div>'''

LAYERS = [
    ('Płyta gipsowo-włóknowa Fermacell', 'Wzmocniona włóknami, dźwiękochłonna i ognioodporna. Można na niej wieszać półki i obrazy.', 32, 70),
    ('Płyta OSB3 lub OSB4', 'Usztywnia ścianę od środka i daje mocne podłoże pod wykończenie.', 21, 41.5),
    ('Folia paroizolacyjna', 'Chroni izolację przed wilgocią z wnętrza domu.', 47, 38),
    ('Szkielet z drewna i wełna mineralna', 'Między elementami konstrukcji 150 mm wełny mineralnej lub skalnej.', 53, 24),
    ('Wiatroizolacja', 'Zatrzymuje wiatr, a jednocześnie pozwala ścianie oddychać.', 77.5, 47),
    ('Elewacja z desek', 'Ściany zewnętrzne obudowane drewnem świerkowym albo tworzywem.', 84.3, 30),
]
def wall(p):
    pins = '\n'.join(f'          <span class="pin" style="left:{x}%;top:{y}%" aria-hidden="true">{i+1}</span>' for i, (_, _, x, y) in enumerate(LAYERS))
    lis = '\n'.join(f'        <li><div><b>{a}</b><span>{b}</span></div></li>' for a, b, _, _ in LAYERS)
    return f'''    <div class="wall" data-wall>
      <figure class="wall-fig" data-in="l">
        <div class="wall-pic">
          {pic(p, 'przekroj', 'Przekrój ściany domu szkieletowego EXEVER: płyty, izolacja, szkielet i elewacja', '(min-width: 961px) 620px, 100vw')}
{pins}
        </div>
      </figure>
      <div data-in="r">
        <ol class="layers">
{lis}
        </ol>
        <p class="src">Rysunek i opis warstw: katalog i opis technologii EXEVER.</p>
      </div>
    </div>'''

SPEC = [('Ściany zewnętrzne', '150 mm wełny mineralnej lub skalnej'), ('Dach i podłoga', 'do 250 mm izolacji'),
        ('Okna', 'potrójne szyby, ograniczone mostki termiczne'), ('Płyty od wewnątrz', 'OSB3 / OSB4 i Fermacell'),
        ('Elewacja', 'deska świerkowa albo tworzywo')]
def specs():
    rows = '\n'.join(f'      <div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in SPEC)
    return f'    <dl class="spec">\n{rows}\n    </dl>'

# galeria: (plik, kategoria, podpis, opis)
GAL = [
    ('dom-narozny', 'domy', 'Dom z elewacją z pionowych desek', 'rolety zewnętrzne, dach z blachy'),
    ('dom-dlugi', 'domy', 'Dom z przeszkleniami od podłogi', 'elewacja z desek pionowych i poziomych'),
    ('elewacja', 'domy', 'Elewacja z desek układanych poziomo', 'okna w grafitowych ramach'),
    ('dom-plac', 'domy', 'Dom szkieletowy z elewacją z desek', 'gotowy do przekazania'),
    ('wnetrze', 'domy', 'Wnętrze gotowego domu', 'drzwi, podłoga, duże przeszklenia'),
    ('szkielet-hala', 'domy', 'Konstrukcja ścian i dachu', 'montaż w hali'),
    ('welna', 'domy', 'Izolacja z wełny mineralnej', 'z przygotowanymi przejściami instalacji'),
    ('osb', 'domy', 'Ściany z płyt OSB', 'przed wykończeniem'),
    ('hala-kurierska', 'instalacje', 'Instalacje elektryczne w hali kurierskiej', 'realizacja EXEVER'),
    ('hala-przenosniki', 'instalacje', 'Hala magazynowa z linią przenośników', 'realizacja EXEVER'),
    ('rozdzielnia', 'instalacje', 'Rozdzielnia elektryczna', 'realizacja EXEVER'),
    ('resort', 'instalacje', 'Instalacje elektryczne w nadmorskim resorcie', 'realizacja EXEVER'),
    ('budynek-wielorodzinny', 'instalacje', 'Instalacje wod-kan w budynku wielorodzinnym', 'Ustka'),
    ('kotlownia', 'instalacje', 'Kotłownia i instalacja grzewcza', 'Ustka'),
    ('kotly', 'instalacje', 'Instalacje wod-kan i grzewcze', 'Ustka'),
]
SIDE3 = ('l', 'f', 'r')  # trzy kolumny: lewa z lewej, środek pojawia się, prawa z prawej
def gallery(p, only=None, skip=()):
    items = []
    for n, k, c, d in GAL:
        if only and k != only: continue
        if n in skip: continue
        items.append(f'''      <a href="{p}img/{full(n)}" data-in="{SIDE3[len(items) % 3]}" data-k="{k}" data-cap="{c} – {d}"><span class="gimg">{pic(p, n, c + ' – ' + d, '(min-width: 961px) 384px, (min-width: 681px) 50vw, 100vw')}</span><span class="gcap">{c}<small>{d}</small></span></a>''')
    return '    <div class="gallery">\n' + '\n'.join(items) + '\n    </div>'

def proj(p, names):
    out = []
    for i, n in enumerate(names):
        _, _, c, d = next(g for g in GAL if g[0] == n)
        out.append(f'      <figure data-in="{SIDE3[i % 3]}">{pic(p, n, c + " – " + d, "(min-width: 961px) 384px, (min-width: 681px) 50vw, 100vw")}<figcaption>{c}<small>{d}</small></figcaption></figure>')
    return '    <div class="proj">\n' + '\n'.join(out) + '\n    </div>'

def sierotki(html):
    # jednoliterowe spójniki i przyimki nie zostają na końcu wiersza (poza <script> i znacznikami)
    parts = re.split(r'(<script.*?</script>|<style>.*?</style>|<title>.*?</title>|<[^>]+>)', html, flags=re.S)
    for i, s in enumerate(parts):
        if s.startswith('<'):
            continue
        parts[i] = re.sub(r'(?<![\w&;])([aiouwzAIOUWZ]) ', r'\1&nbsp;', s)
    return ''.join(parts)

def slide(html):
    """Rzędy tekst/zdjęcie: element po lewej wjeżdża z lewej, po prawej – z prawej (jak na exever.pl/technologia)."""
    out, pos = [], 0
    for m in re.finditer(r'<div class="row( rev)?"[^>]*>', html):
        kids = list(re.finditer(r'<div class="row-(img|txt)">', html[m.end():]))[:2]
        if len(kids) < 2 or m.end() < pos:
            continue
        order = [k.group(1) for k in kids]
        left = 'txt' if m.group(1) else order[0]
        for k in kids:
            a = m.end() + k.start()
            out.append(html[pos:a])
            out.append(f'<div class="row-{k.group(1)}" data-in="{"l" if k.group(1) == left else "r"}">')
            pos = a + len(k.group(0))
    return ''.join(out) + html[pos:]

PAGE_IMGS = {}
def write(path, html):
    html = sierotki(slide(html))
    seen = []
    for m in re.finditer(r'<img [^>]*?srcset="([^"]+)"[^>]*?alt="([^"]*)"', html):
        last = m.group(1).split(',')[-1].strip().split(' ')[0]
        u = BASE + re.sub(r'^(\.\./)+', '', last)
        if m.group(2) and u not in [x[0] for x in seen]:
            seen.append((u, m.group(2)))
    PAGE_IMGS[path] = seen
    fp = os.path.join(ROOT, path, 'index.html') if path else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('zapisano', fp)

# =====================================================================
# STRONA GŁÓWNA
# =====================================================================
def home():
    p = ''
    h = head(p, '', 'Domy szkieletowe i instalacje – EXEVER Ustka, Koszalin',
             'EXEVER sp. z o.o. z Ustki: domy szkieletowe z drewna od projektu do odbioru oraz instalacje elektryczne, sanitarne i grzewcze. Od 2010 roku. Tel. 601 681 185.',
             ld=[], preload=('dom-narozny', '(min-width: 961px) 50vw, 100vw'), img='dom-narozny')
    body = f'''
<section class="hero">
  <div class="hero-txt">
    <h1>Domy szkieletowe z drewna i instalacje w budynkach</h1>
    <p class="lead">Budujemy domy szkieletowe od rozmowy o działce i projekcie, przez formalności w urzędzie, po odbiór techniczny z dokumentacją. Instalacje elektryczne, sanitarne i grzewcze wykonujemy w nich sami – a także w halach i budynkach wielorodzinnych.</p>
    <div class="actions">
      <a class="btn btn-main" href="kontakt/?temat=dom">Zapytaj o dom</a>
      <a class="btn btn-sec" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a>
    </div>
    <p class="hero-note"><b>EXEVER sp. z o.o.</b> – siedziba w Ustce, oddział w Koszalinie, w KRS od 2010 roku. Ocena 5,0 w serwisie Oferteo.pl.</p>
  </div>
  <figure class="hero-img">{pic(p, 'dom-narozny', 'Dom szkieletowy EXEVER z elewacją z pionowych desek świerkowych i roletami', '(min-width: 961px) 50vw, 100vw', lazy=False, high=True)}</figure>
</section>

<section class="sec">
  <div class="wrap">
    <div class="row">
      <div class="row-img" data-in="l">
        {pic(p, 'dom-dlugi', 'Dom szkieletowy EXEVER z przeszkleniami od podłogi i elewacją z desek', '(min-width: 961px) 560px, 100vw')}
      </div>
      <div class="row-txt" data-in="r">
        <h2>Dom szkieletowy pod klucz</h2>
        <p class="lead">Konstrukcja z drewna, wełna mineralna w ścianach, dachu i podłodze, wykończenie w standardzie, który wybierzesz. Całą budowę prowadzi jedna firma.</p>
        <ul class="list">
          <li>gotowy projekt albo projekt od podstaw</li>
          <li>pomoc przy pozwoleniu na budowę albo zgłoszeniu</li>
          <li>fundamenty, konstrukcja, instalacje, ocieplenie, wykończenie</li>
          <li>odbiór techniczny z pełną dokumentacją</li>
        </ul>
        <a class="more" href="domy-szkieletowe/">Więcej o domach szkieletowych</a>
      </div>
    </div>
    <div class="row rev">
      <div class="row-img" data-in="r">
        {pic(p, 'hala-przenosniki', 'Hala magazynowa z linią przenośników – realizacja instalacji EXEVER', '(min-width: 961px) 560px, 100vw')}
      </div>
      <div class="row-txt" data-in="l">
        <h2>Instalacje w domach, halach i budynkach wielorodzinnych</h2>
        <p class="lead">Od instalacji zaczynaliśmy w 2010 roku. Pracujemy dla firm wykonawczych, inwestorów i klientów indywidualnych, na terenie całej Polski.</p>
        <ul class="list">
          <li>instalacje elektryczne, rozdzielnie, oświetlenie, instalacje odgromowe</li>
          <li>instalacje wodno-kanalizacyjne i grzewcze</li>
          <li>kotłownie gazowe i na pellet, pompy ciepła, fotowoltaika</li>
          <li>teletechnika, monitoring, automatyka budynkowa</li>
        </ul>
        <a class="more" href="instalacje/">Pełny zakres instalacji</a>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-stone">
  <div class="wrap">
    <div class="row">
      <div class="row-txt" data-in="l">
        <h2>Instalacje planujemy razem z konstrukcją</h2>
        <p class="lead">Konstrukcję domu składamy pod dachem, w hali. Zanim ściany zostaną zamknięte, prowadzimy w nich przewody i rury – instalacje to nasza pierwsza specjalność, więc nie dokładamy ich na końcu.</p>
{specs()}
        <p style="margin-top:26px"><a class="more" href="domy-szkieletowe/#sciana">Co jest w ścianie – warstwa po warstwie</a></p>
      </div>
      <div class="row-img" data-in="r">
        <div class="pair">
          {pic(p, 'szkielet-hala', 'Konstrukcja szkieletowa ścian i dachu w hali', '(min-width: 961px) 300px, 50vw')}
          {pic(p, 'welna', 'Wełna mineralna ułożona między elementami konstrukcji', '(min-width: 961px) 250px, 50vw')}
        </div>
        <p class="figcap">Konstrukcja w hali i izolacja z wełny mineralnej – zdjęcia z katalogu EXEVER.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head-row">
      <div class="sec-head">
        <h2>Realizacje instalacji</h2>
        <p>Hale, resort, budynek wielorodzinny i kotłownie w Ustce – zdjęcia z naszych budów.</p>
      </div>
      <a class="more" href="realizacje/">Wszystkie realizacje</a>
    </div>
{proj(p, ['hala-kurierska', 'rozdzielnia', 'resort', 'budynek-wielorodzinny', 'kotlownia', 'kotly'])}
  </div>
</section>

<section class="sec sec-stone">
  <div class="wrap">
    <div class="sec-head">
      <h2>Jak wygląda budowa domu z nami</h2>
      <p>Prowadzimy całość, także część papierową. Na każdym etapie wiesz, co się dzieje i co będzie dalej.</p>
    </div>
{steps()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Co piszą klienci</h2>
    </div>
{reviews()}
  </div>
</section>

{cta(p)}'''
    write('', h + header(p, '') + body + footer(p))

# =====================================================================
# DOMY SZKIELETOWE
# =====================================================================
FAQ = [
    ('Czy pomagacie w formalnościach?', 'Tak. Pomagamy uzyskać pozwolenie na budowę albo przeprowadzamy procedurę zgłoszenia – zależnie od tego, czego wymaga Twój dom i działka.'),
    ('Muszę mieć gotowy projekt?', 'Nie. Pomagamy wybrać gotowy projekt albo projektujemy dom od podstaw, dopasowany do działki i stylu życia.'),
    ('Kto robi fundamenty?', 'My. Wyrównujemy teren i wykonujemy fundamenty pod dom szkieletowy – to część budowy, nie osobne zlecenie.'),
    ('Jakie ogrzewanie mogę wybrać?', 'W naszych domach można zastosować różne rodzaje ogrzewania. Instalacje grzewcze, kotłownie i pompy ciepła wykonujemy sami, więc dobierzemy rozwiązanie do domu i Twoich oczekiwań.'),
    ('Ile kosztuje dom?', 'To zależy od projektu, działki i standardu wykończenia. Po konsultacji przygotowujemy szczegółową ofertę z podziałem na etapy – a w umowie zapisujemy terminy, zakres i koszty.'),
    ('Co dostaję przy odbiorze?', 'Po zakończeniu budowy przeprowadzamy odbiór techniczny i przekazujemy dom razem z pełną dokumentacją.'),
]
def domy():
    p = '../'
    path = 'domy-szkieletowe/'
    ld = [crumbs_ld([('', 'EXEVER'), (path, 'Domy szkieletowe')]),
          {"@type": "Service", "@id": BASE + path + "#usluga", "name": "Domy szkieletowe z drewna pod klucz",
           "alternateName": "Domy kanadyjskie", "serviceType": "Budowa domów szkieletowych",
           "description": "Budowa domu szkieletowego od projektu i formalności, przez fundamenty, konstrukcję, instalacje i ocieplenie, po wykończenie i odbiór techniczny z dokumentacją.",
           "provider": ORG_REF, "areaServed": {"@type": "Country", "name": "Polska"}, "url": BASE + path,
           "image": BASE + "img/" + full('dom-dlugi'),
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Zakres budowy", "itemListElement": [
               {"@type": "Offer", "itemOffered": {"@type": "Service", "name": a, "description": b}} for a, b in STEPS_A + STEPS_B]}},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    h = head(p, path, 'Domy szkieletowe z drewna pod klucz – EXEVER Ustka',
             'Domy szkieletowe (kanadyjskie) pod klucz: projekt, formalności, fundamenty, konstrukcja, instalacje i wykończenie. 150 mm wełny w ścianach. EXEVER Ustka.',
             ld=ld, preload=('dom-dlugi', '(min-width: 961px) 600px, 100vw'), img='dom-dlugi')
    faq = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = f'''
{phero(p, 'Domy szkieletowe', 'Domy szkieletowe z drewna – od projektu do odbioru kluczy',
        'Dom szkieletowy, nazywany też kanadyjskim, ma konstrukcję z drewna wypełnioną izolacją. Budujemy go od fundamentów po wykończenie i sami wykonujemy w nim wszystkie instalacje.',
        '<a class="btn btn-main" href="../kontakt/?temat=dom">Zapytaj o dom</a><a class="btn btn-sec" href="#przebieg">Jak przebiega budowa</a>',
        'dom-dlugi', 'Dom szkieletowy EXEVER z przeszkleniami od podłogi')}

<section class="sec">
  <div class="wrap">
    <div class="row">
      <div class="row-txt">
        <h2>Dlaczego drewno</h2>
        <p class="lead">W krajach bogatych w lasy buduje się z drewna od wieków. To materiał mocny i stabilny, a jednocześnie elastyczny – dobrze znosi naprężenia.</p>
        <p>Drewno na elewacji pokryte woskiem, bejcą albo lakierem dobrze pokazuje usłojenie i nadaje domowi ciepły wygląd. Ściany zewnętrzne obudowujemy drewnem świerkowym albo tworzywem – do wyboru.</p>
        <ul class="list">
          <li><b>Konstrukcja dopasowana do projektu</b> – gotowego albo przygotowanego od podstaw</li>
          <li><b>Dokładność montażu</b> – od niej zależy trwałość domu i brak błędów na kolejnych etapach</li>
          <li><b>Wykończenie w wybranym standardzie</b>, wewnątrz i na zewnątrz</li>
        </ul>
      </div>
      <div class="row-img">
        {pic(p, 'elewacja', 'Elewacja z desek układanych poziomo i okna w grafitowych ramach', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Elewacja z desek układanych poziomo.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-stone" id="sciana">
  <div class="wrap">
    <div class="sec-head">
      <h2>Co jest w ścianie</h2>
      <p>O jakości domu szkieletowego decyduje to, czego po wykończeniu nie widać. Najedź na numer albo na warstwę, żeby zobaczyć, gdzie leży.</p>
    </div>
{wall(p)}
{specs()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="row rev">
      <div class="row-img">
        {pic(p, 'wnetrze', 'Wnętrze gotowego domu szkieletowego EXEVER', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Wnętrze gotowego domu.</p>
      </div>
      <div class="row-txt">
        <h2>Ogrzewanie i automatyka od tej samej ekipy</h2>
        <p class="lead">Instalacje elektryczne, sanitarne i grzewcze to nasza pierwsza specjalność. W domu, który budujemy, wykonujemy je sami.</p>
        <ul class="list">
          <li><b>Ogrzewanie do wyboru</b> – kotłownia albo pompa ciepła, razem z instalacją</li>
          <li><b>Automatyka domowa</b> i zdalne sterowanie</li>
          <li><b>Monitoring</b> i instalacje teletechniczne</li>
          <li><b>Fotowoltaika</b>, jeśli chcesz produkować własny prąd</li>
        </ul>
        <div class="actions"><a class="more" href="../instalacje/">Pełny zakres instalacji</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head-row">
      <div class="sec-head"><h2>Nasze domy</h2><p>Od szkieletu w hali po gotową elewację.</p></div>
      <a class="more" href="../realizacje/">Wszystkie realizacje</a>
    </div>
{gallery(p, 'domy', skip=('welna', 'osb'))}
  </div>
</section>

<section class="sec sec-stone" id="przebieg">
  <div class="wrap">
    <div class="sec-head">
      <h2>Przebieg budowy w 10 krokach</h2>
      <p>Od pierwszej rozmowy do przekazania kluczy prowadzi Cię jedna firma.</p>
    </div>
{steps()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Najczęstsze pytania</h2></div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>

{cta(p)}'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# INSTALACJE
# =====================================================================
INST_LD = [
    ('elektryczne', 'Instalacje elektryczne', ['Instalacje elektryczne w domach, halach i budynkach usługowych', 'Rozdzielnie elektryczne', 'Montaż oświetlenia', 'Instalacje odgromowe', 'Instalacje fotowoltaiczne']),
    ('sanitarne', 'Instalacje sanitarne i grzewcze', ['Instalacje wodno-kanalizacyjne', 'Instalacje grzewcze', 'Kotłownie gazowe i na pellet', 'Pompy ciepła', 'Odnawialne źródła energii']),
    ('teletechnika', 'Teletechnika i automatyka', ['Instalacje teletechniczne', 'Systemy monitoringu', 'Automatyka budynkowa', 'Zdalne sterowanie urządzeniami w domu']),
]
def instalacje():
    p = '../'
    path = 'instalacje/'
    ld = [crumbs_ld([('', 'EXEVER'), (path, 'Instalacje')]),
          *[{"@type": "Service", "@id": BASE + path + "#" + i, "name": n, "serviceType": n, "provider": ORG_REF,
            "areaServed": {"@type": "Country", "name": "Polska"}, "url": BASE + path + "#" + i,
            "audience": {"@type": "Audience", "audienceType": "firmy wykonawcze, inwestorzy, klienci indywidualni"},
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": n, "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": x}} for x in xs]}}
            for i, n, xs in INST_LD]]
    h = head(p, path, 'Instalacje elektryczne, sanitarne i grzewcze – EXEVER Ustka',
             'Instalacje elektryczne, fotowoltaika, wod-kan, ogrzewanie, kotłownie gazowe i na pellet, pompy ciepła, teletechnika. Dla firm i domów. EXEVER, od 2010 roku.',
             og='og-instalacje.jpg', ogalt='Hala kurierska – instalacje elektryczne EXEVER', ld=ld, preload=('hala-przenosniki', '(min-width: 961px) 600px, 100vw'), img='hala-przenosniki')
    body = f'''
{phero(p, 'Instalacje', 'Instalacje elektryczne, sanitarne i grzewcze',
        'Od tego zaczęliśmy w 2010 roku. Wykonujemy instalacje w domach, halach i budynkach wielorodzinnych – dla firm wykonawczych, inwestorów i klientów indywidualnych, na terenie całej Polski.',
        f'<a class="btn btn-main" href="../kontakt/?temat=instalacja">Zapytaj o instalację</a><a class="btn btn-sec" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a>',
        'hala-przenosniki', 'Hala magazynowa z linią przenośników – realizacja EXEVER')}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Zakres prac</h2></div>
    <div class="inst">
      <div id="elektryczne">
        <h3>Elektryczne</h3>
        <ul><li>instalacje elektryczne w domach, halach i budynkach usługowych</li><li>rozdzielnie elektryczne</li><li>montaż oświetlenia</li><li>instalacje odgromowe</li><li>instalacje fotowoltaiczne</li></ul>
      </div>
      <div id="sanitarne">
        <h3>Sanitarne i grzewcze</h3>
        <ul><li>instalacje wodno-kanalizacyjne</li><li>instalacje grzewcze</li><li>kotłownie gazowe i na pellet</li><li>pompy ciepła</li><li>odnawialne źródła energii</li></ul>
      </div>
      <div id="teletechnika">
        <h3>Teletechnika i automatyka</h3>
        <ul><li>instalacje teletechniczne</li><li>systemy monitoringu</li><li>automatyka budynkowa</li><li>zdalne sterowanie urządzeniami w domu</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-stone">
  <div class="wrap">
    <div class="row">
      <div class="row-img">
        {pic(p, 'hala-kurierska', 'Hala kurierska – instalacje elektryczne EXEVER', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Instalacje elektryczne w hali kurierskiej.</p>
      </div>
      <div class="row-txt">
        <h2>Hale, resorty, budynki wielorodzinne</h2>
        <p class="lead">Współpracujemy z firmami wykonawczymi i inwestorami. Do każdego zlecenia podchodzimy rzetelnie i w przemyślany sposób.</p>
        <ul class="list">
          <li><b>Hala kurierska</b> – instalacje elektryczne</li>
          <li><b>Hala magazynowa z przenośnikami</b></li>
          <li><b>Nadmorski resort</b> – instalacje elektryczne</li>
          <li><b>Budynek wielorodzinny w Ustce</b> – instalacje wod-kan</li>
        </ul>
      </div>
    </div>
    <div class="row rev">
      <div class="row-img">
        {pic(p, 'kotly', 'Kotły i instalacja grzewcza wykonana przez EXEVER w Ustce', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Instalacje wod-kan i grzewcze, Ustka.</p>
      </div>
      <div class="row-txt">
        <h2>Nowa instalacja albo modernizacja kotłowni</h2>
        <p class="lead">Instalacja w nowym domu, wymiana kotłowni, fotowoltaika albo pompa ciepła. Zadzwoń albo opisz sprawę w formularzu – oddzwonimy i ustalimy szczegóły.</p>
        <p>Klienci piszą o nas: „Szybko, solidnie, pełna komunikacja. Serwis gwarancyjny i pogwarancyjny.” <a href="{OFERTEO}" rel="noopener">(Oferteo.pl)</a></p>
        <div class="actions"><a class="btn btn-main" href="../kontakt/?temat=instalacja">Zapytaj o instalację</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head-row">
      <div class="sec-head"><h2>Realizacje instalacji</h2></div>
      <a class="more" href="../realizacje/">Wszystkie realizacje</a>
    </div>
{gallery(p, 'instalacje', skip=('hala-przenosniki',))}
  </div>
</section>

{cta(p, 'Potrzebujesz wykonawcy instalacji?', 'Zadzwoń albo napisz – oddzwonimy i ustalimy szczegóły.', 'instalacja')}'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# REALIZACJE
# =====================================================================
def realizacje():
    p = '../'
    path = 'realizacje/'
    h = head(p, path, 'Realizacje – domy szkieletowe i instalacje | EXEVER',
             'Zdjęcia domów szkieletowych EXEVER i realizacji instalacji: hala kurierska, nadmorski resort, kotłownie i budynki wielorodzinne w Ustce.',
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'Realizacje')]),
                 {"@type": "ImageGallery", "@id": BASE + path + "#galeria", "name": "Realizacje EXEVER", "url": BASE + path,
                  "author": ORG_REF, "numberOfItems": len(GAL),
                  "image": [{"@type": "ImageObject", "contentUrl": BASE + "img/" + full(n), "name": c, "caption": f"{c} – {d}",
                             "creditText": "EXEVER sp. z o.o.", "copyrightHolder": ORG_REF, "creator": ORG_REF}
                            for n, k, c, d in GAL]}],
             ptype='CollectionPage', img='dom-dlugi')
    body = f'''
{phero(p, 'Realizacje', 'Realizacje – domy szkieletowe i instalacje',
        'Domy szkieletowe – od konstrukcji w hali po gotową elewację – i instalacje, które wykonaliśmy w halach, resortach i budynkach wielorodzinnych.')}
<section class="sec" style="padding-top:48px">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Pokaż">
      <button type="button" data-f="all" aria-pressed="true">Wszystkie</button>
      <button type="button" data-f="domy" aria-pressed="false">Domy szkieletowe</button>
      <button type="button" data-f="instalacje" aria-pressed="false">Instalacje</button>
    </div>
{gallery(p)}
  </div>
</section>
{cta(p)}'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# O FIRMIE
# =====================================================================
def ofirmie():
    p = '../'
    path = 'o-firmie/'
    h = head(p, path, 'O firmie – EXEVER sp. z o.o., Ustka',
             'EXEVER sp. z o.o. z Ustki, w KRS od 2010 roku: instalacje elektryczne, sanitarne i grzewcze oraz domy szkieletowe z drewna. Oddział w Koszalinie.',
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'O firmie')])], ptype='AboutPage', img='elewacja', preload=('elewacja', '(min-width: 961px) 600px, 100vw'))
    body = f'''
{phero(p, 'O firmie', 'EXEVER – firma z Ustki, od 2010 roku',
        'Zaczynaliśmy od instalacji elektrycznych i sanitarnych. Dziś budujemy też całe domy w konstrukcji szkieletowej – i instalacje wykonujemy w nich sami.',
        img='elewacja', alt='Elewacja z desek domu szkieletowego EXEVER')}

<section class="sec">
  <div class="wrap">
    <div class="row">
      <div class="row-txt">
        <h2>Jedna firma zamiast kilku ekip</h2>
        <p class="lead">Spółkę zarejestrowaliśmy w lutym 2010 roku. Od początku wykonujemy instalacje – dla firm wykonawczych i dla klientów indywidualnych.</p>
        <p>Budując dom, prowadzimy wszystko: projekt, formalności, fundamenty, konstrukcję, instalacje, ocieplenie i wykończenie. Nie musisz koordynować kilku wykonawców ani pilnować, żeby elektryk zdążył przed zamknięciem ścian.</p>
        <p>Siedzibę mamy w Ustce, oddział w Koszalinie.</p>
      </div>
      <div class="row-img">
        {pic(p, 'szkielet-hala', 'Konstrukcja szkieletowa domu EXEVER w hali', '(min-width: 961px) 564px, 100vw')}
      </div>
    </div>
  </div>
</section>

<section class="sec sec-stone">
  <div class="wrap">
    <div class="row" style="align-items:start">
      <div>
        <h2 style="margin-bottom:28px">Z kim rozmawiasz</h2>
        <div class="people">
          <div><b>Krzysztof Kowalski</b><span>Prezes zarządu, project manager</span></div>
          <div><b>Damian Michalik</b><span>Project manager</span></div>
        </div>
        <p style="margin-top:24px">Telefon: <a href="tel:{TEL1H}">{TEL1}</a> · <a href="tel:{TEL2H}">{TEL2}</a><br>E-mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
      </div>
      <div>
        <h2 style="margin-bottom:28px">Dane firmy</h2>
        <table class="facts">
          <tr><th scope="row">Nazwa</th><td>EXEVER sp. z o.o.</td></tr>
          <tr><th scope="row">Siedziba</th><td>ul. Grunwaldzka 18, 76-270 Ustka</td></tr>
          <tr><th scope="row">Oddział</th><td>ul. Przemysłowa 6c, Koszalin</td></tr>
          <tr><th scope="row">W rejestrze KRS od</th><td>23 lutego 2010</td></tr>
          <tr><th scope="row">KRS</th><td>0000349698, Sąd Rejonowy dla m. Gdańska, VIII Wydział Gospodarczy KRS</td></tr>
          <tr><th scope="row">NIP</th><td>586 225 04 18</td></tr>
          <tr><th scope="row">REGON</th><td>220961999</td></tr>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Opinie klientów</h2><p>Ocena 5,0 na 5 w serwisie Oferteo.pl.</p></div>
{reviews()}
  </div>
</section>
{cta(p)}'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# KONTAKT
# =====================================================================
def kontakt():
    p = '../'
    path = 'kontakt/'
    h = head(p, path, 'Kontakt – EXEVER Ustka i Koszalin, tel. 601 681 185',
             'Kontakt z EXEVER: tel. 601 681 185 lub 500 629 172, biuro@exever.pl. Siedziba ul. Grunwaldzka 18, 76-270 Ustka, oddział ul. Przemysłowa 6c, Koszalin.',
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'Kontakt')])], ptype='ContactPage')
    body = f'''
{phero(p, 'Kontakt', 'Kontakt',
        'Zadzwoń albo napisz, czego potrzebujesz. Pierwsza konsultacja w sprawie domu jest bezpłatna.')}
<section class="sec" style="padding-top:64px">
  <div class="wrap contact">
    <div>
      <h2 class="vh">Dane kontaktowe</h2>
      <a class="tel-big" href="tel:{TEL1H}">{TEL1}</a>
      <a class="tel-big" href="tel:{TEL2H}" style="margin-top:6px">{TEL2}</a>
      <p style="margin:14px 0 30px;font-size:19px"><a href="mailto:{MAIL}">{MAIL}</a></p>
      <div class="c-block c-grid">
        <div><h3>Siedziba</h3><p>ul. Grunwaldzka 18<br>76-270 Ustka</p></div>
        <div><h3>Oddział</h3><p>ul. Przemysłowa 6c<br>Koszalin</p></div>
      </div>
      <div class="c-block">
        <h3>Project managerowie</h3>
        <p>Krzysztof Kowalski · Damian Michalik</p>
      </div>
      <div class="c-block">
        <h3>Dane firmy</h3>
        <p>EXEVER sp. z o.o. · NIP 586 225 04 18 · REGON 220961999 · KRS 0000349698</p>
      </div>
      <div class="map">
        <iframe title="Mapa – EXEVER, ul. Grunwaldzka 18, Ustka" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=16.8553%2C54.5745%2C16.8853%2C54.5864&amp;layer=mapnik&amp;marker=54.5804384%2C16.8703415"></iframe>
        <a href="https://www.google.com/maps/search/?api=1&amp;query=EXEVER+Grunwaldzka+18+Ustka" rel="noopener">Otwórz w Mapach Google</a>
      </div>
    </div>
    <form class="form" id="quote" novalidate>
      <h2>Zapytanie</h2>
      <p>Odpowiemy telefonicznie albo mailowo.</p>
      <div class="row2">
        <div class="field"><label for="imie">Imię i nazwisko</label><input type="text" id="imie" name="imie" autocomplete="name"></div>
        <div class="field"><label for="tel">Telefon</label><input type="tel" id="tel" name="tel" autocomplete="tel"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="email">E-mail (opcjonalnie)</label><input type="email" id="email" name="email" autocomplete="email"></div>
        <div class="field"><label for="miejsce">Miejscowość budowy</label><input type="text" id="miejsce" name="miejsce"></div>
      </div>
      <fieldset class="field">
        <legend>Czego dotyczy zapytanie?</legend>
        <div class="opts">
          <label><input type="radio" name="temat" value="dom"> Dom szkieletowy</label>
          <label><input type="radio" name="temat" value="instalacja"> Instalacja elektryczna</label>
          <label><input type="radio" name="temat" value="ogrzewanie"> Ogrzewanie, kotłownia, OZE</label>
          <label><input type="radio" name="temat" value="firma"> Zlecenie dla firmy</label>
        </div>
      </fieldset>
      <div class="field"><label for="wiad">Kilka słów o planach</label><textarea id="wiad" name="wiad" placeholder="np. mam działkę pod Słupskiem, szukam domu ok. 100 m²"></textarea></div>
      <label class="consent"><input type="checkbox" name="zgoda"> <span>Zgadzam się na kontakt w sprawie zapytania. Zasady w <a href="../polityka-prywatnosci/">polityce prywatności</a>.</span></label>
      <button class="btn btn-main" type="submit">Wyślij zapytanie</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# POLITYKA
# =====================================================================
def polityka():
    p = '../'
    path = 'polityka-prywatnosci/'
    h = head(p, path, 'Polityka prywatności | EXEVER', 'Zasady przetwarzania danych osobowych przez EXEVER sp. z o.o. z Ustki: administrator, cel, czas przechowywania, Twoje prawa i pliki cookies.',
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'Polityka prywatności')])])
    body = f'''
<section class="sec" style="padding-top:56px">
  <div class="wrap doc">
    {crumbs(p, 'Polityka prywatności')}
    <h1>Polityka prywatności</h1>
    <h2>Administrator danych</h2>
    <p>Administratorem danych osobowych jest EXEVER sp. z o.o., ul. Grunwaldzka 18, 76-270 Ustka, NIP 586 225 04 18, KRS 0000349698, tel. {TEL1}, e-mail: {MAIL}.</p>
    <h2>Jakie dane i po co</h2>
    <p><b>Zapytanie z formularza.</b> Imię i nazwisko, telefon, e-mail (jeśli go podasz), miejscowość i treść wiadomości. Przetwarzamy je, żeby odpowiedzieć na zapytanie i przygotować ofertę (art. 6 ust. 1 lit. b RODO).</p>
    <h2>Jak długo</h2>
    <p>Dane z zapytania przechowujemy przez czas potrzebny na przygotowanie oferty i realizację umowy, a potem przez okres wymagany przepisami.</p>
    <h2>Twoje prawa</h2>
    <p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia oraz wniesienia sprzeciwu. Możesz też złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych.</p>
    <h2>Pliki cookies</h2>
    <p>Strona nie używa plików cookies do celów reklamowych ani analitycznych. Mapa na stronie kontaktowej pochodzi z serwisu OpenStreetMap.</p>
  </div>
</section>'''
    write(path, h + header(p, path) + body + footer(p))

# =====================================================================
# 404, sitemap, źródła
# =====================================================================
def extras():
    b = '/exever/'
    html = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nie ma takiej strony | EXEVER</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#1a1a18">
<link rel="icon" href="{b}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{b}assets/styles.css">
</head>
<body>
<header class="site-head"><div class="wrap head-in"><a class="brand" href="{b}" aria-label="EXEVER – strona główna"><img src="{b}img/logo.png" width="535" height="120" alt="EXEVER"></a></div></header>
<main class="sec"><div class="wrap doc">
<h1>Nie ma takiej strony</h1>
<p style="margin-top:18px">Adres mógł się zmienić. Zacznij od strony głównej albo zadzwoń: <a href="tel:{TEL1H}">{TEL1}</a>.</p>
<div class="actions"><a class="btn btn-main" href="{b}">Strona główna</a><a class="btn btn-sec" href="{b}kontakt/">Kontakt</a></div>
</div></main>
</body></html>
'''
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n').write(html)
    urls = ['', 'domy-szkieletowe/', 'instalacje/', 'realizacje/', 'o-firmie/', 'kontakt/', 'polityka-prywatnosci/']
    def ent(u):
        imgs = ''.join(f'\n    <image:image><image:loc>{i}</image:loc></image:image>' for i, _ in PAGE_IMGS.get(u, []))
        return f'  <url>\n    <loc>{BASE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>{imgs}\n  </url>\n'
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + ''.join(ent(u) for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
        f'User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: {BASE}sitemap.xml\n')
    json.dump({"name": "EXEVER – domy szkieletowe i instalacje", "short_name": "EXEVER", "lang": "pl", "start_url": "./",
               "icons": [{"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                         {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
               "theme_color": "#ffffff", "background_color": "#ffffff", "display": "browser"},
              open(os.path.join(ROOT, 'site.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False)
    llms = f'''# EXEVER sp. z o.o.

> Firma z Ustki (oddział w Koszalinie), w KRS od 2010 roku. Buduje domy szkieletowe z drewna od projektu do odbioru i wykonuje instalacje elektryczne, sanitarne, grzewcze i teletechniczne w domach, halach i budynkach wielorodzinnych.

Telefon: {TEL1}, {TEL2} · E-mail: {MAIL} · ul. Grunwaldzka 18, 76-270 Ustka · NIP 586 225 04 18 · KRS 0000349698

## Strony

- [Domy szkieletowe]({BASE}domy-szkieletowe/): technologia ściany, przebieg budowy w 10 krokach, pytania i odpowiedzi
- [Instalacje]({BASE}instalacje/): elektryczne, odgromowe, fotowoltaika, wod-kan, grzewcze, kotłownie, pompy ciepła, teletechnika
- [Realizacje]({BASE}realizacje/): zdjęcia domów i realizacji instalacji
- [O firmie]({BASE}o-firmie/): historia, osoby, dane rejestrowe
- [Kontakt]({BASE}kontakt/): telefony, adresy, formularz zapytania
'''
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8', newline='\n').write(llms)
    KAT = 'https://www.exever.pl/wp-content/uploads/2025/07/Exever-katalog-proof_250625_105735_250630_203544-'
    OF = 'https://static.oferteo.pl/images/portfolio/4053523/orig/'
    src = {
        'dom-narozny': KAT + '9-1.jpg', 'dom-dlugi': KAT + '5-1.jpg', 'elewacja': KAT + '3-1.jpg', 'dom-plac': KAT + '2.jpg',
        'wnetrze': KAT + '8.jpg', 'szkielet-hala': KAT + '7-1.jpg', 'welna': KAT + '4.jpg', 'osb': KAT + '5-1.jpg',
        'przekroj': KAT + '6.png',
        'hala-kurierska': OF + '1751374470094-crop-img-20230119-155049.jpg', 'hala-przenosniki': OF + '1751374523746-crop-img-20230119-154802.jpg',
        'rozdzielnia': OF + '1751374495257-crop-img-20220604-125201.jpg', 'resort': OF + '1751374663598-crop-img-20210518-161256.jpg',
        'budynek-wielorodzinny': OF + '1751374545072-crop-img-20230718-102816.jpg', 'kotlownia': OF + '1752756190691-crop-1000032534.jpg',
        'kotly': OF + '1752756188090-crop-1000032533.jpg',
    }
    lis = ''.join(f'<li><img src="img/{variants(n)[0][1]}" width="140" height="95" alt="" loading="lazy"><div><b>{n}</b><br>'
                  f'{"katalog EXEVER na exever.pl (przycięte, bez filtrów)" if "exever.pl" in u else "galeria realizacji EXEVER w serwisie Oferteo.pl"}<br><a href="{u}">{u}</a></div></li>'
                  for n, u in src.items())
    html = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Źródła zdjęć | EXEVER</title><meta name="robots" content="noindex, follow"><link rel="icon" href="favicon.svg" type="image/svg+xml"><style>body{{font:15px/1.5 system-ui;max-width:900px;margin:40px auto;padding:0 16px;color:#1d1f1b}}ul{{list-style:none;padding:0}}li{{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid #ddd}}img{{width:140px;height:95px;object-fit:cover;flex:none}}a{{word-break:break-all;color:#1e5b3a}}</style></head><body><h1>Źródła zdjęć</h1><p>Wszystkie zdjęcia na stronie to materiały EXEVER: katalog opublikowany na exever.pl oraz galeria realizacji firmy w serwisie Oferteo.pl. Logo – z exever.pl. Zdjęcia są przycięte, bez filtrów. Na stronie nie ma zdjęć stockowych.</p><ul>{lis}</ul><p><a href="./">← strona główna</a></p></body></html>
'''
    open(os.path.join(ROOT, 'zrodla-zdjec.html'), 'w', encoding='utf-8', newline='\n').write(html)

if __name__ == '__main__':
    home(); domy(); instalacje(); realizacje(); ofirmie(); kontakt(); polityka(); extras()
    js = open(os.path.join(ROOT, '_src', 'app-main.js'), encoding='utf-8').read()
    licz = open(os.path.join(ROOT, '_src', 'licznik.js'), encoding='utf-8').read()
    open(os.path.join(ROOT, 'assets', 'app.js'), 'w', encoding='utf-8', newline='\n').write(js + '\n/* licznik otwarć dema – nie usuwać */\n' + licz)
    print('ok')
