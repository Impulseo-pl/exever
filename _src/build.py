# -*- coding: utf-8 -*-
"""Generator dema EXEVER v2. Uruchom: python _src/build.py (z katalogu exever)."""
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
    "department": {"@type": "HomeAndConstructionBusiness", "name": "EXEVER – oddział Koszalin",
                   "address": {"@type": "PostalAddress", "streetAddress": "ul. Przemysłowa 6c",
                               "addressLocality": "Koszalin", "addressRegion": "zachodniopomorskie", "addressCountry": "PL"}},
    "areaServed": {"@type": "Country", "name": "Polska"},
    "employee": [{"@type": "Person", "name": "Krzysztof Kowalski", "jobTitle": "Prezes zarządu, project manager"},
                 {"@type": "Person", "name": "Damian Michalik", "jobTitle": "Project manager"}],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Usługi", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in [
            "Domy szkieletowe z drewna pod klucz", "Instalacje elektryczne", "Instalacje fotowoltaiczne",
            "Instalacje sanitarne i grzewcze", "Kotłownie gazowe i na pellet", "Pompy ciepła",
            "Instalacje teletechniczne i monitoring", "Automatyka budynkowa"]]}
}

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (u, n) in enumerate(items)]}

def head(p, path, title, desc, og='og.jpg', ogalt='Dom szkieletowy EXEVER z elewacją z desek', ld=None, preload=None):
    graph = ld or []
    ldj = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
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
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{BASE}{path}">
<meta name="theme-color" content="#1a1a18">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="EXEVER">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}img/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogalt}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preload" href="{p}fonts/hanken-grotesk-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}fonts/hanken-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="{p}assets/styles.css">
<script type="application/ld+json">
{ldj}
</script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
'''

def header(p, cur):
    links = '\n'.join(
        f'      <a href="{p}{u}"{" aria-current=\"page\"" if u == cur else ""}>{n}</a>' for u, n in NAV)
    return f'''<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{p or './'}" aria-label="EXEVER – strona główna"><img src="{p}img/logo-biale.png" width="535" height="120" alt="EXEVER"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav class="menu" id="menu" aria-label="Menu główne">
{links}
      <a class="head-tel" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a>
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
          <li><a href="{p}instalacje/">Instalacje elektryczne</a></li>
          <li><a href="{p}instalacje/">Instalacje sanitarne i grzewcze</a></li>
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

