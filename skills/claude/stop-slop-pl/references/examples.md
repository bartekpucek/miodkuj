# Polish Before And After Examples

## Contents

- Officialese, generic introductions, nominalizations, and passive forms
- Fake synthesis and unsupported marketing claims
- Voice matching and protected spans
- Portability, synonym cycling, fake-profound endings, and second-hand phrases

## Officialese

Before:

> W celu dokonania zgłoszenia należy wypełnić niniejszy formularz.

After:

> Wypełnij ten formularz, żeby zgłosić sprawę.

## Generic AI Intro

Before:

> W dzisiejszym dynamicznie zmieniającym się świecie sztuczna inteligencja odgrywa coraz ważniejszą rolę w wielu obszarach życia.

After:

> Coraz więcej firm używa AI do obsługi klientów, analizy dokumentów i pisania kodu.

## Nominalization

Before:

> Przeprowadzenie analizy danych umożliwiło identyfikację kluczowych obszarów wymagających optymalizacji.

After:

> Po analizie danych znaleźliśmy trzy miejsca, w których system traci najwięcej czasu.

Only use a specific result if the source text gives it. If facts are missing:

> Analiza danych pokazała, gdzie system działa najwolniej.

## Passive

Before:

> Decyzja została podjęta po uwzględnieniu opinii użytkowników.

After, actor known:

> Zespół zdecydował po rozmowach z użytkownikami.

After, actor unknown or irrelevant:

> Decyzję podjęto po konsultacjach z użytkownikami.

## Fake Synthesis

Before:

> Wyniki badania pokazują, jak ważne jest holistyczne podejście do transformacji cyfrowej.

After, fact known:

> Firmy, które najpierw uporządkowały dane, wdrażały nowe narzędzia średnio dwa miesiące szybciej.

After, fact not known:

> Badanie nie wskazuje jednego narzędzia. Pokazuje raczej, że firmy najpierw muszą uporządkować dane.

## Marketing Claim Without Proof

Before:

> Nasze kompleksowe rozwiązanie stanowi kluczowy element skutecznej transformacji cyfrowej.

After:

> Nasze narzędzie porządkuje dane, automatyzuje raporty i pokazuje zespołowi, gdzie projekt traci czas.

If those functions are not stated in the source, do not invent them:

> Nasze narzędzie ma wspierać transformację cyfrową. Tekst potrzebuje konkretu: co dokładnie robi i dla kogo?

## Voice Match

Sample:

> Piszę krótko. Bez ozdobników. Jeśli coś działa, mówię dlaczego. Jeśli nie działa, też mówię.

Before:

> Warto zauważyć, że wdrożenie narzędzia może stanowić istotny krok w kierunku zwiększenia efektywności procesów biznesowych.

After:

> To narzędzie może przyspieszyć pracę. Ale tylko jeśli wiemy, który proces ma naprawić.

## Protected Spans

Before:

> Warto zauważyć, że endpoint `POST /v1/search` stanowi kluczowy element procesu. Dokumentacja: https://example.com/docs. Cytat: "Model zwrócił 42 wyniki".

After:

> Endpoint `POST /v1/search` obsługuje ten proces. Dokumentacja: https://example.com/docs. Cytat: "Model zwrócił 42 wyniki".

## Portability Test

Before:

> W dynamicznie zmieniającym się otoczeniu organizacje muszą elastycznie odpowiadać na nowe wyzwania.

After, no supporting detail available:

> Organizacje muszą elastycznie odpowiadać na zmiany. Tekst potrzebuje konkretu: jakie zmiany i na czym ma polegać elastyczna odpowiedź?

The original sentence could describe almost any organization. Make it smaller or ask for the missing detail; do not invent one.

## Synonym Cycling

Before:

> Agent analizuje zgłoszenie. Asystent wybiera kategorię. Następnie narzędzie przekazuje sprawę konsultantowi.

After:

> Agent analizuje zgłoszenie, wybiera kategorię i przekazuje sprawę konsultantowi.

Repeat a stable term when it names the same thing.

## Fake-Profound Ending

Before:

> Zespół nadal używa trzech definicji aktywnego klienta. Dane są walutą przyszłości.

After:

> Zespół nadal używa trzech definicji aktywnego klienta.

Use a source-supported consequence instead of a generic aphorism. Here the source does not give one, so the edit ends on the first sentence.

## Second-Hand Phrase

Before:

> W prezentacji pada zdanie „Warto podkreślić, że AI odgrywa kluczową rolę”. To jedyne uzasadnienie inwestycji.

After:

> W prezentacji pada zdanie „Warto podkreślić, że AI odgrywa kluczową rolę”, ale to jedyne uzasadnienie inwestycji.

Keep the quoted wording exact and edit only the surrounding analysis.
