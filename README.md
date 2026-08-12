# Miodkuj

> **Polszczyzna bez sztucznego tonu.**

Miodkuj poprawia polskie teksty bez zmieniania ich sensu. Usuwa slop AI, czyli schematyczne, napompowane brzmienie, a także urzędniczy język, kalki z angielskiego i gładkie ogólniki. Zachowuje fakty, styl i głos autora.

## Co robi

- Poprawia tylko fragmenty, które tego potrzebują. Zostawia mocne zdania, cel tekstu i rozpoznawalny sposób pisania autora.
- Nie zmienia faktów, liczb, nazw, dat, linków, cytatów, kodu, podstaw prawnych ani zastrzeżeń.
- Usuwa puste wstępy, bezosobowe zdania, ciężkie konstrukcje rzeczownikowe, wymuszone kontrasty, kalki z angielskiego i ogólnikowe zakończenia.
- Dopasowuje redakcję do rodzaju tekstu: instrukcji, marketingu, dokumentacji technicznej, tekstu naukowego, pisma urzędowego lub prawnego czy wypowiedzi osobistej.
- Może też zrobić sam audyt: wskazać problematyczne fragmenty i kierunek zmian, bez przepisywania tekstu i zgadywania, czy napisało go AI.

Miodkuj nie obiecuje obchodzenia wykrywaczy AI, tekstu „nie do wykrycia”, podszywania się pod inną osobę ani uzupełniania brakujących faktów.

## Wybierz platformę

| Używasz | Najłatwiejsza instalacja | Jak wywołać |
| --- | --- | --- |
| ChatGPT | Pobierz plik i wgraj go w Skills | `Użyj Miodkuj, aby…` |
| Claude.ai | Pobierz plik i wgraj go w Skills | `Użyj Miodkuj, aby…` |
| Claude Code | Zainstaluj plugin z marketplace | `/miodkuj:miodkuj` |
| Codex | Zainstaluj plugin z marketplace | `$miodkuj` |

## ChatGPT

