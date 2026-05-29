# Manual Test Scenarios

Use these scenarios to validate `$polish-anti-slop` before publishing changes.

## 1. Officialese To Plain Polish

Prompt:

```text
Use $polish-anti-slop to odslopuj ten tekst po polsku:
W celu dokonania zgłoszenia należy wypełnić niniejszy formularz oraz przekazać go do właściwej komórki organizacyjnej w terminie 7 dni od daty zaistnienia zdarzenia.
```

Expected behavior:

- Return revised text first.
- Use direct public-facing Polish.
- Preserve the 7-day deadline.
- Remove `w celu`, `dokonania`, `niniejszy`, and institutional fog.

## 2. Marketing Slop

Prompt:

```text
Use $polish-anti-slop. Tryb: marketing. Usuń AI-owy styl:
Nasze innowacyjne i kompleksowe rozwiązanie stanowi kluczowy element transformacji cyfrowej, umożliwiając firmom skuteczne wykorzystanie potencjału danych w dynamicznie zmieniającym się świecie.
```

Expected behavior:

- Cut unsupported adjectives.
- Avoid inventing proof.
- Make the claim concrete or honestly mark missing evidence.

## 3. Academic Polish

Prompt:

```text
Use $polish-anti-slop. Tryb: akademicki. Zachowaj ostrożność:
W badaniu zaobserwowano istotny statystycznie wzrost dokładności klasyfikacji z 81,2% do 84,7% (p = 0,03), co może sugerować, że zastosowana metoda poprawia stabilność modelu.
```

Expected behavior:

- Preserve numbers, percentage values, and `p = 0,03`.
- Preserve appropriate hedging.
- Do not turn correlation or suggestion into certainty.
- Do not force active voice if passive/impersonal style is acceptable.

## 4. Legal Or Official Text

Prompt:

```text
Use $polish-anti-slop. Tryb: urzędowy/prawny. Uprość bez usuwania podstawy prawnej:
Na podstawie art. 15 ust. 2 ustawy z dnia 6 marca 2018 r. przedsiębiorca zobowiązany jest do złożenia oświadczenia w terminie 14 dni od dnia doręczenia wezwania.
```

Expected behavior:

- Preserve statute reference and 14-day deadline.
- Clarify where possible.
- Do not remove legal force or required procedural language.

## 5. Voice Match

Prompt:

```text
Use $polish-anti-slop. Dopasuj głos do próbki.

Próbka głosu:
Piszę krótko. Bez ozdobników. Jeśli coś działa, mówię dlaczego. Jeśli nie działa, też mówię.

Tekst:
Warto zauważyć, że wdrożenie narzędzia może stanowić istotny krok w kierunku zwiększenia efektywności procesów biznesowych.
```

Expected behavior:

- Match short, blunt rhythm.
- Keep meaning.
- Remove throat-clearing and business abstractions.

## 6. Protected Spans

Prompt:

```text
Use $polish-anti-slop. Zachowaj linki, kod, cytat i liczby:
Warto zauważyć, że endpoint `POST /v1/search` stanowi kluczowy element procesu. Dokumentacja: https://example.com/docs. Cytat: "Model zwrócił 42 wyniki". Wynik wzrósł z 12,4% do 15,1%.
```

Expected behavior:

- Preserve `POST /v1/search`, URL, quoted text, and numbers exactly.
- Improve surrounding Polish only.

## 7. Audit Only

Prompt:

```text
Use $polish-anti-slop. Tylko audyt, bez przepisywania:
W obecnych realiach kompleksowe rozwiązania AI odgrywają kluczową rolę w optymalizacji procesów.
```

Expected behavior:

- Do not rewrite.
- List concrete issues and severity.
- Mention missing proof/concrete actors.
