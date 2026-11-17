# Polish Slop Patterns

A listed word or construction marks a place to look, not a defect.

- **Cut on sight** sections (chatbot residue, throat-clearing, redundant officialese, generic endings): the wording goes and nothing is lost.
- **Every other section** lists ordinary Polish that is slop only when empty or piled up. A sentence where the listed wording carries real content stays verbatim, even if its neighbours are edited. If a cut leaves the next sentence with no grammatical subject, add that one word to it and change nothing else. `Keep when` and `False-positive guard` lines name the common cases.

## Chatbot Residue

Cut on sight: `jako model językowy`, `nie mam dostępu do`, `moja wiedza kończy się`, `mogę pomóc w`, `oto poprawiona wersja`, `mam nadzieję, że to pomoże`, and any explanation of the task in place of the task.

Fix: remove the interface chatter and return the finished text. Keep notes separate from the rewrite.

## Throat-Clearing

Cut on sight:

- weight announcers: `warto zauważyć`, `należy podkreślić`, `trzeba zaznaczyć`, `nie sposób nie wspomnieć`, `co istotne`, `ważne jest, aby`,
- stock settings: `w dzisiejszych czasach`, `w obecnych realiach`, `w dynamicznie zmieniającym się świecie`, `w erze sztucznej inteligencji`, `w dobie cyfryzacji`.

Fix: start with the claim, action, fact, or consequence. Delete the opener when the sentence means the same without it.

## Inflated Importance

Watchlist: `kluczowy`, `istotny`, `znaczący`, `fundamentalny`, `strategiczny`, `kompleksowy`, `przełomowy`, `unikalny`, `niezwykle ważny`, `wielowymiarowy`, `holistyczny`, `innowacyjny`, `nowoczesny`, `skuteczny`.

Edit when the adjective stands in for missing evidence: replace it with a number, user, deadline, risk, cost, result, or comparison from the source, or make the claim smaller.

## Officialese

Cut on sight:

- `niniejszy` -> `ten`
- `celem`, `w celu` + verbal noun -> `aby`, `żeby` + verb
- `w dniu dzisiejszym` -> `dzisiaj`; `w dniu 3 marca` -> `3 marca`; `w miesiącu maju` -> `w maju`
- `dokonać zakupu` -> `kupić`; `realizować działania`, `podejmować działania` -> the action's verb
- `ulec pogorszeniu` -> `pogorszyć się`; `posiadać możliwość` -> `może`
- `w związku z powyższym` -> `dlatego`, or cut

Judge in context: `w ramach`, `w zakresie`, `w przypadku`, `z uwagi na`, `na skutek`.

Edit when the phrase heads a noun chain (see Genitive Chains) or can go with nothing lost: `w ramach realizacji projektu` -> `w projekcie`.

Keep when one noun follows and names a real scope, condition, or cause: `w ramach umowy serwisowej`, `w przypadku awarii`. It stays as written; `podczas`, `jeśli`, or `w razie` in its place is a synonym swap, not a fix.

## Nominalizations

Signals: verbal nouns in `-anie`, `-enie`, `-cie` carrying the action: `wdrożenie rozwiązania`, `realizacja działań`, `przeprowadzenie analizy`, `podjęcie decyzji`, `zapewnienie możliwości`.

Fix: prefer a finite verb. Name the actor only if the source names one; otherwise use an impersonal form:

- `przeprowadzenie analizy danych` -> `przeanalizowano dane`
- `podjęcie decyzji nastąpiło` -> `podjęto decyzję`

Keep when the noun is a term of art, legal label, official procedure name, scientific term, or a heading where the noun form is natural.

## Passive And Impersonal Fog

Watchlist: `zostało wykonane`, `jest realizowane`, `został opracowany`, `dokonano` + noun, `można zauważyć`, `powinno się`.

Fix: use the shorter form without inventing an actor.

- `zostało opracowane narzędzie` -> `opracowano narzędzie`
- `dokonano zmiany` -> `zmieniono`
- actor named in the same sentence: `raport został przygotowany przez dział finansów` -> `raport przygotował dział finansów`

Keep when:

- the verb is already a plain impersonal form (`opracowano`, `wymieniono`): that is the fix, not the fog,
- an impersonal verb reports a finding or decision (`stwierdzono, że`, `przyjęto, że`): deleting it turns the finding into a bare fact, and giving it a subject (`stwierdziliśmy`, `zespół przyjął`) names an actor the source does not,
- the sentence names no actor: one named in a neighbouring sentence is not evidence,
- the text is legal, an official notice, or an academic method section.

## Genitive Chains

Signals: three or more stacked nouns in the genitive, with unclear ownership or relation.

Fix: convert the chain into a clause: `w przypadku braku możliwości uruchomienia pojazdu` -> `jeśli nie możesz uruchomić pojazdu`.

