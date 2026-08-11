# Polish Slop Patterns

Use these as cluster-sensitive signals. Most items are not absolute bans.

## Contents

- Chatbot residue, throat-clearing, and inflated importance
- Officialese, nominalizations, passive fog, genitive chains, and participial heaviness
- Formulaic structures, faux insight, metadiscourse, colon reveals, and negative listing
- Synonym cycling, fake-profound endings, formatting slop, and second-hand text
- Em dashes, generic endings, and generic specificity

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

## Faux Insight And Exclusivity

Watchlist:

- `oto czego nikt ci nie mówi`
- `większość ludzi nie rozumie`
- `najczęściej pomijany element`
- `to część, której wszyscy nie dostrzegają`
- `prawdziwy problem polega na tym`

Problem:

- The setup presents an ordinary claim as hidden knowledge and flatters the writer or reader as part of an informed minority.

Fix:

- Remove the exclusivity claim and state the substantive point.

Before:

> Oto czego większość firm nie rozumie: dane są prawdziwą przewagą.

After:

> Dane są przewagą firmy.

False-positive guard: Keep the construction when the text can identify a specific, evidenced misconception held by a defined group. Do not infer that evidence from the setup itself.

## Interpretive Metadiscourse

Watchlist:

- `ten punkt jest ważniejszy, niż się wydaje`
- `jak widać`
- `warto zwrócić uwagę na to, że`
- `innymi słowy` followed by a repetition
- `to rozróżnienie ma kluczowe znaczenie`

Problem:

- The prose steps outside the subject to tell the reader how much weight to give a claim instead of supplying the reason.

Fix:

- Delete the instruction when the point is already clear. Otherwise replace it with the source-grounded consequence.

Before:

> Ten punkt jest ważniejszy, niż się wydaje. Zespół nie ma jednej definicji aktywnego klienta.

After:

> Zespół nie ma jednej definicji aktywnego klienta.

False-positive guard: Keep genuine signposting in long, technical, legal, or academic arguments when it helps readers navigate a real distinction. Remove only commentary that adds no reasoning.

## Colon Reveals

Watchlist:

- a short evaluative label followed by a colon and a dramatic reveal,
- `najważniejsze:`, `najlepsze:`, `wniosek:`, `sekret:` used as a hook rather than a label.

Problem:

- The colon manufactures a reveal where an ordinary sentence would be clearer.

Fix:

- Turn the label and reveal into a direct sentence.

Before:

> Największa zmiana: system uczy się sam.

After:

> Największą zmianą jest to, że system uczy się sam.

False-positive guard: Keep colons for lists, definitions, quotations, UI labels, headings, and concise summaries where the text after the colon genuinely specifies the label.

## Negative Listing

Watchlist:

- `Nie X. Nie Y. Z.`
- several consecutive negated fragments followed by a positive label,
- clipped rejections used to build a slogan.

Problem:

- Stacked negations manufacture force while delaying the actual claim.

Fix:

- State the positive claim and keep only a contrast that changes its meaning.

Before:

> Nie raport. Nie dashboard. System decyzji.

After:

> To system decyzji, a nie raport ani dashboard.

False-positive guard: Keep a short negative series in dialogue, literary prose, political rhetoric, or a voice sample when its cadence is deliberate and distinctive rather than repeated throughout the text.

## Synonym Cycling

Watch for:

- changing `agent`, `asystent`, `narzędzie`, and `system` while referring to the same product,
- rotating `firma`, `organizacja`, `przedsiębiorstwo`, and `podmiot` only to avoid repetition,
- unclear pronouns introduced by unnecessary variation.

Problem:

- Forced variation makes terminology unstable and can suggest distinctions that do not exist.

Fix:

- Repeat the clearest established term. Use a different term only for a different concept.

Before:

> Agent porządkuje zgłoszenia. Asystent przypisuje priorytety. Następnie narzędzie przekazuje sprawy zespołowi.

After:

> Agent porządkuje zgłoszenia, przypisuje im priorytety i przekazuje sprawy zespołowi.

False-positive guard: Keep distinct terms when the source defines distinct components, legal roles, system layers, or actors. Precision outranks stylistic repetition.

## Fake-Profound Kickers And Aphorisms

Watchlist:

- `dane są walutą przyszłości`
- `X jest językiem Y`
- `X staje się lustrem Y`
- `przyszłość nie czeka`
- a final metaphor or mic-drop sentence that adds no consequence or action.

Problem:

- The ending converts an ordinary point into a reusable slogan and often replaces the actual implication.

Fix:

- Delete the kicker and end on the last concrete fact, unresolved tension, decision, or next action already supported by the source.

Before:

> Zespół nadal używa trzech definicji aktywnego klienta. Dane są walutą przyszłości.

After:

> Zespół nadal używa trzech definicji aktywnego klienta.

False-positive guard: Keep a metaphor when it is original, developed by the author, and carries reasoning that plain paraphrase would lose. A familiar phrase alone is not enough.

## Formatting Slop

Watch for:

- emoji decorating headings or bullets,
- bold applied to routine phrases mid-sentence,
- many headings over one- or two-sentence sections,
- a bullet list that hides a simple relationship better expressed in prose.

Problem:

- Formatting performs importance and fragments the argument instead of clarifying its structure.

Fix:

- Keep headings for real sections, bold for genuine scanning needs, and lists for parallel items. Merge decorative fragments into prose.

Before:

> ## 🚀 **Wdrożenie**
>
> ### **Start**
>
> Zaczynamy w maju. Pilotaż obejmie dział sprzedaży.
>
> ### **Zakres**
>
> Najpierw uruchomimy raportowanie. Integracje poczekają.
>
> ### **Decyzja**
>
> Ania zatwierdzi harmonogram. Zespół wdrożeniowy rozpocznie prace po akceptacji.

After:

> ## Wdrożenie
>
> Zaczynamy w maju od pilotażu w dziale sprzedaży. Najpierw uruchomimy raportowanie; integracje poczekają. Po zatwierdzeniu harmonogramu przez Anię zespół wdrożeniowy rozpocznie prace.

False-positive guard: Keep required brand formatting, accessibility-oriented structure, UI copy conventions, checklists, comparison tables, and user-requested Markdown.

## Second-Hand Text Guard

Watch for:

- watched phrases inside quotations, titles, proper names, code, examples, or passages that discuss the phrase itself,
- an edit that silently changes a cited speaker's wording.

Problem:

- Pattern matching without scope awareness corrupts evidence and protected text.

Fix:

- Leave second-hand text exact. Edit only the surrounding prose unless the user explicitly asks to alter the quotation or example.

Before:

> Autor zaczyna od zdania „Warto podkreślić, że transformacja ma kluczowe znaczenie”, a potem nie podaje żadnego przykładu.

After:

> Autor zaczyna od zdania „Warto podkreślić, że transformacja ma kluczowe znaczenie”, ale nie podaje żadnego przykładu.

False-positive guard: This is a preservation rule. It does not protect unattributed prose merely because it uses quotation marks decoratively; determine whether the words are genuinely cited, named, or discussed.

## Em Dashes

Signals:

- an em dash used as a default connector between clauses,
- several em dashes in one paragraph,
- an em dash standing in for a comma, colon, or full stop.

Fix:

- Replace the em dash with a comma, colon, or full stop, or split the sentence.
- Prefer shorter finite Polish sentences over dash-joined clauses.
- Keep a dash only where Polish genuinely needs it, such as dialogue or a clear apposition.

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