def cta(p, h='Masz działkę albo projekt? Porozmawiajmy.', t='Pierwsza konsultacja jest bezpłatna. Doradzimy, zanim cokolwiek podpiszesz.', temat='dom'):
    return f'''<section class="cta">
  {pic(p, 'dom-narozny', '', '100vw', cls='cta-bg')}
  <div class="wrap">
    <div>
      <h2>{h}</h2>
      <p>{t}</p>
    </div>
    <div class="actions">
      <a class="btn btn-light" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a>
      <a class="btn btn-ghost" href="{p}kontakt/?temat={temat}">Napisz do nas</a>
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
    def col(title, items, start):
        lis = '\n'.join(f'          <li><span>{start+i}</span><div><b>{a}</b><p>{b}</p></div></li>' for i, (a, b) in enumerate(items))
        return f'      <div>\n        <h3>{title}</h3>\n        <ol>\n{lis}\n        </ol>\n      </div>'
    return f'''    <div class="steps">
{col('Zanim ruszy budowa', STEPS_A, 1)}
{col('Budowa i odbiór', STEPS_B, 6)}
    </div>'''

OFERTEO = 'https://www.oferteo.pl/exever-spolka-z-ograniczona-odpowiedzialnoscia/firma/4053523'
def reviews():
    return f'''    <div class="reviews">
      <figure class="review">
        <div class="stars" aria-label="Ocena 5 na 5">★★★★★</div>
        <blockquote>„Szybko, solidnie, pełna komunikacja. Serwis gwarancyjny i pogwarancyjny.”</blockquote>
        <figcaption>B. · opinia w serwisie <a href="{OFERTEO}" rel="noopener">Oferteo.pl</a></figcaption>
      </figure>
      <figure class="review">
        <div class="stars" aria-label="Ocena 5 na 5">★★★★★</div>
        <blockquote>„Szybka, fajna obsługa, bardzo porządny wykonawca.”</blockquote>
        <figcaption>M. Ł. · opinia w serwisie <a href="{OFERTEO}" rel="noopener">Oferteo.pl</a></figcaption>
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
      <figure class="wall-fig">
        <div class="wall-pic">
          {pic(p, 'przekroj', 'Przekrój ściany domu szkieletowego EXEVER: płyty, izolacja, szkielet i elewacja', '(min-width: 961px) 620px, 100vw')}
{pins}
        </div>
      </figure>
      <div>
        <ol class="layers">
{lis}
        </ol>
        <p class="src">Rysunek i opis warstw: katalog i opis technologii EXEVER.</p>
      </div>
    </div>'''

def specs():
    return '''    <div class="specs">
      <div><b>150 mm</b><span>wełny mineralnej w ścianach</span></div>
      <div><b>do 250 mm</b><span>izolacji w dachu i podłodze</span></div>
      <div><b>3 szyby</b><span>w oknach, ograniczone mostki termiczne</span></div>
      <div><b>OSB + Fermacell</b><span>ściany działowe</span></div>
    </div>'''

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
def gallery(p, only=None, skip=()):
    items = []
    for n, k, c, d in GAL:
        if only and k != only: continue
        if n in skip: continue
        items.append(f'''      <a href="{p}img/{full(n)}" data-k="{k}" data-cap="{c} – {d}">{pic(p, n, c, '(min-width: 961px) 380px, (min-width: 681px) 50vw, 100vw')}<span class="gcap">{c}<small>{d}</small></span></a>''')
    return '    <div class="gallery">\n' + '\n'.join(items) + '\n    </div>'

def sierotki(html):
    # jednoliterowe spójniki i przyimki nie zostają na końcu wiersza (poza <script> i znacznikami)
    parts = re.split(r'(<script.*?</script>|<[^>]+>)', html, flags=re.S)
    for i, s in enumerate(parts):
        if s.startswith('<'):
            continue
        parts[i] = re.sub(r'(?<![\w&;])([aiouwzAIOUWZ]) ', r'\1&nbsp;', s)
    return ''.join(parts)

def write(path, html):
    html = sierotki(html)
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
    h = head(p, '', 'EXEVER Ustka – domy szkieletowe z drewna i instalacje',
             'EXEVER sp. z o.o. z Ustki: domy szkieletowe z drewna od projektu do odbioru oraz instalacje elektryczne, sanitarne i grzewcze. Od 2010 roku. Tel. 601 681 185.',
             ld=[ORG, {"@type": "WebSite", "@id": BASE + "#strona", "url": BASE, "name": "EXEVER", "inLanguage": "pl-PL",
                       "publisher": {"@id": BASE + "#firma"}}],
             preload=('dom-dlugi', '100vw'))
    body = f'''
