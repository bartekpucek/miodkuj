# Podsumowanie researchu

Stop Slop PL nie tłumaczy angielskich list zakazanych słów. Dostosowuje wzorce anti-slop do polszczyzny, ale traktuje je jako wskazówki redakcyjne, a nie dowód autorstwa.

## Co łączy zewnętrzne skille

Najlepsze skille anti-slop (m.in. `hardikpandya/stop-slop`, `blader/humanizer`, `slopbuster`, `de-slop` i `deslopify`) zgadzają się co do kilku rzeczy:

- Listy wzorców pomagają, ale dobra redakcja zmienia tylko fragmenty, które rzeczywiście tego wymagają.
- Sens, fakty, liczby, cytaty, linki i przytoczenia trzeba zachować.
- Pojedyncze „zakazane" słowa to słaby sygnał. Liczy się ich nagromadzenie.
- Głos i rejestr ważą więcej niż ogólna „humanizacja".
- Druga tura audytu wyłapuje to, co zostało po pierwszym przejściu.
- Wyjątki gatunkowe chronią przed przesadną korektą.
- Nie obiecujemy obejścia wykrywaczy AI.

## Wybrana architektura

Wersja 1.1 pozostaje lekkim edytorem opartym na instrukcji i referencjach. Najpierw rozpoznaje zadanie, rejestr i kilka cech głosu autora. Potem robi najmniejszą skuteczną zmianę, a na końcu przechodzi binarną kontrolę wierności, głosu i trybu odpowiedzi.

Nie dodajemy deterministycznego lintera do rdzenia. Taki linter pomaga przy pracy wsadowej, lecz sama lista dopasowań nie rozstrzyga kontekstu i nie chroni głosu autora. Pełny audyt gramatyki, terminologii i anglicyzmów również pozostaje poza zakresem tego skilla.

## Adaptacja do polszczyzny

Polski slop najczęściej wygląda tak:

- urzędowe zwroty: `niniejszy`, `celem`, `w ramach`, `w zakresie`,
- rzeczowniki odczasownikowe: `dokonanie`, `wdrożenie`, `przeprowadzenie`, `realizacja działań`,
- strona bierna i formy bezosobowe: `zostało wykonane`, `dokonano`, `ustalono`, `należy`,
- łańcuchy dopełniaczy: `w przypadku braku możliwości uruchomienia pojazdu`,
- puste przymiotniki: `kluczowy`, `fundamentalny`, `kompleksowy`, `przełomowy`,
- schematyczne konstrukcje: `nie tylko X, ale także Y`, `z jednej strony... z drugiej strony...`,
- ogólnikowe zakończenia: `podsumowując`, `przyszłość pokaże`, `warto śledzić rozwój sytuacji`.

Skill korzysta z wytycznych prostego języka z Gov.pl i sygnałów czytelności w stylu Jasnopisu: krótkie zdania w tekstach dla szerokiego odbiorcy, sprawcy i czasowniki, bezpośrednia perspektywa czytelnika, mniej łańcuchów rzeczownikowych, mniej strony biernej, mniej imiesłowów i mniej abstrakcyjnego słownictwa.

## Kontekst polskich modeli (LLM)

PLLuM i Bielik pokazują, dlaczego instrukcje pod polszczyznę mają znaczenie. To dobre punkty odniesienia dla jakości polskiego i stylu promptów, ale nie zastępują redakcyjnych zabezpieczeń. Dlatego skill traktuje polskie modele jako możliwych pomocników, nie źródła prawdy.

## Granica

Stop Slop PL poprawia jasność, konkret, dopasowanie rejestru i głos. Nie obiecuje obejścia wykrywaczy AI ani „niewykrywalnego" tekstu.

Audyt wskazuje nazwane wzorce i cytuje dowody z tekstu. Nie orzeka, czy tekst napisał człowiek, model ani konkretny system.
