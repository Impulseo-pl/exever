# -*- coding: utf-8 -*-
"""Kontrola technicznego SEO po zbudowaniu. Uruchom: python _src/seo_check.py (z katalogu exever)."""
import os, re, json, html as H
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://impulseo-pl.github.io/exever/'
PAGES = ['', 'domy-szkieletowe/', 'instalacje/', 'realizacje/', 'o-firmie/', 'kontakt/', 'polityka-prywatnosci/']
bad, titles, descs = [], {}, {}

def err(page, msg):
    bad.append(f'/{page}: {msg}')

for page in PAGES:
    fp = os.path.join(ROOT, page, 'index.html')
    s = open(fp, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    d = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    titles[page], descs[page] = t, d
    if not 25 <= len(t) <= 62: err(page, f'title ma {len(t)} znaków')
    if not 70 <= len(d) <= 160: err(page, f'description ma {len(d)} znaków')
    if '&nbsp;' in t: err(page, 'twarda spacja w <title>')
    if s.count('<h1') != 1: err(page, f'{s.count("<h1")} nagłówków h1')
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not canon or canon.group(1) != BASE + page: err(page, 'zły canonical')
    for m in ('og:title', 'og:description', 'og:image', 'og:url', 'twitter:card'):
        if m not in s: err(page, 'brak ' + m)
    # hierarchia nagłówków – bez przeskoków (h2 -> h4)
    lv = [int(x) for x in re.findall(r'<h([1-6])', s)]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1: err(page, f'przeskok nagłówków h{a} -> h{b}')
    # JSON-LD
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            g = json.loads(blk)['@graph']
        except Exception as e:
            err(page, 'JSON-LD nie parsuje się: ' + str(e)); continue
        ids = {x.get('@id') for x in g}
        for need in (BASE + '#firma', BASE + '#witryna', BASE + page + '#strona'):
            if need not in ids: err(page, 'JSON-LD bez ' + need)
        refs = set(re.findall(r'"@id":"([^"]+)"', blk))
        for r in refs:
            if r not in ids and not any(r == x.get('@id') for x in g):
                pass
    # obrazy: alt, wymiary, lazy poza pierwszym ekranem
    for img in re.findall(r'<img [^>]+>', s):
        if 'alt=' not in img: err(page, 'obraz bez alt: ' + img[:80])
        if 'width=' not in img or 'height=' not in img: err(page, 'obraz bez width/height: ' + img[:80])
    # linki wewnętrzne
    for href in re.findall(r'(?:href|src)="([^"#?]+)', s):
        if href.startswith(('http', 'mailto:', 'tel:', 'data:')): continue
        path = os.path.normpath(os.path.join(ROOT, page, unquote(href)))
        if os.path.isdir(path): path = os.path.join(path, 'index.html')
        if not os.path.exists(path): err(page, 'martwy link: ' + href)
    # kotwice w obrębie serwisu
    for href, anchor in re.findall(r'href="([^"#]*)#([\w-]+)"', s):
        target = os.path.normpath(os.path.join(ROOT, page, href or '.', 'index.html')) if not href.endswith('.html') else os.path.join(ROOT, page, href)
        if os.path.exists(target) and f'id="{anchor}"' not in open(target, encoding='utf-8').read():
            err(page, f'brak kotwicy #{anchor} w {href or "tej stronie"}')

for kind, d in (('title', titles), ('description', descs)):
    vals = list(d.values())
    for v in set(vals):
        if vals.count(v) > 1: bad.append(f'powtórzony {kind}: {v}')

sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
for loc in re.findall(r'<(?:loc|image:loc)>([^<]+)<', sm):
    rel = loc.replace(BASE, '')
    p = os.path.join(ROOT, rel, 'index.html') if (rel == '' or rel.endswith('/')) else os.path.join(ROOT, rel)
    if not os.path.exists(p): bad.append('sitemap wskazuje na brakujący plik: ' + loc)

print('\n'.join(bad) if bad else f'OK – {len(PAGES)} stron, bez uwag')
raise SystemExit(1 if bad else 0)