<section class="hero">
  <div class="hero-txt">
    <h1>Budujemy domy szkieletowe i robimy w nich instalacje</h1>
    <p class="lead">Prowadzimy budowę od rozmowy o działce i projekcie, przez formalności w urzędzie, po odbiór techniczny z dokumentacją. Instalacje elektryczne, sanitarne i grzewcze wykonujemy sami – od 2010 roku, także w halach i budynkach wielorodzinnych.</p>
    <div class="actions">
      <a class="btn btn-main" href="kontakt/?temat=dom">Zapytaj o dom</a>
      <a class="btn btn-sec" href="realizacje/">Zobacz realizacje</a>
    </div>
    <div class="hero-meta">
      <div><b>Od 2010 roku</b>w rejestrze KRS</div>
      <div><b>Ustka i Koszalin</b>siedziba i oddział</div>
      <div><b><a href="tel:{TEL1H}" style="color:inherit;text-decoration:none">{TEL1}</a></b>{MAIL}</div>
    </div>
  </div>
  <div class="hero-img">
    {pic(p, 'dom-dlugi', 'Dom szkieletowy EXEVER z przeszkleniami i elewacją z desek', '100vw', lazy=False, high=True)}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Cały dom albo same instalacje</h2>
      <p>Możemy postawić dom od fundamentów po wykończenie. Możemy też wykonać tylko instalacje w budynku, który już stoi albo właśnie powstaje.</p>
    </div>
    <div class="doors">
      <a class="door" href="domy-szkieletowe/">
        <div class="door-img">{pic(p, 'dom-narozny', 'Dom szkieletowy z elewacją z pionowych desek', '(min-width: 961px) 586px, 100vw')}</div>
        <div class="door-body">
          <h3>Dom szkieletowy pod klucz</h3>
          <p>Konstrukcja z drewna, wełna mineralna w ścianach, dachu i podłodze, wykończenie w standardzie, który wybierzesz.</p>
          <ul>
            <li>gotowy projekt albo projekt od podstaw</li>
            <li>pomoc przy pozwoleniu na budowę</li>
            <li>fundamenty, konstrukcja, instalacje, wykończenie</li>
            <li>odbiór techniczny z pełną dokumentacją</li>
          </ul>
          <span class="more">Domy szkieletowe</span>
        </div>
      </a>
      <a class="door" href="instalacje/">
        <div class="door-img">{pic(p, 'hala-przenosniki', 'Hala magazynowa z linią przenośników – realizacja instalacji EXEVER', '(min-width: 961px) 586px, 100vw')}</div>
        <div class="door-body">
          <h3>Instalacje w budynkach</h3>
          <p>Dla firm wykonawczych, inwestorów i klientów indywidualnych – w domach, halach i budynkach wielorodzinnych.</p>
          <ul>
            <li>instalacje elektryczne i odgromowe</li>
            <li>instalacje wodno-kanalizacyjne i grzewcze</li>
            <li>kotłownie gazowe i na pellet, pompy ciepła</li>
            <li>fotowoltaika, teletechnika, monitoring</li>
          </ul>
          <span class="more">Instalacje</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap">
    <div class="split">
      <div class="split-img">
        <div class="pair">
          {pic(p, 'szkielet-hala', 'Konstrukcja szkieletowa ścian i dachu w hali', '(min-width: 961px) 320px, 50vw')}
          {pic(p, 'welna', 'Wełna mineralna ułożona między elementami konstrukcji', '(min-width: 961px) 260px, 50vw')}
        </div>
        <p class="figcap">Konstrukcja i izolacja – zdjęcia z katalogu EXEVER.</p>
      </div>
      <div class="split-txt">
        <div class="kicker">Jak budujemy</div>
        <h2>Instalacje planujemy razem z konstrukcją</h2>
        <p class="lead">Konstrukcję domu składamy pod dachem, w hali. Zanim ściany zostaną zamknięte, prowadzimy w nich przewody i rury – instalacje to nasza pierwsza specjalność, więc nie dokładamy ich na końcu.</p>
        <ul class="ticks">
          <li><b>Szkielet z drewna</b>, między elementami wełna mineralna lub skalna</li>
          <li><b>Folia paroizolacyjna i wiatroizolacyjna</b> po obu stronach izolacji</li>
          <li><b>Ściany działowe z OSB i Fermacell</b> – półkę czy obraz powiesisz bez kombinowania</li>
          <li><b>Potrójne szyby</b> i ograniczone mostki termiczne</li>
        </ul>
        <div class="actions"><a class="more" href="domy-szkieletowe/#sciana">Zobacz, co jest w ścianie</a></div>
      </div>
    </div>
{specs()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head-row">
      <div class="sec-head">
        <div class="kicker">Instalacje</div>
        <h2>Od instalacji zaczynaliśmy w 2010 roku</h2>
        <p>Dziś robimy je w domach, halach i budynkach wielorodzinnych. Pracujemy dla firm wykonawczych, inwestorów i klientów indywidualnych na terenie całej Polski.</p>
      </div>
      <a class="btn btn-sec" href="instalacje/">Zakres instalacji</a>
    </div>
    <div class="inst">
      <div>
        <h3>Elektryczne</h3>
        <ul><li>instalacje elektryczne</li><li>rozdzielnie</li><li>oświetlenie</li><li>instalacje odgromowe</li><li>fotowoltaika</li></ul>
      </div>
      <div>
        <h3>Sanitarne i grzewcze</h3>
        <ul><li>instalacje wodno-kanalizacyjne</li><li>instalacje grzewcze</li><li>kotłownie gazowe i na pellet</li><li>pompy ciepła</li></ul>
      </div>
      <div>
        <h3>Teletechnika i automatyka</h3>
        <ul><li>instalacje teletechniczne</li><li>monitoring</li><li>automatyka budynkowa</li><li>zdalne sterowanie w domu</li></ul>
      </div>
    </div>
    <div class="proj">
      <figure>{pic(p, 'hala-kurierska', 'Hala kurierska – instalacje elektryczne EXEVER', '(min-width: 961px) 480px, 100vw')}<figcaption>Instalacje elektryczne w hali kurierskiej</figcaption></figure>
      <figure>{pic(p, 'rozdzielnia', 'Rozdzielnia elektryczna wykonana przez EXEVER', '(min-width: 961px) 340px, 50vw')}<figcaption>Rozdzielnia elektryczna</figcaption></figure>
      <figure>{pic(p, 'resort', 'Nadmorski resort – instalacje elektryczne EXEVER', '(min-width: 961px) 340px, 50vw')}<figcaption>Instalacje elektryczne w nadmorskim resorcie</figcaption></figure>
      <figure>{pic(p, 'kotlownia', 'Kotłownia z instalacją grzewczą w Ustce', '(min-width: 961px) 340px, 50vw')}<figcaption>Kotłownia i instalacja grzewcza, Ustka</figcaption></figure>
      <figure>{pic(p, 'budynek-wielorodzinny', 'Budynek wielorodzinny w budowie – instalacje wod-kan EXEVER', '(min-width: 961px) 340px, 50vw')}<figcaption>Instalacje wod-kan w budynku wielorodzinnym</figcaption></figure>
    </div>
    <p style="margin-top:28px"><a class="more" href="realizacje/">Wszystkie realizacje</a></p>
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap">
    <div class="sec-head">
      <h2>Jak wygląda budowa domu z nami</h2>
      <p>Prowadzimy całość, także część papierową. Na każdym etapie wiesz, co się dzieje i co będzie dalej.</p>
    </div>
{steps()}
  </div>
</section>

<section class="sec sec-sand">
  <div class="wrap">
    <div class="sec-head">
      <h2>Opinie klientów</h2>
      <p>Ocena 5,0 na 5 w serwisie Oferteo.pl.</p>
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
          {"@type": "Service", "name": "Domy szkieletowe z drewna pod klucz", "serviceType": "Budowa domów szkieletowych",
           "provider": {"@id": BASE + "#firma"}, "areaServed": {"@type": "Country", "name": "Polska"}, "url": BASE + path},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    h = head(p, path, 'Domy szkieletowe z drewna pod klucz – EXEVER Ustka',
             'Domy szkieletowe (kanadyjskie) od projektu do odbioru: fundamenty, konstrukcja, instalacje, ocieplenie i wykończenie. 150 mm wełny w ścianach, potrójne szyby. EXEVER Ustka.',
             ld=ld, preload=('dom-dlugi', '100vw'))
    faq = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = f'''
<section class="phero">
  <div class="wrap">
    {crumbs(p, 'Domy szkieletowe')}
    <h1>Domy szkieletowe z drewna – od projektu do odbioru kluczy</h1>
    <p class="lead">Dom szkieletowy, nazywany też kanadyjskim, ma konstrukcję z drewna wypełnioną izolacją. Budujemy go od fundamentów po wykończenie i sami wykonujemy w nim wszystkie instalacje.</p>
    <div class="actions">
      <a class="btn btn-main" href="../kontakt/?temat=dom">Zapytaj o dom</a>
      <a class="btn btn-sec" href="#przebieg">Jak przebiega budowa</a>
    </div>
  </div>
</section>
<div class="wide-img">{pic(p, 'dom-dlugi', 'Dom szkieletowy EXEVER z przeszkleniami od podłogi', '100vw', lazy=False, high=True)}</div>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div class="split-txt">
        <h2>Dlaczego drewno</h2>
        <p class="lead">W krajach bogatych w lasy buduje się z drewna od wieków. To materiał mocny i stabilny, a jednocześnie elastyczny – dobrze znosi naprężenia.</p>
        <p>Drewno na elewacji pokryte woskiem, bejcą albo lakierem dobrze pokazuje usłojenie i nadaje domowi ciepły wygląd. Ściany zewnętrzne obudowujemy drewnem świerkowym albo tworzywem – do wyboru.</p>
        <ul class="ticks">
          <li><b>Konstrukcja dopasowana do projektu</b> – gotowego albo przygotowanego od podstaw</li>
          <li><b>Dokładność montażu</b> – od niej zależy trwałość domu i brak błędów na kolejnych etapach</li>
          <li><b>Wykończenie w wybranym standardzie</b>, wewnątrz i na zewnątrz</li>
        </ul>
      </div>
      <div class="split-img">
        {pic(p, 'elewacja', 'Elewacja z desek układanych poziomo i okna w grafitowych ramach', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Elewacja z desek układanych poziomo.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-sand" id="sciana">
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
    <div class="split rev">
      <div class="split-img">
        {pic(p, 'wnetrze', 'Wnętrze gotowego domu szkieletowego EXEVER', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Wnętrze gotowego domu.</p>
      </div>
      <div class="split-txt">
        <h2>Ogrzewanie i automatyka od tej samej ekipy</h2>
        <p class="lead">Instalacje elektryczne, sanitarne i grzewcze to nasza pierwsza specjalność. W domu, który budujemy, wykonujemy je sami.</p>
        <ul class="ticks">
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

<section class="sec sec-sand">
  <div class="wrap">
    <div class="sec-head-row">
      <div class="sec-head"><h2>Nasze domy</h2><p>Od szkieletu w hali po gotową elewację.</p></div>
      <a class="more" href="../realizacje/">Wszystkie realizacje</a>
    </div>
{gallery(p, 'domy', skip=('welna', 'osb'))}
  </div>
</section>

<section class="sec sec-dark" id="przebieg">
  <div class="wrap">
    <div class="sec-head">
      <h2>Przebieg budowy w 10 krokach</h2>
      <p>Od pierwszej rozmowy do przekazania kluczy prowadzi Cię jedna firma.</p>
    </div>
{steps()}
  </div>
</section>

<section class="sec sec-sand">
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
def instalacje():
    p = '../'
    path = 'instalacje/'
    ld = [crumbs_ld([('', 'EXEVER'), (path, 'Instalacje')]),
          {"@type": "Service", "name": "Instalacje elektryczne, sanitarne i grzewcze", "serviceType": "Instalacje budowlane",
           "provider": {"@id": BASE + "#firma"}, "areaServed": {"@type": "Country", "name": "Polska"}, "url": BASE + path}]
    h = head(p, path, 'Instalacje elektryczne, sanitarne i grzewcze – EXEVER Ustka',
             'Instalacje elektryczne, odgromowe, fotowoltaika, wod-kan, instalacje grzewcze, kotłownie gazowe i na pellet, pompy ciepła, teletechnika. Dla firm i klientów indywidualnych. EXEVER, od 2010 roku.',
             og='og-instalacje.jpg', ogalt='Hala kurierska – instalacje elektryczne EXEVER', ld=ld, preload=('hala-przenosniki', '100vw'))
    body = f'''
<section class="phero">
  <div class="wrap">
    {crumbs(p, 'Instalacje')}
    <h1>Instalacje elektryczne, sanitarne i grzewcze</h1>
    <p class="lead">Od tego zaczęliśmy w 2010 roku. Wykonujemy instalacje w domach, halach i budynkach wielorodzinnych – dla firm wykonawczych, inwestorów i klientów indywidualnych, na terenie całej Polski.</p>
    <div class="actions">
      <a class="btn btn-main" href="../kontakt/?temat=instalacja">Zapytaj o instalację</a>
      <a class="btn btn-sec" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a>
    </div>
  </div>
</section>
<div class="wide-img">{pic(p, 'hala-przenosniki', 'Hala magazynowa z linią przenośników – realizacja EXEVER', '100vw', lazy=False, high=True)}</div>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Zakres prac</h2></div>
    <div class="inst">
      <div>
        <h3>Elektryczne</h3>
        <ul><li>instalacje elektryczne w domach, halach i budynkach usługowych</li><li>rozdzielnie elektryczne</li><li>montaż oświetlenia</li><li>instalacje odgromowe</li><li>instalacje fotowoltaiczne</li></ul>
      </div>
      <div>
        <h3>Sanitarne i grzewcze</h3>
        <ul><li>instalacje wodno-kanalizacyjne</li><li>instalacje grzewcze</li><li>kotłownie gazowe i na pellet</li><li>pompy ciepła</li><li>odnawialne źródła energii</li></ul>
      </div>
      <div>
        <h3>Teletechnika i automatyka</h3>
        <ul><li>instalacje teletechniczne</li><li>systemy monitoringu</li><li>automatyka budynkowa</li><li>zdalne sterowanie urządzeniami w domu</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-sand">
  <div class="wrap">
    <div class="split">
      <div class="split-img">
        {pic(p, 'hala-kurierska', 'Hala kurierska – instalacje elektryczne EXEVER', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Instalacje elektryczne w hali kurierskiej.</p>
      </div>
      <div class="split-txt">
        <div class="kicker">Dla firm i inwestorów</div>
        <h2>Hale, resorty, budynki wielorodzinne</h2>
        <p class="lead">Współpracujemy z firmami wykonawczymi i inwestorami. Do każdego zlecenia podchodzimy rzetelnie i w przemyślany sposób.</p>
        <ul class="ticks">
          <li><b>Hala kurierska</b> – instalacje elektryczne</li>
          <li><b>Hala magazynowa z przenośnikami</b></li>
          <li><b>Nadmorski resort</b> – instalacje elektryczne</li>
          <li><b>Budynek wielorodzinny w Ustce</b> – instalacje wod-kan</li>
        </ul>
      </div>
    </div>
    <div class="split rev">
      <div class="split-img">
        {pic(p, 'kotly', 'Kotły i instalacja grzewcza wykonana przez EXEVER w Ustce', '(min-width: 961px) 564px, 100vw')}
        <p class="figcap">Instalacje wod-kan i grzewcze, Ustka.</p>
      </div>
      <div class="split-txt">
        <div class="kicker">Dla domu</div>
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
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'Realizacje')])])
    body = f'''
<section class="phero">
  <div class="wrap">
    {crumbs(p, 'Realizacje')}
    <h1>Realizacje</h1>
    <p class="lead">Domy szkieletowe – od konstrukcji w hali po gotową elewację – i instalacje, które wykonaliśmy w halach, resortach i budynkach wielorodzinnych.</p>
  </div>
</section>
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
             'EXEVER sp. z o.o. – firma z Ustki, w rejestrze KRS od 2010 roku. Instalacje elektryczne, sanitarne i grzewcze oraz domy szkieletowe z drewna. Oddział w Koszalinie.',
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'O firmie')]), ORG])
    body = f'''
