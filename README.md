# EXEVER — demo v5 (domy szkieletowe + instalacje)

Lead: **Krzysztof** (w KRS prezes zarządu: Krzysztof Kowalski), **EXEVER sp. z o.o.**, +48 601 681 185, biuro@exever.pl,
ul. Grunwaldzka 18, 76-270 Ustka; oddział: ul. Przemysłowa 6c, Koszalin. Obecna strona: https://www.exever.pl/
CRM: karta `b9c95493-f8ee-4e7c-98c2-181a94b5a9ad`. Demo: https://impulseo-pl.github.io/exever/ (sprawdzamy **zawsze z `?team=1`**).

Podgląd lokalny: z `C:\Users\kluch` uruchom `python -m http.server 8123` i wejdź na `http://127.0.0.1:8123/exever/`.
**Strony generuje `_src/build.py`** — treść zmieniaj tam, potem `python _src/build.py`. Zdjęcia: `_src/obrazy.py`.

## v2 (26.09) — „lepsza niż ich obecna, to konkretny klient”

Ich exever.pl to jedna krótka strona z szablonu WordPress: stockowe zdjęcia (dekarze w kaskach, szklane biurowce),
liczniki „50 / 60+ / 15 lat”, zero realizacji instalacji. Demo v2 to **pełny serwis, 6 podstron**:

| Strona | Co jest |
|---|---|
| `/` | hero z ich domem, dwie ścieżki (dom / instalacje), „instalacje planujemy razem z konstrukcją”, parametry, ciemna sekcja instalacji z 5 realizacjami, 10 kroków, opinie |
| `/domy-szkieletowe/` | dlaczego drewno, **interaktywny przekrój ściany** (6 warstw z ich katalogu), ogrzewanie i automatyka, galeria, 10 kroków, FAQ (+ FAQPage w JSON-LD) |
| `/instalacje/` | pełny zakres (elektryka, wod-kan i grzewcze, teletechnika), dla firm i inwestorów / dla domu, galeria realizacji |
| `/realizacje/` | 15 zdjęć z filtrem Domy / Instalacje i podglądem |
| `/o-firmie/` | historia od 2010, osoby, dane rejestrowe, opinie |
| `/kontakt/` | 2 telefony, adresy, mapa, formularz z tematem (`?temat=dom|instalacja` zaznacza opcję) |

**Najmocniejszy argument w rozmowie:** na Oferteo EXEVER ma 7 zdjęć własnych realizacji instalacji (hala kurierska, hala
z przenośnikami, nadmorski resort, budynek wielorodzinny w Ustce, kotłownie, rozdzielnia) — **na ich stronie nie ma żadnego
z nich**. W demie są wszystkie. Zero stocku: każde zdjęcie to ich materiał (`zrodla-zdjec.html`).

