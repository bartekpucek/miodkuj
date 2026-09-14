# Źródła i inspiracje

Ten plik dokumentuje materiały wykorzystane przy projektowaniu Miodkuj. Nie jest częścią kontekstu uruchomieniowego: agent nie potrzebuje listy źródeł, żeby redagować tekst.

## Zewnętrzne skille anti-slop i humanizujące

- `hardikpandya/stop-slop`: https://github.com/hardikpandya/stop-slop
- `blader/humanizer`: https://github.com/blader/humanizer
- `petergyang/no-ai-slop`: https://github.com/petergyang/no-ai-slop
- `gabelul/slopbuster`: https://github.com/gabelul/slopbuster
- `petekp/de-slop`: https://playbooks.com/skills/petekp/agent-skills/de-slop
- `shreyas-makes/deslopify`: https://github.com/shreyas-makes/deslopify
- `adenaufal/anti-slop-writing`: https://github.com/adenaufal/anti-slop-writing
- `glaforge/deslopify`: https://github.com/glaforge/deslopify
- `aplaceforallmystuff/the-antislop`: https://github.com/aplaceforallmystuff/the-antislop
- `machinemade-mm/humanmade-antislop`: https://github.com/machinemade-mm/humanmade-antislop
- `theclaymethod/unslop`: https://github.com/theclaymethod/unslop
- `researchanddeploy/sztuczny-miodek`: https://github.com/researchanddeploy/sztuczny-miodek

## Ogólne materiały o pisaniu z AI

- Anti-Slop Writing Rules: https://llmbestpractices.com/writing/anti-slop
- Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Why Does ChatGPT Delve So Much?: https://arxiv.org/html/2412.11385
- Delving into LLM-assisted writing in biomedical publications: https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/

## Polski prosty język i czytelność

- Gov.pl, Prosty język, Służba Cywilna: https://www.gov.pl/web/sluzbacywilna/prosty-jezyk
- Gov.pl, Prosty język, Ministerstwo Cyfryzacji: https://www.gov.pl/web/cyfryzacja/prosty-jezyk
- Podręcznik Jasnopisu: https://jasnopis.pl/manual/

## Dobór słów i rejestr w przekładzie

- [Zgłoszenie #2: centre -> Środek ciężkości](https://github.com/bartekpucek/miodkuj/issues/2) zainspirowało przykład z Edynburgiem i scenariusze 20–23. Scenariusze rozwijają przypadek redakcyjny; nie dokumentują odtworzonego błędu konkretnego modelu lub wersji skilla.
- [WSJP PAN: środek ciężkości, znaczenie przenośne](https://wsjp.pl/haslo/podglad/38155/srodek-ciezkosci/4714234/polityki) odnotowuje utrwalone użycie książkowe. To podstawa oceny rejestru zamiast zakazu wyrażenia.
- [WSJP PAN: środek ciężkości, znaczenie fizyczne](https://wsjp.pl/haslo/podglad/38155/srodek-ciezkosci/4714233/ciala) dokumentuje termin techniczny, który należy zachować.
- [Zgłoszenie #3: Stay -> Zamieszkaj](https://github.com/bartekpucek/miodkuj/issues/3) zainspirowało przykład krótkiego pobytu i scenariusze 24–26. Pełne zdania w scenariuszach są syntetyczne; nie odtwarzają brakującego kontekstu urwanego zgłoszenia.
- [WSJP PAN: zamieszkać](https://wsjp.pl/index.php/haslo/podglad/3172/zamieszkac/2428781/w-domu) potwierdza użycia dotyczące także hotelu i tymczasowego zamieszkania. Dobór `zatrzymaj się` w poradzie na krótki wyjazd jest decyzją kontekstową, a nie zakazem czasownika `zamieszkać`.

## Polska stylometria i teksty AI

- Humanistyka.dev, rodziny cech tekstów AI: https://blog.humanistyka.dev/2026/02/rozpoznawanie-tekstow-ai-piec-grup-cech-zamiast-jednego-wskaznika
- Humanistyka.dev, cechy stylometryczne: https://blog.humanistyka.dev/2026/03/stylometryczne-cechy-tekstow-generowanych-maszynowo
- Artykuł o StyloMetrix: https://ar5iv.labs.arxiv.org/html/2309.12810
- Repozytorium StyloMetrix: https://github.com/ZILiAT-NASK/StyloMetrix
- Polskie metryki StyloMetrix: https://raw.githubusercontent.com/ZILiAT-NASK/StyloMetrix/main/resources/metrics_list_pl.md
- Stylometria rozpoznaje teksty ludzi i LLM w krótkich próbkach: https://arxiv.org/pdf/2507.00838
- PolEval 2025 SMIGIEL, detektor Qwen: https://aclanthology.org/2025.poleval-main.3.pdf
- PolEval 2025 SMIGIEL, scoring kontrastywny: https://aclanthology.org/2025.poleval-main.4.pdf
- PolEval 2025 SMIGIEL, różnica perplexity: https://aclanthology.org/2025.poleval-main.5.pdf
- Science in Poland o idiolektach AI: https://scienceinpoland.pl/en/news/news%2C108666%2Cai-chatbots-develop-distinctive-writing-styles-humans-polish-research-finds.html
- Ludzie Nauki o idiolektach AI: https://ludzie.nauka.gov.pl/wp/aktualnosci/kazda-sztuczna-inteligencja-ma-swoj-styl-artykul-polki-w-scientific-american/
- Wykład HF Studio o idiolektach LLM: https://www.hf.uio.no/hf-studio/arrangementer/2026/Beyond%20%E2%80%9CAI%20Language%E2%80%9D:%20The%20case%20for%20treating%20LLM%20output%20as%20idiolects.html

## Polskie modele językowe

- PLLuM prompt book: https://pllum.org.pl/prompt_book
- Artykuł o PLLuM: https://arxiv.org/html/2511.03823
- Strona artykułu PLLuM: https://huggingface.co/papers/2511.03823
- Korpus instrukcji PLLuM: https://arxiv.org/pdf/2511.17161
- Karta modelu PLLuM: https://huggingface.co/CYFRAGOVPL/PLLuM-8x7B-instruct-2412
- Strona projektu PLLuM: https://opi.org.pl/en/project/odpowiedzialny-rozwoj-otwartego-duzego-modelu-jezykowego-pllum-polish-large-language-universal-model/
- Bielik-PL-11B-v3.0-Instruct: https://huggingface.co/speakleash/Bielik-PL-11B-v3.0-Instruct
