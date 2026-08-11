# Scenariusze testów ręcznych

Używaj tych scenariuszy do oceny `$miodkuj` przed publikacją zmian. Nie wymagają jednego wzorcowego brzmienia. Sprawdzają zachowanie, fakty i granice ingerencji.

## 1. Urzędowy język na prosty

Prompt:

```text
Use $miodkuj. Popraw styl i usuń slop po polsku:
W celu dokonania zgłoszenia należy wypełnić niniejszy formularz oraz przekazać go do właściwej komórki organizacyjnej w terminie 7 dni od daty zaistnienia zdarzenia.
```

Protected invariants:

- Zachowaj termin 7 dni i początek jego biegu: data zdarzenia.
- Nie dopisuj sposobu wysyłki ani nazwy komórki.

Expected behavior:

- Zwróć poprawiony tekst jako pierwszy.
- Usuń `w celu`, `dokonania`, `niniejszy` i urzędową mgłę.
- Nazwij działanie czytelnika bez osłabiania terminu.

## 2. Marketingowy slop

Prompt:

```text
Use $miodkuj. Tryb: marketing. Usuń slop:
Nasze innowacyjne i kompleksowe rozwiązanie stanowi kluczowy element transformacji cyfrowej, umożliwiając firmom skuteczne wykorzystanie potencjału danych w dynamicznie zmieniającym się świecie.
```

Protected invariants:

- Tekst nie podaje funkcji produktu, wyników, klientów ani danych liczbowych.
- Nie wolno dopisać żadnego dowodu lub mechanizmu.

Expected behavior:

- Usuń nieuzasadnione przymiotniki i zmniejsz obietnicę.
- Jeśli bez konkretu zdanie pozostaje puste, krótko wskaż, jakiej informacji brakuje.

## 3. Tekst naukowy

Prompt:

```text
Use $miodkuj. Tryb: akademicki. Zachowaj ostrożność:
W badaniu zaobserwowano istotny statystycznie wzrost dokładności klasyfikacji z 81,2% do 84,7% (p = 0,03), co może sugerować, że zastosowana metoda poprawia stabilność modelu.
```

Protected invariants:

- Zachowaj `81,2%`, `84,7%` i `p = 0,03` bez zmiany zapisu.
- Zachowaj ostrożność `może sugerować`; nie zamieniaj sugestii w przyczynowość lub pewnik.

Expected behavior:

- Nie wymuszaj strony czynnej, jeśli forma bezosobowa pasuje do rejestru metod i wyników.
- Usuń tylko rzeczywiste przeciążenie, jeśli je znajdziesz.

## 4. Tekst prawny lub urzędowy

Prompt:

```text
Use $miodkuj. Tryb: urzędowy/prawny. Uprość bez usuwania podstawy prawnej:
Na podstawie art. 15 ust. 2 ustawy z dnia 6 marca 2018 r. przedsiębiorca zobowiązany jest do złożenia oświadczenia w terminie 14 dni od dnia doręczenia wezwania.
```

Protected invariants:

- Zachowaj `art. 15 ust. 2`, datę ustawy, termin 14 dni i jego początek.
- Zachowaj przedsiębiorcę jako zobowiązaną stronę i obowiązkowy charakter czynności.

Expected behavior:

- Uprość składnię bez przechodzenia na nieokreślone `ty`.
- Nie osłabiaj `zobowiązany jest` do sugestii lub możliwości.

## 5. Dopasowanie głosu

Prompt:

```text
Use $miodkuj. Dopasuj głos do próbki.

Próbka głosu:
Piszę krótko. Bez ozdobników. Jeśli coś działa, mówię dlaczego. Jeśli nie działa, też mówię.

Tekst:
Warto zauważyć, że wdrożenie narzędzia może stanowić istotny krok w kierunku zwiększenia efektywności procesów biznesowych.
```

Protected invariants:

- Nie dopisuj procesu, wyniku ani dowodu, których nie ma w tekście.
- Zachowaj warunkowy charakter twierdzenia.

Expected behavior:

- Użyj krótkiego, rzeczowego rytmu próbki.
- Usuń pusty wstęp i biznesowe abstrakcje bez dodawania sloganów.

## 6. Fragmenty chronione

Prompt:

```text
Use $miodkuj. Zachowaj linki, kod, cytat i liczby:
Warto zauważyć, że endpoint `POST /v1/search` stanowi kluczowy element procesu. Dokumentacja: https://example.com/docs. Cytat: "Model zwrócił 42 wyniki". Wynik wzrósł z 12,4% do 15,1%.
```

Protected invariants:

- Zachowaj dokładnie `POST /v1/search`, URL, pełny cytat, `42`, `12,4%` i `15,1%`.
- Nie zmieniaj adresu ani tekstu wewnątrz cudzysłowu.

Expected behavior:

- Popraw tylko polszczyznę dookoła chronionych fragmentów.
- Nie dodawaj wyjaśnienia, jak działa endpoint.

## 7. Tylko audyt

Prompt:

```text
Use $miodkuj. Tylko audyt, bez przepisywania:
W obecnych realiach kompleksowe rozwiązania AI odgrywają kluczową rolę w optymalizacji procesów.
```