## Participial Heaviness

Watchlist: `mając na uwadze`, `biorąc pod uwagę`, `uwzględniając`, `dotyczący`, `obejmujący`, `stanowiący`, `wskazujący`, `umożliwiający`, `pozwalający`, `korzystając z`.

Edit when participles stack in one sentence or delay its verb: convert them to clauses with a finite verb.

## Translated Word Choices And Register

Watch for:

- a translated metaphor that makes a practical statement sound abstract or bookish,
- a translation that selects the wrong sense of a word for the supplied situation,
- a grammatically correct Polish expression whose register does not fit the text's job or the writer's voice.

Problem:

- An established Polish expression can still be an awkward choice in context. In a plain travel itinerary, `środek ciężkości` can obscure the trip's main focus. In accommodation advice for a short visit, `zatrzymaj się` usually fits `stay` better than `zamieszkaj`. These are contextual editing decisions, not proof that either Polish expression is incorrect or that AI wrote the text.

Fix:

- Express the intended relationship in Polish appropriate to the situation. Do not replace every instance of an English word or Polish phrase with one fixed equivalent.
- If the source identifies only a trip's main focus, name that focus directly. Calling it a base, a place to sleep, or the place where most days are spent adds logistics the source has not supplied. This also applies to suggested fixes in audit mode.
- When an original and a translation are supplied for comparison, preserve the original's constraints as well as its main point. Practical feasibility is stronger than theoretical reachability; a day trip is not an unrestricted excursion. `Without driving` does not exclude travelling as a passenger.
- If only the Polish draft is supplied, or the original is truncated, do not reconstruct missing context or add itinerary details. See `examples.md` for the Edinburgh and accommodation cases.

False-positive guard: Preserve literal technical meanings, established figurative uses that fit the register, deliberate metaphors supported by the writer's voice, and protected quotations. `Środek ciężkości` is legitimate in both physics and figurative Polish. `Zamieszkać` can describe residence or temporary accommodation; it does not always imply permanence. For `stay` meaning remain in place, use the corresponding sense, such as `zostań`, rather than accommodation wording.

Keep business and IT working vocabulary as written, even where a style guide would call it an anglicism or a calque: borrowed words (`deploy`, `onboarding`, `feedback`), Polish words in a business sense taken from English (`dedykowany`, `adresować problem`), and set phrases (`na koniec dnia`). The writer and their readers use these daily. A purer Polish replacement is a style preference, and it can shift the meaning.

## Formulaic AI Structures

Watchlist: `nie tylko X, ale także Y`; `to nie X, lecz Y`; `z jednej strony... z drugiej strony...`; `zarówno X, jak i Y`; `od X po Y`; `X stanowi Y`; `X wpisuje się w szerszy trend`; `X pokazuje, jak ważne jest Y`; `X odzwierciedla potrzebę Y`; `X jest przykładem tego, jak Y`.

Edit when one side of the pair is filler or the synthesis is generic: state the real side directly, or give the consequence the source supplies.

Keep when both sides are stated facts or named things: `z jednej strony tańszy o 200 zł, z drugiej wolniejszy o 20%`; `zarówno kierowca, jak i pasażerowie`. The connector stays as written; `ale` or `jednak` in its place is a synonym swap, not a fix.

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

False-positive guard: This is a preservation rule. It does not protect unattributed prose merely because it uses quotation marks decoratively; determine whether the words are genuinely cited, named, or discussed.

## Dashes

Signals: several dashes in one paragraph; a dash where a comma, colon, or full stop is the ordinary mark; a dash staging a reveal.

Fix: use the ordinary mark or split the sentence. Add a connector dash only when a supplied voice sample uses one.

Keep a source dash that does a standard Polish job: marking an omitted element (`Ojciec czytał gazetę, matka — książkę`), standing for `jest` or `są` before `to` (`Wiedza — to potęga`), or setting off one insertion or a line of dialogue.

## Generic Endings

Cut on sight: `podsumowując`, `można stwierdzić`, `czas pokaże`, `przyszłość pokaże`, `to krok w dobrym kierunku`, `ma ogromny potencjał`, `będzie odgrywać coraz większą rolę`, `warto śledzić rozwój sytuacji`.

Fix: end on the last concrete fact, next step, implication, or unresolved tension the source gives. In public-service text, end with the action the reader should take.

## Generic Specificity

Watch for bare `interesariusze`, `użytkownicy`, `organizacje`, `rozwiązania`, `procesy`, `wyzwania`, `obszary`, `aspekty`, and claims without dates, names, examples, measurements, constraints, tradeoffs, or consequences.

Fix: ask who, when, where, how much, compared with what, what changed, and what breaks if ignored. Add only known facts; if they are missing, make the sentence honest instead of invented.