<section class="phero">
  <div class="wrap">
    {crumbs(p, 'O firmie')}
    <h1>EXEVER – firma z Ustki, od 2010 roku</h1>
    <p class="lead">Zaczynaliśmy od instalacji elektrycznych i sanitarnych. Dziś budujemy też całe domy w konstrukcji szkieletowej – i instalacje wykonujemy w nich sami.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div class="split-txt">
        <h2>Jedna firma zamiast kilku ekip</h2>
        <p class="lead">Spółkę zarejestrowaliśmy w lutym 2010 roku. Od początku wykonujemy instalacje – dla firm wykonawczych i dla klientów indywidualnych.</p>
        <p>Budując dom, prowadzimy wszystko: projekt, formalności, fundamenty, konstrukcję, instalacje, ocieplenie i wykończenie. Nie musisz koordynować kilku wykonawców ani pilnować, żeby elektryk zdążył przed zamknięciem ścian.</p>
        <p>Siedzibę mamy w Ustce, oddział w Koszalinie.</p>
      </div>
      <div class="split-img">
        {pic(p, 'szkielet-hala', 'Konstrukcja szkieletowa domu EXEVER w hali', '(min-width: 961px) 564px, 100vw')}
      </div>
    </div>
  </div>
</section>

<section class="sec sec-sand">
  <div class="wrap">
    <div class="split" style="align-items:start">
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
             ld=[crumbs_ld([('', 'EXEVER'), (path, 'Kontakt')]), ORG])
    body = f'''
<section class="phero" style="padding-bottom:40px;border-bottom:0">
  <div class="wrap">
    {crumbs(p, 'Kontakt')}
    <h1>Kontakt</h1>
    <p class="lead">Zadzwoń albo napisz, czego potrzebujesz. Pierwsza konsultacja w sprawie domu jest bezpłatna.</p>
  </div>
</section>
<section class="sec" style="padding-top:64px">
  <div class="wrap contact">
    <div>
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
    h = head(p, path, 'Polityka prywatności | EXEVER', 'Zasady przetwarzania danych osobowych przez EXEVER sp. z o.o., Ustka.',
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
<header class="site-head"><div class="wrap head-in"><a class="brand" href="{b}" aria-label="EXEVER – strona główna"><img src="{b}img/logo-biale.png" width="535" height="120" alt="EXEVER"></a></div></header>
<main class="sec"><div class="wrap doc">
<h1>Nie ma takiej strony</h1>
<p style="margin-top:18px">Adres mógł się zmienić. Zacznij od strony głównej albo zadzwoń: <a href="tel:{TEL1H}">{TEL1}</a>.</p>
<div class="actions"><a class="btn btn-main" href="{b}">Strona główna</a><a class="btn btn-sec" href="{b}kontakt/">Kontakt</a></div>
</div></main>
</body></html>
'''
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n').write(html)
    urls = ['', 'domy-szkieletowe/', 'instalacje/', 'realizacje/', 'o-firmie/', 'kontakt/', 'polityka-prywatnosci/']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         ''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>2026-09-26</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
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