Styl (v5, 28.09) – v4 (szeroki Archivo, etykiety wersalikami, znaczki 01/02, pigułki, wielkie liczby) Szymon ocenił jako „AI slop”.
v5 to zwykła, jasna strona firmy budowlanej:
- **Nagłówki: Newsreader (szeryf), tekst: Source Sans 3** – lokalnie, przycięte do polskich znaków (6 plików, 113 KB łącznie).
- Biel + ciepła szarość (#f3f1ec) na co drugą sekcję, jeden akcent: ciemna zieleń świerka (#2e4a3e) – przyciski i linki. Drewno daje kolor na zdjęciach.
- Pasek z adresem i mailem nad menu, białe menu z czarnym logo, hero: tekst na bieli + zdjęcie domu do prawej krawędzi.
- Rzędy tekst/zdjęcie naprzemiennie, dane techniczne jako zwykła tabela, kroki budowy jako lista 1–10, opinie jako cytaty kursywą,
  na dole pas z telefonami zamiast ciemnego CTA na zdjęciu. Podstrony: biały nagłówek + zdjęcie na całą szerokość.
- **Przejścia jak na exever.pl/technologia** (tam Elementor `slideInLeft` / `slideInRight`): w każdym rzędzie element po lewej wjeżdża
  z lewej, po prawej – z prawej; w galerii lewa kolumna z lewej, prawa z prawej, środkowa się pojawia. `data-in="l|r|f"`,
  IntersectionObserver w `assets/app.js`, strony wyliczane w `slide()` w build.py. Bez JS i przy `prefers-reduced-motion` – bez ruchu.
  Argument w rozmowie: „te same przejścia, które macie teraz, tylko na szybkiej stronie”.

## Techniczne SEO

- **Kontrola:** `python _src/seo_check.py` — długość title/description, jeden h1, hierarchia nagłówków, canonical, OG, poprawność
  JSON-LD, alt + width/height obrazów, martwe linki i kotwice, duplikaty, pliki z sitemapy. Teraz: „OK – 7 stron, bez uwag”.
- **JSON-LD na każdej stronie jako jeden `@graph` z `@id`:** `HomeAndConstructionBusiness` (NIP/KRS/REGON, adres, geo, oddział, osoby,
  2× `contactPoint`, `sameAs` Oferteo, `hasMap`, `knowsAbout`, `areaServed`, katalog usług z linkami) + `WebSite` + strona
  (`WebPage` / `AboutPage` / `ContactPage` / `CollectionPage`) z `breadcrumb`, `primaryImageOfPage`, `dateModified`.
  Podstrony: `BreadcrumbList`, `Service` z katalogiem (dom: 10 etapów budowy; instalacje: 3 usługi z kotwicami), `FAQPage`,
  `ImageGallery` z 15 `ImageObject` (autor i właściciel praw = EXEVER).
- **Mapa witryny ze zdjęciami** (`image:image`, każde zdjęcie w pełnej rozdzielczości), `lastmod`, `robots.txt` (blokuje `/_src/`), `llms.txt`.
- W `<head>`: `hreflang` pl + x-default, Twitter Cards, `og:image:type`, `max-image-preview:large`, meta geo (Ustka), `referrer`.
- **Wydajność:** cały CSS wklejony zminifikowany do `<head>` (zero blokujących żądań), preload dwóch fontów i zdjęcia LCP z `fetchpriority`,
  zapasowy font z `size-adjust` (mniejszy CLS), `srcset`/`sizes` dopasowane do nowego układu, `width`/`height`, `loading="lazy"`.
- Kotwice `#elektryczne`, `#sanitarne`, `#teletechnika` na /instalacje/ — linkowane z paska usług i stopki.
- Licznik otwarć dema (`demo_views`) — koniec `assets/app.js`, 1:1 z mk-bau (`_src/licznik.js`).
- `404.html`, favicon, manifest, polityka prywatności, dolny pasek „Zadzwoń / Zapytaj o wycenę” na telefonie.
- **DEMO ma `noindex`.** Przy wdrożeniu: usunąć `noindex`, podmienić `https://impulseo-pl.github.io/exever/` na domenę
  (stała `BASE` w build.py i seo_check.py), w 404 ścieżki `/exever/` na `/`, podpiąć formularz, 301 ze starych adresów WordPressa
  (`/o-nas/`→`/o-firmie/`, `/uslugi/`→`/domy-szkieletowe/`, `/technologia/`→`/domy-szkieletowe/#sciana`), zgłosić sitemapę w Search Console,
  założyć/uzupełnić Profil Firmy w Google tymi samymi danymi (NAP 1:1 ze stroną).

## Skąd są fakty (zero zmyślonych liczb)

| Na stronie | Źródło |
|---|---|
| Od 2010, rejestracja 23.02.2010 | KRS 0000349698 (rejestr.io, imsig.pl); Oferteo: „Firma powstała w 2010 roku” |
| Zaczynali od instalacji elektrycznych i sanitarnych; firmy wykonawcze + klienci indywidualni; „na terenie Polski”; „rzetelnie i przemyślanie” | opis firmy na Oferteo |
| Zakres instalacji (w tym odgromowe, oświetlenie, PV, pompy ciepła, kotłownie gazowe i na pellet) | exever.pl/o-nas + kategorie i oferta na Oferteo |
| 10 kroków budowy, bezpłatna konsultacja, pozwolenie/zgłoszenie, fundamenty, odbiór z dokumentacją | exever.pl/uslugi |
| Drewno, warstwy ściany, 150 mm / do 250 mm, OSB3/OSB4 + Fermacell, potrójne szyby, ogrzewanie do wyboru, automatyka, zdalne sterowanie, monitoring | exever.pl/technologia |
| Krzysztof Kowalski, Damian Michalik — project managerowie; KK prezes zarządu | exever.pl/o-nas; KRS |
| Opinie 5/5 (B., M. Ł.) | oferteo.pl/exever-spolka-z-ograniczona-odpowiedzialnoscia/firma/4053523 |
| Podpisy realizacji instalacji | tytuły zdjęć w galerii Oferteo |
| Zdjęcia domów i przekrój ściany | katalog EXEVER na exever.pl/technologia (przycięte, bez zielonych skosów) |

**Celowo pominięte:** „50 projektów / 60+ klientów / 15 lat” z exever.pl — „15 lat” nie zgadza się z 2010, reszta wygląda na
liczby z szablonu. Ceny, czasy budowy, gwarancje — nigdzie ich nie podają.

## Do potwierdzenia z klientem (przed wdrożeniem)

1. **„Konstrukcję składamy pod dachem, w hali”** — wniosek ze zdjęć katalogu (szkielet i wełna w hali, gotowe domy na podporach
   na placu). Czy domy są przewożone w całości (moduły / domy mobilne)? Jeśli tak — to wyróżnik, dopisać wprost.
2. „Konstrukcja nośna ze stali” (exever.pl/technologia) vs szkielet drewniany — co dokładnie jest stalowe (rama pod domem?).
3. Prawdziwe liczby: ile domów, ile instalacji — wtedy sekcja z liczbami.
4. Kody pocztowe: Ustka 76-270 (KRS) vs 76-260 (stopka exever.pl); Koszalin 75-216 vs 75-211. Co jest w Koszalinie.
5. Obszar działania — Oferteo: zachodniopomorskie i dolnośląskie, opis: „na terenie Polski”.
6. Czyj jest numer 500 629 172 (Damian Michalik?) — wtedy przypisać numery do osób.
7. Zgoda na zdjęcia z Oferteo, zdjęcia gotowych domów u klientów na działkach, zdjęcie ekipy/hali.
8. Nazwy/miejsca realizacji (hala kurierska — dla kogo? resort — gdzie?) — tylko jeśli klient pozwoli.
9. Formularz — podpiąć wysyłkę (teraz demo, nic nie wysyła).
