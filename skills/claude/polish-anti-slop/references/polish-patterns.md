# Polish Slop Patterns

Use these as cluster-sensitive signals. Most items are not absolute bans.

## Chatbot Residue

Red flags:

- `jako model językowy`
- `nie mam dostępu do`
- `moja wiedza kończy się`
- `mogę pomóc w`
- `oto poprawiona wersja`
- `mam nadzieję, że to pomoże`
- explaining the task instead of doing it

Fix:

- Remove interface chatter.
- Return the finished text.
- Keep notes separate from the rewrite.

## Throat-Clearing

Watchlist:

- `warto zauważyć`
- `należy podkreślić`
- `trzeba zaznaczyć`
- `nie sposób nie wspomnieć`
- `co istotne`
- `ważne jest, aby`
- `w dzisiejszych czasach`
- `w obecnych realiach`
- `w dynamicznie zmieniającym się świecie`
- `w erze sztucznej inteligencji`
- `w dobie cyfryzacji`

Fix:

- Start with the claim, action, fact, or consequence.
- Delete any opener that can disappear without changing meaning.

## Inflated Importance

Watchlist:

- `kluczowy`
- `istotny`
- `znaczący`
- `fundamentalny`
- `strategiczny`
- `kompleksowy`
- `przełomowy`
- `unikalny`
- `niezwykle ważny`
- `wielowymiarowy`
- `holistyczny`
- `innowacyjny`
- `nowoczesny`
- `skuteczny`

Fix:

- Replace adjective with evidence: number, user, deadline, risk, cost, result, comparison.
- If evidence is missing, make the claim smaller.

## Officialese

Watchlist:

- `niniejszy`
- `celem`
- `w celu`
- `w ramach`
- `w zakresie`
- `w przypadku`
- `z uwagi na`
- `na skutek`
- `w związku z powyższym`
- `dokonać`
- `dokonywać`
- `realizować działania`
- `podejmować działania`
- `ulec poprawie`
- `ulec pogorszeniu`
- `posiadać możliwość`
- `w miesiącu maju`
- `w dniu dzisiejszym`

Common replacements:

- `niniejszy` -> `ten`
- `celem` -> `aby` or `żeby`
- `w dniu dzisiejszym` -> `dzisiaj`
- `w miesiącu maju` -> `w maju`
- `dokonać zakupu` -> `kupić`
- `ulec pogorszeniu` -> `pogorszyć się`
- `posiadać możliwość` -> `może`

## Nominalizations

Signals:

- endings: `-anie`, `-enie`, `-cie`
- `wdrożenie rozwiązania`
- `realizacja działań`
- `dokonanie zmiany`
- `przeprowadzenie analizy`
- `podjęcie decyzji`
- `zwiększenie efektywności`
- `zapewnienie możliwości`

Fix:

- Prefer actor plus finite verb:
  - `przeprowadzenie analizy danych` -> `zespół przeanalizował dane`
  - `podjęcie decyzji nastąpiło` -> `rada zdecydowała`
  - `realizacja działań` -> `robimy`, `zrobiliśmy`, `urząd zrobi`

Keep:

- terms of art,
- legal labels,
- official procedure names,
- scientific terms,
- headings where the noun form is natural.

## Passive And Impersonal Fog

Watchlist:

- `zostało wykonane`
- `jest realizowane`
- `został opracowany`
- `dokonano`
- `ustalono`
- `przyjęto`
- `wskazano`
- `należy`
- `powinno się`
- `można zauważyć`

Fix:

- Name the actor when useful:
  - `zostało opracowane narzędzie` -> `zespół opracował narzędzie`
  - `dokonano zmiany` -> `zmieniliśmy`
  - `należy złożyć wniosek` -> `złóż wniosek`

Keep:

- legal text,
- official notices,
- academic methods,
- cases where actor is irrelevant or unknown.

## Genitive Chains

Signals:

- stacked nouns in dopełniacz,
- unclear ownership or relation,
- phrases like `w przypadku braku możliwości uruchomienia pojazdu`.

Fix:

- Convert the chain into a clause:
  - `w przypadku braku możliwości uruchomienia pojazdu` -> `jeśli nie możesz uruchomić pojazdu`
  - `analiza wyników badania satysfakcji klientów` -> `przeanalizowaliśmy, jak klienci ocenili usługę`

## Participial Heaviness

Watchlist:

- `mając na uwadze`
- `biorąc pod uwagę`
- `uwzględniając`
- `dotyczący`
- `obejmujący`
- `stanowiący`
- `wskazujący`
- `umożliwiający`
- `pozwalający`
- `korzystając z`

Fix:

- Convert to shorter clauses.
- Put the action in a finite verb.

## Formulaic AI Structures

Watchlist:

- `nie tylko X, ale także Y`
- `to nie X, lecz Y`
- `z jednej strony... z drugiej strony...`
- `zarówno X, jak i Y`
- `od X po Y`
- `X stanowi Y`
- `X wpisuje się w szerszy trend`
- `X pokazuje, jak ważne jest Y`
- `X odzwierciedla potrzebę Y`
- `X jest przykładem tego, jak Y`

Fix:

- Keep contrast only if it carries a real distinction.
- Replace generic synthesis with actual consequence.
- Avoid balanced pairs unless the text genuinely compares two sides.

## Generic Endings

Watchlist:

- `podsumowując`
- `można stwierdzić`
- `czas pokaże`
- `przyszłość pokaże`
- `to krok w dobrym kierunku`
- `ma ogromny potencjał`
- `będzie odgrywać coraz większą rolę`
- `warto śledzić rozwój sytuacji`

Fix:

- End with a concrete next step, implication, unresolved tension, or crisp final claim.
- In public-service text, end with the action the reader should take.

## Generic Specificity

Watch for:

- `interesariusze`, `użytkownicy`, `organizacje`, `rozwiązania`, `procesy`, `wyzwania`, `obszary`, `aspekty`,
- claims without dates, names, examples, measurements, constraints, tradeoffs, or consequences,
- paragraphs that could apply to any company, ministry, project, or product.

Fix:

- Ask: who, when, where, how much, compared with what, what changed, who cares, what breaks if ignored?
- Add only known facts. If facts are missing, make the sentence honest instead of invented.
