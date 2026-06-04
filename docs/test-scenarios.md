# Scenariusze testów ręcznych

Tych scenariuszy używaj, żeby sprawdzić `$stop-slop-pl` przed publikacją zmian.

## 1. Urzędowy język na prosty

Prompt:

```text
Use $stop-slop-pl. Popraw styl i usuń slop po polsku:
W celu dokonania zgłoszenia należy wypełnić niniejszy formularz oraz przekazać go do właściwej komórki organizacyjnej w terminie 7 dni od daty zaistnienia zdarzenia.
```

Oczekiwane zachowanie:

- Najpierw zwraca poprawiony tekst.
- Pisze bezpośrednią, prostą polszczyzną.
- Zachowuje termin 7 dni.
- Usuwa `w celu`, `dokonania`, `niniejszy` i urzędową mgłę.

## 2. Marketingowy slop

Prompt:

```text
Use $stop-slop-pl. Tryb: marketing. Usuń slop:
Nasze innowacyjne i kompleksowe rozwiązanie stanowi kluczowy element transformacji cyfrowej, umożliwiając firmom skuteczne wykorzystanie potencjału danych w dynamicznie zmieniającym się świecie.
```

Oczekiwane zachowanie:

- Wycina nieuzasadnione przymiotniki.
- Nie zmyśla dowodów.
- Konkretyzuje obietnicę albo uczciwie zaznacza brak dowodów.

## 3. Tekst naukowy

Prompt:

```text
Use $stop-slop-pl. Tryb: akademicki. Zachowaj ostrożność:
W badaniu zaobserwowano istotny statystycznie wzrost dokładności klasyfikacji z 81,2% do 84,7% (p = 0,03), co może sugerować, że zastosowana metoda poprawia stabilność modelu.
```

Oczekiwane zachowanie:

- Zachowuje liczby, wartości procentowe i `p = 0,03`.
- Zachowuje odpowiednią ostrożność (hedging).
- Nie zamienia korelacji ani sugestii w pewnik.
- Nie wymusza strony czynnej, jeśli strona bierna lub bezosobowa jest tu właściwa.

## 4. Tekst prawny lub urzędowy

Prompt:

```text
Use $stop-slop-pl. Tryb: urzędowy/prawny. Uprość bez usuwania podstawy prawnej:
Na podstawie art. 15 ust. 2 ustawy z dnia 6 marca 2018 r. przedsiębiorca zobowiązany jest do złożenia oświadczenia w terminie 14 dni od dnia doręczenia wezwania.
```

Oczekiwane zachowanie:

- Zachowuje odwołanie do ustawy i termin 14 dni.
- Upraszcza tam, gdzie się da.
- Nie usuwa mocy prawnej ani wymaganego języka proceduralnego.

## 5. Dopasowanie głosu

Prompt:

```text
Use $stop-slop-pl. Dopasuj głos do próbki.

Próbka głosu:
Piszę krótko. Bez ozdobników. Jeśli coś działa, mówię dlaczego. Jeśli nie działa, też mówię.

Tekst:
Warto zauważyć, że wdrożenie narzędzia może stanowić istotny krok w kierunku zwiększenia efektywności procesów biznesowych.
```

Oczekiwane zachowanie:

- Trzyma krótki, zwięzły rytm.
- Zachowuje sens.
- Usuwa puste wstępy i biznesowe abstrakcje.

## 6. Fragmenty chronione

Prompt:

```text
Use $stop-slop-pl. Zachowaj linki, kod, cytat i liczby:
Warto zauważyć, że endpoint `POST /v1/search` stanowi kluczowy element procesu. Dokumentacja: https://example.com/docs. Cytat: "Model zwrócił 42 wyniki". Wynik wzrósł z 12,4% do 15,1%.
```

Oczekiwane zachowanie:

- Zachowuje bez zmian `POST /v1/search`, URL, cytat i liczby.
- Poprawia tylko polszczyznę dookoła.

## 7. Tylko audyt

Prompt:

```text
Use $stop-slop-pl. Tylko audyt, bez przepisywania:
W obecnych realiach kompleksowe rozwiązania AI odgrywają kluczową rolę w optymalizacji procesów.
```

Oczekiwane zachowanie:

- Nie przepisuje.
- Wypisuje konkretne problemy i ich wagę.
- Wskazuje brak dowodów i konkretnych sprawców.