1. [Pobierz `miodkuj.skill`](https://github.com/bartekpucek/miodkuj/releases/latest/download/miodkuj.skill).
2. W ChatGPT wybierz **Plugins** → **Skills** → **Create** → **Upload from your computer**. Możesz też otworzyć [chatgpt.com/skills](https://chatgpt.com/skills).
3. Wskaż pobrany plik. ChatGPT sprawdzi plik, zanim skill stanie się dostępny.
4. Otwórz czat i napisz na przykład: `Użyj Miodkuj, aby poprawić ten tekst: …`

ChatGPT może też wybrać Miodkuj automatycznie, gdy poprosisz o poprawę polskiego tekstu. Nie używaj tutaj polecenia slash.

Personal Skills, czyli osobiste skille, są obecnie ogólnie dostępne na kontach Business, Enterprise, Healthcare i Edu. Na kontach Enterprise i Edu administrator decyduje, kto może korzystać ze Skills i przesyłać pliki. Jeśli nie widzisz sekcji **Skills** lub opcji przesłania pliku, sprawdź plan i ustawienia administratora. Szczegóły opisuje [oficjalna instrukcja OpenAI](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## Claude.ai

1. [Pobierz `miodkuj.skill`](https://github.com/bartekpucek/miodkuj/releases/latest/download/miodkuj.skill).
2. Jeśli używasz planu Free, Pro lub Max, otwórz **Settings** → **Capabilities** i włącz **Code execution and file creation**, czyli wykonywanie kodu i tworzenie plików.
3. Na planie Team lub Enterprise właściciel organizacji musi sprawdzić w **Organization settings** → **Skills**, czy włączone są **Code execution and file creation** oraz **Skills**.
4. Otwórz **Customize** → **Skills**, wybierz dodanie własnego skilla i wgraj plik `miodkuj.skill`. Po wgraniu upewnij się, że skill jest włączony.
5. Napisz na przykład: `Użyj Miodkuj, aby poprawić ten tekst: …`

Te wymagania i ustawienia dla poszczególnych planów opisuje [oficjalna instrukcja Anthropic](https://support.claude.com/en/articles/12512180-use-skills-in-claude). Claude.ai może wybrać Miodkuj automatycznie. Nie używaj tutaj polecenia slash.

## Claude Code

W otwartej sesji Claude Code wpisz kolejno:

```text
/plugin marketplace add bartekpucek/miodkuj
/plugin install miodkuj@miodkuj
/reload-plugins
```

Marketplace to katalog pluginów dostępny w Claude Code. Teraz wywołaj Miodkuj poleceniem `/miodkuj:miodkuj`. Claude Code dopisuje nazwę pluginu przed nazwą skilla, żeby odróżnić go od innych. Dlatego ta instalacja nie daje krótkiego `/miodkuj`. Więcej informacji znajdziesz w [oficjalnej instrukcji pluginów Claude Code](https://code.claude.com/docs/en/discover-plugins).

### Instalacja ręczna z krótkim `/miodkuj`

Jeśli wolisz krótkie `/miodkuj`, wybierz instalację ręczną. Potrzebujesz programu Git. W terminalu wpisz kolejno:

```bash
miodkuj_tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/bartekpucek/miodkuj.git "$miodkuj_tmp"
mkdir -p ~/.claude/skills
cp -R "$miodkuj_tmp/plugins/miodkuj/skills/miodkuj" ~/.claude/skills/miodkuj
rm -rf "$miodkuj_tmp"
```

Pierwsza linia tworzy osobny katalog tymczasowy i zapisuje jego dokładną ścieżkę. Następne linie pobierają repozytorium i kopiują z niego tylko folder `plugins/miodkuj/skills/miodkuj`. Ostatnia linia usuwa ten sam katalog tymczasowy. Po instalacji użyj `/miodkuj`. Zobacz też [dokumentację poleceń slash w Claude Code](https://code.claude.com/docs/en/slash-commands).

## Codex

W terminalu wpisz kolejno:

```bash
codex plugin marketplace add bartekpucek/miodkuj
codex plugin add miodkuj@miodkuj
```

Pierwsze polecenie dodaje katalog pluginów Miodkuj, a drugie instaluje plugin. Po instalacji rozpocznij nowe zadanie w Codex i wpisz `$miodkuj`. Codex może też wybrać skill automatycznie, gdy Twoja prośba pasuje do jego opisu.

## Jak używać

Możesz zacząć od jednego z tych poleceń:

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

Miodkuj najpierw zwraca tekst po minimalnej redakcji. Uwagi dodaje tylko na prośbę albo wtedy, gdy zmiana byłaby ryzykowna lub brakuje danych. Jeśli chcesz sam audyt, napisz `tylko audyt`.

## Układ repozytorium

```text
shared/references/      # główny zestaw polskich reguł
plugins/
  miodkuj/
    skills/miodkuj/     # jeden skill używany na wszystkich platformach
scripts/                # budowanie, synchronizacja i sprawdzanie
tests/                  # testy repozytorium i paczki
docs/                   # źródła, opis badań i scenariusze zachowania
```

## Rozwój

Reguły źródłowe znajdziesz w `shared/references/`, a gotowy skill w `plugins/miodkuj/skills/miodkuj/`. Po zmianie uruchom dwa polecenia:

```bash
./scripts/build.sh      # synchronizuje reguły i buduje dist/miodkuj.skill
./scripts/validate.sh   # sprawdza skill, metadane, synchronizację i paczkę
```

Końcowa kontrola jest opisana w `references/eval.md` w folderze skilla. Przed publikacją sprawdź, czy tekst zachowuje sens i głos autora, pasuje do sytuacji oraz działa w wybranym trybie. Ręczne scenariusze, w tym teksty, których nie należy poprawiać, znajdziesz w [docs/test-scenarios.md](docs/test-scenarios.md).

## Pochodzenie nazwy

Miodkuj jest niezależnym projektem open source. Nazwa jest językowym hołdem dla profesora Jana Miodka. Profesor Jan Miodek nie uczestniczy w projekcie ani go nie popiera.

## Źródła

Miodkuj powstał po przeglądzie otwartych narzędzi do usuwania slopu i nadawania tekstom bardziej naturalnego brzmienia. Wykorzystuje też polskie materiały o prostym języku, czytelności, stylometrii i polskich modelach językowych. Zobacz [podsumowanie przeglądu](docs/research-summary.md) i [pełną listę źródeł](docs/sources.md).

## Licencja

MIT. Zobacz [LICENSE](LICENSE).
