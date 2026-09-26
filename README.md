# EXEVER — demo (domy szkieletowe + instalacje)

Lead: **Krzysztof** (w KRS prezes zarządu: Krzysztof Kowalski), **EXEVER sp. z o.o.**, +48 601 681 185, biuro@exever.pl,
ul. Grunwaldzka 18, 76-270 Ustka; oddział: ul. Przemysłowa 6c, Koszalin. Obecna strona: https://www.exever.pl/
CRM: karta `b9c95493-f8ee-4e7c-98c2-181a94b5a9ad`.

Podgląd lokalny: `python -m http.server 8123`. Sprawdzanie opublikowanego dema przez nas — **zawsze z `?team=1`**.

## Założenia

Obecna strona exever.pl to szablon WordPress (Kadence) ze zdjęciami ze stocków (szklane biurowce, „uśmiechnięty mężczyzna”)
i licznikami „50 projektów / 60+ klientów / 15 lat”. Demo pokazuje to, co firma naprawdę robi: **drewniane domy szkieletowe**
(zdjęcia z ich własnego katalogu) plus **instalacje**, od których firma zaczynała (PKD główne 43.21.Z).

Styl: zwykła strona firmy budowlanej — biel, piaskowe tło sekcji, akcent leśna zieleń (#2f5a3a, nawiązanie do zieleni
z ich katalogu), nagłówki Bitter, tekst Source Sans 3 (inne niż w mk-bau). Zdjęcia duże, bez filtrów, rzędy tekst/zdjęcie
naprzemiennie. Bez ekranu ładowania, ziarna, mono-etykiet, liczników, kafelków.

Sekcje: hero → pasek „w skrócie” → o firmie (fakty z KRS) → oferta (3 rzędy) → z czego jest dom (warstwy ściany,
dane z ich podstrony Technologia) → galeria z katalogu → opinie z Oferteo → przebieg budowy (ich 10 kroków w 2 kolumnach)
→ kontakt + formularz + mapa.

## Techniczne SEO

- `title`, `description`, `canonical`, Open Graph (`img/og.jpg` 1200×630), JSON-LD `HomeAndConstructionBusiness`
  (NIP, KRS, REGON, adres, oddział Koszalin, usługi) + `WebSite`.
- Fonty lokalne woff2 (latin + latin-ext, preload), LCP z `preload` + `fetchpriority`, `srcset` 720/1100/pełny,
  `width`/`height`, `loading="lazy"` poniżej pierwszego ekranu.
- `sitemap.xml`, `robots.txt`, `404.html`, `favicon.svg` (sygnet EXEVER), `apple-touch-icon.png`, `site.webmanifest`,
  polityka prywatności, `zrodla-zdjec.html`.
- Menu na telefonie, dolny pasek „Zadzwoń / Zapytaj o dom”.
- Licznik otwarć dema (`demo_views`) — ostatnie IIFE w `assets/app.js`, skopiowane 1:1 z mk-bau.
- **DEMO ma `noindex`.** Przy wdrożeniu: usunąć `noindex`, podmienić `https://impulseo-pl.github.io/exever/` na domenę
  klienta (canonical, og, JSON-LD, sitemap, robots), w 404.html ścieżki `/exever/` na `/`, podpiąć formularz.

## Skąd są fakty (zero zmyślonych liczb)

| Na stronie | Źródło |
|---|---|
| Od 2010 roku | KRS 0000349698 — rejestracja 23.02.2010 (imsig.pl); opis firmy na Oferteo: „Rozpoczęliśmy działalność w 2010 roku” |
| NIP, REGON, KRS, adres Grunwaldzka 18, 76-270 Ustka | stopka exever.pl + KRS (imsig.pl) |
| Oddział Przemysłowa 6c, Koszalin | exever.pl/kontakt |
| Telefony 601 681 185, 500 629 172, biuro@exever.pl | exever.pl |
| Domy szkieletowe, 10 kroków budowy, pomoc przy pozwoleniu | exever.pl/uslugi |
| Instalacje: elektryczne, teletechniczne, monitoring, sanitarne i grzewcze, OZE i kotłownie | exever.pl/o-nas |
| Zaczynali od instalacji elektrycznych i sanitarnych | Oferteo (opis firmy) + PKD główne 43.21.Z |
| Warstwy ściany: 150 mm / do 250 mm, wełna, folie, OSB3/OSB4, Fermacell, potrójne szyby, konstrukcja nośna ze stali | exever.pl/technologia |
| Dwie opinie 5/5 („Szybko, solidnie…”, „Szybka fajna obsługa…”) | oferteo.pl/exever-spolka-z-ograniczona-odpowiedzialnoscia/firma/4053523 |
| Krzysztof Kowalski | exever.pl/o-nas (Project Manager) + KRS (prezes zarządu wg krs-pobierz) |
| Zdjęcia domów | katalog EXEVER na exever.pl/technologia (przycięte, bez filtrów) — lista w `zrodla-zdjec.html` |

**Celowo pominięte:** „50 zrealizowanych projektów”, „60+ szczęśliwych klientów”, „15 lat na rynku” z exever.pl/o-nas —
wyglądają na liczby z szablonu, a „15 lat” nie zgadza się z rejestracją w 2010 (dziś 16 lat). Wstawić, jeśli klient potwierdzi.

## Do potwierdzenia z klientem (przed wdrożeniem)

1. **Liczby do strony**: ile domów zbudowali, ile instalacji — jeśli potwierdzi, dajemy sekcję z liczbami.
2. **Kod pocztowy**: Ustka to 76-270 (KRS), a stopka exever.pl ma 76-260. Koszalin: strona ma 75-216, katalogi 75-211.
   Czy Koszalin to hala produkcyjna, biuro czy tylko adres kontaktowy.
3. **Konstrukcja**: „szkielet z drewna” vs „konstrukcja nośna ze stali” (strona Technologia) — zdjęcia z katalogu pokazują
   domy na stalowej ramie/podwoziu (domy mobilne?). Jeśli to domy mobilne/modułowe — to mocny wyróżnik, warto go nazwać wprost.
4. **Obszar działania** (tylko Pomorze/Koszalin czy cała Polska).
5. **Zdjęcie do rzędu „Instalacje”** — teraz poglądowe z obecnej strony (Pixabay); potrzebne zdjęcie z ich realizacji.
6. Więcej zdjęć gotowych domów na działkach (u klientów), zdjęcie ekipy/hali.
7. Czy Krzysztof chce być podany z imienia i nazwiska w kontakcie, i czy numer 500 629 172 to Damian Michalik.
8. Ceny lub „ceny od” za dom — dziś brak, nie wstawiamy.
9. Formularz — podpiąć wysyłkę (teraz demo, nic nie wysyła).
