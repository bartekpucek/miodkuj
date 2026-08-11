# Miodkuj

> **Polszczyzna bez sztucznego tonu.**

Miodkuj usuwa slop AI, urzędniczy język, kalki z angielskiego i gładkie ogólniki. Zachowuje fakty, rejestr i głos autora.

## Co robi

- Poprawia tylko to, co tego wymaga. Zostawia mocne zdania, cel tekstu i rozpoznawalny sposób pisania autora.
- Nie zmienia faktów, liczb, nazw, dat, linków, cytatów, kodu, podstaw prawnych ani zastrzeżeń.
- Usuwa między innymi puste wstępy, zdania bez wyraźnego wykonawcy, ciężkie konstrukcje rzeczownikowe, wymuszone kontrasty, kalki z angielskiego i ogólnikowe zakończenia.
- Dopasowuje redakcję do rodzaju tekstu: instrukcji, marketingu, dokumentacji technicznej, tekstu naukowego, pisma urzędowego lub prawnego czy wypowiedzi osobistej.
- Może też zrobić tylko audyt: wskazać problematyczne fragmenty i kierunek zmian bez przepisywania tekstu i zgadywania, czy napisało go AI.

Miodkuj nie obiecuje obchodzenia wykrywaczy AI, tekstu „nie do wykrycia”, podszywania się pod inną osobę ani uzupełniania brakujących faktów.

## Claude Code: /miodkuj

Zainstaluj samodzielny folder skilla przez dowiązanie symboliczne:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/miodkuj" ~/.claude/skills/miodkuj
```

Jeśli nie chcesz używać dowiązania, skopiuj folder:

```bash
mkdir -p ~/.claude/skills
cp -R skills/miodkuj ~/.claude/skills/miodkuj
```

Po instalacji wywołaj skill bezpośrednio poleceniem `/miodkuj`. Zobacz [dokumentację poleceń slash w Claude Code](https://code.claude.com/docs/en/slash-commands).

## Codex: $miodkuj

Zainstaluj ten sam folder przez dowiązanie symboliczne:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/miodkuj" ~/.codex/skills/miodkuj
```

Albo skopiuj folder:

```bash
mkdir -p ~/.codex/skills
cp -R skills/miodkuj ~/.codex/skills/miodkuj
```

Jeśli Twoja konfiguracja korzysta ze wspólnego katalogu skilli, użyj `~/.agents/skills`:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/miodkuj" ~/.agents/skills/miodkuj
```

Wersja bez dowiązania:

```bash
mkdir -p ~/.agents/skills
cp -R skills/miodkuj ~/.agents/skills/miodkuj
```

W Codex wpisz `$miodkuj`. Skill może też uruchomić się automatycznie, gdy prośba pasuje do jego opisu.

## ChatGPT i Claude.ai

Pobierz `miodkuj.skill` z [najnowszego wydania](https://github.com/bartekpucek/miodkuj/releases/latest). Możesz też zbudować plik lokalnie poleceniem `./scripts/build.sh`; wynik znajdziesz w `dist/miodkuj.skill`.

W ChatGPT Personal Skills (umiejętności osobiste) są ogólnie dostępne na kontach Business, Enterprise, Healthcare i Edu. Administratorzy kont Enterprise i Edu mogą najpierw musieć włączyć Skills oraz przesyłanie plików. Jeśli Twoje konto obsługuje Personal Skills, wgraj i zainstaluj skill. ChatGPT może wybrać go automatycznie. Możesz też napisać: `Użyj Miodkuj, aby…`. Nie używaj tutaj polecenia slash. Szczegóły znajdziesz w [dokumentacji Skills w ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

W Claude.ai wgraj `miodkuj.skill`. Claude.ai może wybrać skill automatycznie. Możesz też zwykłym językiem poprosić o użycie Miodkuj. Nie zakładaj, że zadziała tam polecenie slash.

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

Domyślnie skill najpierw zwraca tekst po minimalnej redakcji. Uwagi dodaje tylko na prośbę albo wtedy, gdy zmiana byłaby ryzykowna lub brakuje danych. Jeśli chcesz sam audyt, napisz `tylko audyt`.

## Układ repozytorium

```text
shared/references/      # polskie reguły, jedno źródło
skills/
  miodkuj/              # przenośny skill dla wszystkich platform
scripts/                # budowanie, synchronizacja i walidacja
tests/                  # testy repozytorium i paczki
docs/                   # źródła, research i scenariusze zachowania
```

## Rozwój

Reguły znajdziesz w `shared/references/`. Po zmianie zsynchronizuj je ze skillem, zbuduj paczkę i sprawdź repozytorium:

```bash
./scripts/build.sh      # synchronizuje reguły i buduje dist/miodkuj.skill
./scripts/validate.sh   # sprawdza skill, metadane, synchronizację i paczkę
```

Końcową kontrolę opisuje `references/eval.md` w folderze skilla. Każdy warunek wierności, głosu, rejestru i trybu musi przejść. Ręczne scenariusze, w tym teksty, których nie należy poprawiać, są w [docs/test-scenarios.md](docs/test-scenarios.md).

## Pochodzenie nazwy

Miodkuj jest niezależnym projektem open source i językowym hołdem dla profesora Jana Miodka. Profesor Jan Miodek nie uczestniczy w projekcie ani go nie popiera.

## Źródła

Skill powstał po przeglądzie otwartych narzędzi do usuwania slopu i humanizacji tekstu oraz polskich materiałów o prostym języku, czytelności, stylometrii i polskich modelach językowych. Zobacz [podsumowanie przeglądu](docs/research-summary.md) i [pełną listę źródeł](docs/sources.md).

## Licencja

MIT. Zobacz [LICENSE](LICENSE).
