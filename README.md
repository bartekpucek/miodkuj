# Miodkuj

> **English:** Miodkuj is a Polish-language writing skill for Claude, Claude Code, and Codex. It makes the minimum effective edit to AI-sounding, bureaucratic, or over-polished Polish while preserving facts, register, and the writer's voice. The rest of this README is in Polish, because that's the audience.

Miodkuj poprawia polski tekst, który brzmi jak z AI: sztywny, urzędowy, przegadany albo tłumaczony z angielskiego. Robi najmniejszą potrzebną redakcję i nie rusza faktów, liczb, cytatów, rejestru ani rozpoznawalnego głosu autora.

Skill działa jako jedna przenośna wersja z jednego repozytorium:

- **Claude / Claude Code**: skill `/miodkuj` po instalacji folderu,
- **Codex**: skill `$miodkuj`,
- **ChatGPT**: automatyczny wybór skilla albo prośba w naturalnym języku.

Wszystkie środowiska korzystają z tych samych reguł, więc nie rozjeżdżają się w czasie.

## Co robi

- Domyślnie robi najmniejszą skuteczną redakcję: poprawia to, co przeszkadza, i zostawia mocne zdania w spokoju.
- Zostawia bez zmian fakty, liczby, nazwy, linki, cytaty, kod i podstawy prawne.
- Usuwa typowy polski slop: urzędowy żargon, sztuczne i bezosobowe zwroty (które ukrywają, kto coś robi), puste przymiotniki, wymuszone kontrasty i ogólnikowe zakończenia.
- Dopasowuje styl do rejestru: prosty język, marketing, dokumentacja techniczna, tekst naukowy, pisma urzędowe i prawne, treści społecznościowe.
- Rozpoznaje głos autora z samego tekstu, a jeśli dostanie osobną próbkę, traktuje ją jako mocniejszy wzorzec.
- Na życzenie robi sam audyt: cytuje konkretne wzorce i proponuje kierunek poprawki, ale nie zgaduje, czy tekst napisało AI.

Czego **nie** robi: nie obiecuje obejścia wykrywaczy AI, tekstu „nie do wykrycia", podszywania się pod kogoś ani zmyślania faktów.

## Instalacja w Claude Code

Skopiuj albo podlinkuj folder skilla:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/miodkuj" ~/.claude/skills/miodkuj
```

Skill włącza się sam, gdy poprosisz o poprawę polskiego tekstu. Możesz go też wywołać wprost: `/miodkuj`.

## Instalacja na claude.ai

Pobierz gotowy plik albo zbuduj go samodzielnie.

**Sposób A, gotowy plik (bez terminala).** Pobierz `miodkuj.skill` z [ostatniego wydania](https://github.com/bartekpucek/miodkuj/releases/latest) i wgraj go w ustawieniach: **Settings → Capabilities → Skills**.

**Sposób B, zbuduj samodzielnie:**

```bash
./scripts/build.sh
# tworzy dist/miodkuj.skill
```

> Tej ścieżki w claude.ai nie ma w oficjalnej dokumentacji Claude Code. Sprawdź u siebie, bo interfejs bywa aktualizowany.

## Instalacja w Codex

Skopiuj albo podlinkuj folder skilla do katalogu, z którego korzysta Twój Codex:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/miodkuj" ~/.codex/skills/miodkuj
```

Niektóre konfiguracje czytają skille też z `~/.agents/skills`:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/miodkuj" ~/.agents/skills/miodkuj
```

Po instalacji przeładuj środowisko, żeby zobaczyło nowy skill.

> Tej ścieżki też nie ma w oficjalnej dokumentacji. Zweryfikuj ją w swojej wersji Codex.

## Używanie w ChatGPT

W ChatGPT nie używa się `$miodkuj`. Po wgraniu skilla wybierze go automatycznie, gdy prośba pasuje, albo możesz napisać zwykłym językiem, że ma użyć Miodkuj do poprawy tekstu.

## Jak używać

```text
Popraw styl po polsku, zachowaj sens i fakty:
W celu dokonania zgłoszenia należy wypełnić niniejszy formularz.
```

```text
Napisz to po ludzku, bez zmiany faktów:
...
```

```text
Usuń slop. Pokaż też krótką listę zmian:
...
```

Domyślnie skill zwraca najpierw tekst po minimalnej redakcji. Uwagi dodaje tylko wtedy, gdy o nie poprosisz albo gdy ostrzega przed ryzykowną zmianą lub brakiem dowodu. Jeśli chcesz sam audyt, napisz `tylko audyt`.

## Układ repozytorium

```text
shared/references/      # reguły po polsku, jedno źródło prawdy
skills/
  miodkuj/               # wersja dla Claude, Claude Code, Codex i ChatGPT
scripts/                # build.sh, validate.sh, validate_skill.py
tests/                  # testy synchronizacji i pakowania
docs/                   # research, źródła i scenariusze zachowania
```

## Rozwój

Reguły po polsku trzymamy w jednym miejscu: `shared/references/`. Zmieniaj je tam, a potem zsynchronizuj je do skilla i zbuduj paczkę:

```bash
./scripts/build.sh      # synchronizuje reguły i buduje dist/miodkuj.skill
./scripts/validate.sh   # sprawdza skille, metadane, wersje, synchronizację i paczkę
```

Końcowa kontrola `references/eval.md` działa bez punktów: każdy warunek wierności, głosu, rejestru i trybu musi przejść. Ręczne scenariusze, w tym testy tekstu, którego nie należy poprawiać, są w [docs/test-scenarios.md](docs/test-scenarios.md).

## Źródła

Skill powstał na podstawie przeglądu otwartych narzędzi anti-slop i humanizujących oraz polskich materiałów o prostym języku, czytelności, stylometrii i polskich modelach językowych. Zobacz [podsumowanie researchu](docs/research-summary.md) i [pełną listę źródeł](docs/sources.md).

## Licencja

MIT. Zobacz [LICENSE](LICENSE).