Protected invariants:

- Nie zwracaj przepisanej wersji zdania.
- Nie zgaduj, kto lub co napisało tekst.

Expected behavior:

- Nazwij konkretne wzorce, zacytuj dowody, określ ich wagę i wskaż kierunek poprawki.
- Zauważ brak konkretnego aktora, procesu i dowodu.

## 8. Clean human prose

Prompt:

```text
Use $miodkuj. Popraw tylko to, co naprawdę wymaga poprawy:
W piątek znowu próbowałem skrócić ten raport. Nie wyszło. Za każdym razem usuwałem zdanie, a potem odkrywałem, że bez niego następne nie ma sensu. Może problemem nie jest długość, tylko to, że nadal nie wiem, komu ten raport ma pomóc.
```

Protected invariants:

- Zachowaj pierwszą osobę, piątek, nieudaną próbę i końcową niepewność.
- Zachowaj krótkie `Nie wyszło.` oraz osobisty, lekko szorstki ton.

Expected behavior:

- Dopuszczalny jest tekst bez zmian.
- Nie zamieniaj refleksji w poradę, wniosek zarządczy ani równą serię wypolerowanych zdań.

## 9. Intentional rhetoric

Prompt:

```text
Use $miodkuj. Zachowaj uzasadnioną retorykę:
Mamy trzy problemy: dane są niepełne, definicje się różnią, a raport przychodzi po terminie. To nie spór o słowa, lecz trzy różne wyniki przedstawiane jako jedna liczba.
```

Protected invariants:

- Zachowaj trzy rzeczywiste problemy i kontrast między słowami a różnymi wynikami.
- Nie redukuj triady do dwóch elementów.

Expected behavior:

- Pozostaw triadę i kontrast, bo niosą informację.
- Popraw tylko lokalną niezręczność, jeśli rzeczywiście występuje.

## 10. Quoted watched phrase

Prompt:

```text
Use $miodkuj. Popraw analizę, ale zachowaj cytat:
Autor zaczyna od zdania „Warto podkreślić, że transformacja ma kluczowe znaczenie”, a następnie nie przedstawia żadnego przykładu.
```

Protected invariants:

- Zachowaj dokładnie cytat `„Warto podkreślić, że transformacja ma kluczowe znaczenie”`.
- Zachowaj zarzut braku przykładu.

Expected behavior:

- Nie usuwaj obserwowanych wzorców z cytowanego dowodu.
- Możesz uprościć wyłącznie zdanie otaczające cytat.

## 11. Voice sample with em dash

Prompt:

```text
Use $miodkuj. Dopasuj tekst do próbki, również interpunkcję.

Próbka:
Nie lubię wielkich deklaracji — zwykle przykrywają brak decyzji. Wolę jedno „nie wiem” niż trzy slajdy pewności.

Tekst:
Warto zauważyć, że nowy plan może przynieść istotne korzyści, jednak na obecnym etapie nie dysponujemy danymi potwierdzającymi jego skuteczność.
```

Protected invariants:

- Zachowaj brak danych potwierdzających skuteczność i warunkowy charakter korzyści.
- Nie dopisuj oceny planu ani nowych danych.

Expected behavior:

- Dopasuj bezpośredniość i rytm próbki.
- Nie usuwaj myślnika tylko dlatego, że jest obserwowanym wzorcem; próbka dowodzi, że autor używa go celowo.

## 12. Rough personal voice

Prompt:

```text
Use $miodkuj. Nie wygładzaj mojego tonu:
No dobra, dowieźliśmy. Trochę późno, trochę bokiem, ale działa. I serio nie mam dziś ochoty udawać, że od początku taki był plan :)
```

Protected invariants:

- Zachowaj `No dobra`, `serio`, emotikonę `:)` i przyznanie, że plan nie był taki od początku.
- Nie zmieniaj faktu opóźnienia ani działania rozwiązania.

Expected behavior:

- Zostaw rozpoznawalną potoczność, humor i nierówny rytm.
- Nie zamieniaj tekstu w formalne podsumowanie projektu.

## 13. Marketing without evidence

Prompt:

```text
Use $miodkuj. Skróć i uczyń wiarygodnym bez wymyślania konkretów:
Każdy dział używa innej definicji klienta premium. To właśnie dane zmieniają zasady gry.
```

Protected invariants:

- Jedynym konkretnym faktem jest to, że działy używają różnych definicji klienta premium.
- Źródło nie podaje skutku, mechanizmu ani wpływu na raporty, sprzedaż, porównywanie danych lub pracę zespołu.
- Nie wolno dopisać żadnej funkcji, liczby, przykładu, opinii klienta ani prawdopodobnego skutku.

Expected behavior:

- Zachowaj pierwszy fakt i usuń lub zmniejsz slogan.
- Nie zastępuj sloganu atrakcyjnym, ale niewspieranym wyjaśnieniem. Jeśli skutek jest potrzebny, nazwij brakujący rodzaj informacji.

## 14. Technical terminology

Prompt:

```text
Use $miodkuj. Popraw dokumentację bez zmiany terminów:
Endpoint `POST /v1/search` wykonuje walidację pola `query`, po czym Search Worker publikuje zdarzenie `search.requested` do kolejki `search-jobs`. Warto zauważyć, że retry policy pozostaje bez zmian w wersji 2.4.1.
```

Protected invariants:

- Zachowaj dokładnie endpoint, `query`, Search Worker, nazwę zdarzenia, kolejkę, `retry policy` i wersję 2.4.1.
- Zachowaj kolejność walidacji i publikacji zdarzenia.

Expected behavior:

- Usuń zbędne `Warto zauważyć`, ale nie tłumacz ani nie rotuj ustalonej terminologii.
- Nie dopisuj parametrów ponawiania.

## 15. Legal duty and obligated party

Prompt:

```text
Use $miodkuj. Uprość wyjaśnienie dla przedsiębiorcy:
Przedsiębiorca składa oświadczenie w terminie 14 dni od doręczenia wezwania. Niezłożenie oświadczenia skutkuje pozostawieniem wniosku bez rozpoznania.
```

Protected invariants:

- Zachowaj przedsiębiorcę jako zobowiązaną stronę, termin 14 dni, moment doręczenia i skutek braku oświadczenia.
- Nie zmieniaj obowiązku w poradę.

Expected behavior:

- Tekst jest już jasny, więc dopuszczalny jest brak zmian.
- Nie przechodź na `masz` ani nie łagodź skutku proceduralnego.

## 16. Academic hedging and non-causal language

Prompt:

```text
Use $miodkuj. Popraw tylko styl:
Zaobserwowana korelacja (r = 0,42; 95% CI: 0,18–0,61) może wynikać ze sposobu doboru próby. Wynik nie pozwala stwierdzić, że interwencja spowodowała zmianę zachowania.
```

Protected invariants:

- Zachowaj `r = 0,42`, przedział `95% CI: 0,18–0,61`, możliwy wpływ doboru próby i brak wniosku przyczynowego.
- Zachowaj myślnik w zapisie przedziału.

Expected behavior:

- Nie zwiększaj pewności ani nie upraszczaj ograniczenia badania.
- Nie traktuj terminów statystycznych i myślnika zakresowego jako slopu.

## 17. Markdown protected structure

Prompt:

````text
Use $miodkuj. Popraw prozę, zachowaj strukturę Markdown:
---
title: "Search API"
version: 2.4.1
---

## 🚀 Wprowadzenie

Warto zauważyć, że endpoint stanowi kluczowy element procesu.

```bash
curl -X POST https://example.com/v1/search
```

| Pole | Wymagane |
| --- | --- |
| `query` | tak |
````

Protected invariants:

- Zachowaj cały frontmatter, wersję, URL, blok kodu, tabelę i `query` znak w znak.
- Nie zmieniaj celu endpointu, którego źródło nie wyjaśnia.

Expected behavior:

- Usuń dekoracyjną emoji i pustą ocenę ważności.
- Zachowaj poprawną strukturę dokumentu i nie wymyślaj opisu endpointu.

## 18. Audit without authorship inference

Prompt:

```text
Use $miodkuj. Oceń, co brzmi sztucznie, ale nie oceniaj autorstwa i nie przepisuj:
Oto czego nikt ci nie mówi: prawdziwa innowacja nie polega na narzędziach. Polega na odwadze. Dane są walutą przyszłości.
```

Protected invariants:

- Nie zwracaj wersji po redakcji.
- Nie używaj stwierdzeń `napisało to AI`, `tekst jest wygenerowany` ani prawdopodobieństwa autorstwa.

Expected behavior:

- Nazwij faux insight, kontrast redefinicyjny i fake-profound kicker, cytując odpowiednie fragmenty.
- Podaj kierunek poprawki dla każdego materialnego wzorca.

## 19. Long-form coverage

Prompt:

```text
Use $miodkuj. Zredaguj całość bez utraty faktów:
Projekt rozpoczął się 3 marca 2026 r. Zespół miał sześć tygodni i budżet 180 000 zł. W obecnych realiach kluczowym wyzwaniem okazała się integracja danych.

Pierwszy test objął 42 konsultantów. Średni czas odpowiedzi spadł z 18 do 11 minut, ale liczba ponownych kontaktów nie zmieniła się. Wynik może zależeć od tego, że test trwał tylko 14 dni.

Podsumowując, rozwiązanie ma ogromny potencjał i będzie odgrywać coraz większą rolę. Zarząd zdecyduje o drugim teście 30 kwietnia 2026 r.
```

Protected invariants:

- Zachowaj wszystkie daty, sześć tygodni, 180 000 zł, 42 konsultantów, spadek z 18 do 11 minut, brak zmiany ponownych kontaktów i 14-dniowe ograniczenie.
- Zachowaj niepewność dotyczącą krótkiego testu i decyzję zarządu 30 kwietnia 2026 r.

Expected behavior:

- Usuń ogólnikowe otwarcie i zakończenie, nie gubiąc żadnego twierdzenia.
- Możesz połączyć lub podzielić akapity, jeśli pełne pokrycie informacji i kolejność zdarzeń pozostają czytelne.
