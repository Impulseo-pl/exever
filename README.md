# EXEVER — demo v2 (domy szkieletowe + instalacje)

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

Styl: biel + piaskowe tło sekcji, jedna ciemna sekcja (instalacje), akcent butelkowa zieleń (#1e5b3a — nawiązanie do zieleni
z ich katalogu, bez limonki), jedna rodzina fontów Onest (lokalnie, woff2), ich czarne logo w poziomie złożone z pionowego.
Bez mono-etykiet, liczników, ziarna, ekranu ładowania. Polskie „sierotki” (i, w, z…) sklejane twardą spacją.

## Techniczne SEO

- Na każdej podstronie: `title`, `description`, `canonical`, Open Graph (`img/og.jpg`, `img/og-instalacje.jpg`), JSON-LD
  (`HomeAndConstructionBusiness` z NIP/KRS/REGON, oddziałem i osobami; `BreadcrumbList`; `Service`; `FAQPage`).
- Fonty lokalne, LCP z `preload` + `fetchpriority`, `srcset` 720/1400/pełny, `width`/`height`, `loading="lazy"`.
- `sitemap.xml` (7 adresów), `robots.txt`, `404.html`, favicon, polityka prywatności, dolny pasek „Zadzwoń / Zapytaj o wycenę” na telefonie.
- Licznik otwarć dema (`demo_views`) — koniec `assets/app.js`, 1:1 z mk-bau (`_src/licznik.js`).
- **DEMO ma `noindex`.** Przy wdrożeniu: usunąć `noindex`, podmienić `https://impulseo-pl.github.io/exever/` na domenę
  (stała `BASE` w build.py), w 404 ścieżki `/exever/` na `/`, podpiąć formularz, 301 ze starych adresów WordPressa
  (`/o-nas/`→`/o-firmie/`, `/uslugi/`→`/domy-szkieletowe/`, `/technologia/`→`/domy-szkieletowe/#sciana`).

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
