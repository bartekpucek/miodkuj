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

Najprościej skopiuj folder `skills/miodkuj` do katalogu skilli Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R skills/miodkuj ~/.claude/skills/miodkuj
```

Jeśli rozwijasz Miodkuj i chcesz od razu widzieć każdą zmianę, zamiast kopiowania utwórz skrót do folderu w tym repozytorium (tzw. dowiązanie symboliczne):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/miodkuj" ~/.claude/skills/miodkuj
```

Po instalacji wywołaj skill bezpośrednio poleceniem `/miodkuj`. Zobacz [dokumentację poleceń slash w Claude Code](https://code.claude.com/docs/en/slash-commands).

## Codex: $miodkuj

Najprościej skopiuj folder `skills/miodkuj` do katalogu skilli Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/miodkuj ~/.codex/skills/miodkuj
```

Jeśli rozwijasz Miodkuj i chcesz od razu widzieć każdą zmianę, użyj skrótu do folderu w tym repozytorium:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/miodkuj" ~/.codex/skills/miodkuj
```

Codex może też czytać skille ze wspólnego katalogu `~/.agents/skills`. Aby skopiować tam Miodkuj, wpisz:

```bash
mkdir -p ~/.agents/skills
cp -R skills/miodkuj ~/.agents/skills/miodkuj
```

Jeśli wolisz skrót do folderu w repozytorium:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/miodkuj" ~/.agents/skills/miodkuj
```

W Codex wpisz `$miodkuj`. Skill może też uruchomić się automatycznie, gdy prośba pasuje do jego opisu.

## ChatGPT

1. [Pobierz `miodkuj.skill`](https://github.com/bartekpucek/miodkuj/releases/latest/download/miodkuj.skill).
2. W ChatGPT otwórz **Plugins**, a potem kartę **Skills**. Możesz też wejść bezpośrednio na [chatgpt.com/skills](https://chatgpt.com/skills).
3. Wybierz **Create** → **Upload from your computer**.
4. Wskaż pobrany plik `miodkuj.skill` i poczekaj, aż ChatGPT go sprawdzi.
5. Otwórz czat i napisz na przykład: `Użyj Miodkuj, aby poprawić ten tekst: …`

ChatGPT może też wybrać Miodkuj automatycznie, gdy poprosisz o poprawę polskiego tekstu. Nie używaj polecenia slash. Jeśli nie widzisz sekcji **Skills**, Twój plan może jej nie obsługiwać albo administrator firmowego konta jeszcze jej nie włączył. Personal Skills są obecnie ogólnie dostępne na kontach Business, Enterprise, Healthcare i Edu. Na kontach Enterprise i Edu administrator zarządza również zgodą na przesyłanie plików. Szczegóły znajdziesz w [oficjalnej instrukcji OpenAI](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## Claude.ai

1. [Pobierz `miodkuj.skill`](https://github.com/bartekpucek/miodkuj/releases/latest/download/miodkuj.skill).
2. Włącz wykonywanie kodu zgodnie z [instrukcją korzystania ze skilli](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
3. Wgraj pobrany plik `miodkuj.skill`.
4. Poproś zwykłym językiem o użycie Miodkuj. Claude.ai może też wybrać skill automatycznie.

W Claude.ai nie zakładaj, że zadziała polecenie slash. Jeśli rozwijasz skill lokalnie, zbudujesz nową paczkę poleceniem `./scripts/build.sh`; plik znajdziesz w `dist/miodkuj.skill`.

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
