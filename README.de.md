# Command Autopilot für Claude Code

**Nutze ganz Claude Code, nicht nur die paar Befehle, die du kennst.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | Deutsch

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Claude Code kann parallele Agenten ausschwärmen lassen, ein Ziel von sich aus verfolgen, mehrstufige Workflows ausführen, das Web durchforsten. Doch im entscheidenden Moment greifen selbst Profis darauf zurück, sich von Hand durchzuarbeiten. Command Autopilot beobachtet, was du gerade tatsächlich tust, und legt dir im richtigen Moment **die wenigen wirkungsvollen Züge vor, die passen: als Menü, aus dem du auswählst.** Die Kleinigkeiten (Rückgängig, Kontext-Hygiene) erledigt er einfach. Es ist nicht nur für Einsteiger, die die Befehle nie gehört haben: Auch ein Power-User vergisst unter Druck den besten Zug, und genau dieses zehnte Mal ist der ganze Punkt. Open Source, MIT, null Telemetrie.

## Was es möglich macht

| Der Moment | Ohne Autopilot | Mit Autopilot |
|---|---|---|
| Eine große, mehrdateiige oder repetitive Aufgabe | Du arbeitest dich Schritt für Schritt durch | Er legt ein **Menü schnellerer Wege** vor (parallele Agenten, ein Workflow, /background), bevor es losgeht: mit den Abwägungen, du wählst |
| Eine Aufgabe, die einfach bis zum Ende durchlaufen sollte | Du betreust sie Zug um Zug | Er bietet **/goal** an, damit Claude von selbst bis zum Ende arbeitet |
| Eine Frage, die echte Recherche braucht | Eine oberflächliche Suche | Er führt **tiefe Recherche aus mehreren Quellen** durch und reicht dir eine belegte Antwort |
| Skills, die du installiert, aber vergessen hast | Sie liegen ungenutzt | Er **nutzt sie** und sagt, welcher gerade geholfen hat: „dein pdf-Skill kam zum Einsatz: Datei direkt gelesen“ |
| Du lehnst einen Vorschlag immer wieder ab | Die meisten Tools nerven ewig | Er versteht den Wink und lässt ihn fallen: Er lernt *dich* kennen |
| Die Grundlagen: Rückgängig, Kontext, Nebenbemerkungen | Du hast die Befehle nie gelernt | Still erledigt: **/rewind** vor jeder Reparatur, **/clear** beim Themenwechsel, **/btw** für Nebenbemerkungen |

**Wie es tatsächlich klingt:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

Neu bei den Befehlen selbst? Wir pflegen außerdem [den verständlichen Claude-Code-Befehls-Spickzettel](docs/claude-code-commands-cheatsheet.md) (auf Englisch) und [8 Claude-Code-Workflows, die echte Arbeit sparen](docs/claude-code-workflows.md) (auf Englisch).

Claude Code hat rund 100 eingebaute Slash-Befehle, dazu jeden Skill, den du installiert hast, und die mächtigsten davon (Orchestrierung, Parallelität, Autonomie) sind genau die, die niemand entdeckt. Command Autopilot schließt diese Lücke mit drei Kniffen:

1. **Im richtigen Moment legt er dir deine Optionen als Menü vor.** Vor einer großen, repetitiven, langlaufenden oder riskanten Aufgabe präsentiert er die 2 bis 4 wirkungsvollen Züge, die wirklich passen: parallele Agenten, ein Workflow, ein autonomes /goal, tiefe Recherche, /background, jeweils mit seiner Abwägung, und du wählst. Kein einzelner Vorschlag zum Annehmen-oder-Ablehnen, sondern das Menü, damit du entscheidest. (Auch für einen Profi: Der Wert ist der Zug, an den du *gerade jetzt* nicht gedacht hast, nicht einer, von dem du noch nie gehört hast.)
2. **Den Rest macht er selbst, statt ihn zu empfehlen.** Was Claude von sich aus tun kann, tut er einfach: Große Änderungen gehen in den Planmodus, bevor eine Datei angefasst wird, Vorlieben wandern ins Gedächtnis, deine installierten Skills werden genutzt (und er sagt, welcher geholfen hat). Die Sicherheits-Grundlagen (/rewind, /clear, /btw) reicht er dir im exakten Moment, nie als Vortrag.
3. **Er lernt, dir aus dem Weg zu gehen.** Jeder Vorschlag, den du überspringst, ist lokaler Beleg: Was du immer wieder ablehnst, verstummt, sodass es nie zum Genörgel wird. (Tiefere Personalisierung, das Hineinlehnen in genau die Züge, die *du* bevorzugst, steht auf der Roadmap; der Gewinn von heute ist Präzision und Stille, nicht so zu tun, als kenne er dich schon.)

Er arbeitet nie eine feste Checkliste von Tipps ab. Er denkt über jeden Zug neu nach, weist höchstens einmal auf etwas hin, wenn es wirklich hilft, und bleibt ansonsten still. Das Ziel ist, dass du ihn gar nicht mehr bemerkst.

**Nur am Stöbern?** Füge [portable/PROMPT.md](portable/PROMPT.md) in claude.ai oder einen beliebigen Assistenten ein: das Kernverhalten, nichts installiert, 60 Sekunden.

## Installation

**Am einfachsten: Lass Claude die Installation für dich erledigen.** Kopiere diesen ganzen Block, füge ihn in eine beliebige Claude-Code-Unterhaltung ein und drücke Enter:

```
Install the Command Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Run: claude plugin install command-autopilot@claude-code-command-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude führt die Installation aus und kümmert sich um die Sonderfälle (CLI nicht im PATH usw.). Du brauchst keinerlei Terminal-Kenntnisse.

<details>
<summary>Manuelle Alternativen</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

Falls `claude` nicht gefunden wird, verwende stattdessen `~/.local/bin/claude` oder führe `./install.sh` aus einem Klon dieses Repos aus.

**In einer Claude-Code-CLI-Sitzung** (der Befehl `/plugin` ist in der Desktop-App nicht verfügbar):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

Starte Claude Code danach neu (komplett beenden: Hooks laden beim Start) und frag Claude: **„prüf, ob der Autopilot funktioniert“** – der eingebaute Doctor bestätigt, dass alles von Anfang bis Ende greift. Mach dann die 2-Minuten-Tour: „gib mir die Autopilot-Tour“.

**Funktioniert nicht?**
- Vorschläge erscheinen nie → du musst Claude Code komplett beenden und neu öffnen; Hooks laden nur beim Start.
- `/plugin` nicht gefunden → die Desktop-App hat keinen `/plugin`-Befehl; nutze die Copy-Paste-Installation oben.
- Alles andere → bitte Claude, „den Autopilot-Doctor auszuführen“, und füge dessen Ausgabe in ein [Issue](https://github.com/WinterDDo/claude-code-command-autopilot/issues) ein.

## Aktualisieren

Frag Claude: **„aktualisiere das command-autopilot-Plugin auf die neueste Version.“** Er führt die drei Schritte unten für dich aus.

Von Hand (oder falls du auf „bereits in der neuesten Version“ stößt – das bedeutet, deine lokale Kopie des Marketplace ist veraltet, also frische sie *zuerst* auf):

```sh
claude plugin marketplace update claude-code-command-autopilot   # refresh the catalog from GitHub
claude plugin update command-autopilot@claude-code-command-autopilot
```

Beende dann Claude Code komplett und öffne es neu – Regeln und Hooks laden beim Start. (Cloud-Sitzungen klonen das Repo immer frisch, sie übernehmen neue Versionen also von selbst.)

## In 2 Minuten in Aktion erleben

1. Bitte um etwas Großes: *„Entwirf und baue eine Statistik-Funktion für dieses Projekt.“* → Claude geht **von selbst in den Planmodus**, bevor er eine Datei anfasst. Lehne den Plan ab; nichts hat sich geändert.
2. Lass ihn eine Wegwerf-Datei erstellen und sag dann *„mach das rückgängig.“* → Seine erste Reaktion ist, dir **/rewind (Esc Esc)** zu reichen, statt vorwärts zu flicken.

## Was er niemals tun wird

- **Keine Telemetrie.** Alle Belege liegen in lokalen Dateien, die du öffnen, prüfen und löschen kannst. Die Deinstallation entfernt alles.
- **Kein Genörgel.** Harte Verträge: höchstens ein Vorschlag pro Antwort, derselbe Befehl höchstens einmal pro Sitzung, und „leise“ oder komplett stumm ist nur einen Satz entfernt („Autopilot stummschalten“). Wiederholt weggewischte Vorschläge verblassen von selbst.
- **Kein erfundener Nutzen.** Frag „was hat der Autopilot für mich getan“: Jede Zahl im Bericht lässt sich auf ein echtes, protokolliertes Ereignis zurückführen.

## Die ehrlichen Kosten

Der Autopilot speist seine Regeln in jeden Prompt ein: rund 300 bis 500 Tokens je nach Modus (leise ≈ 300, stumm = 0). Das ist der Preis für die eine Platzierung, die nachweislich funktioniert. Den Regler hast du in der Hand: `teaching` → `normal` → `quiet` → stumm.

## Funktioniert in der Cloud und im Team

Cloud-Sitzungen laden deine persönlichen Plugins nicht, und sie frischen den Marketplace-Cache nicht auf. Der verlässliche Weg, den Autopiloten in Claude Code im Web und für Teamkollegen zu bekommen, ist deshalb, **seine Regeln in dein Repo einzubinden (zu „vendoren“)**: Committe eine kleine `.claude/autopilot-context.json` (die Regeln) plus `.claude/autopilot-cloud.sh` und verdrahte in der `.claude/settings.json` deines Repos die Hooks `SessionStart` + `UserPromptSubmit` damit. Aus einem Klon dieses Repos kopiert ein einziger Befehl die Dateien und gibt die exakten Hook-Zeilen aus:

```sh
plugins/command-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

Neue Cloud-Sitzungen klonen dein Repo frisch und übernehmen die Regeln automatisch – für jeden, der in diesem Repo arbeitet. (Cloud-Einschränkung: Der Lernstand ist dort pro Sitzung; das In-the-Moment-Menü funktioniert trotzdem.)

## Wie es funktioniert (für Neugierige)

Ein einziger `UserPromptSubmit`-Hook baut bei jeder Nachricht den Kontext zusammen: eine kurze Denk-Disziplin + deine gelernten Regeln + ein kompakter Beleg-Auszug. Es gibt **keine Szenario→Befehl-Nachschlagetabelle** – das Modell überlegt sich bei jedem Zug neu, was *deine* Aufgabe braucht; die Wissensbasis ist Referenz, nicht Auslöser. Skripte zeichnen nur auf und komprimieren – **das gesamte Urteilsvermögen liegt beim Modell**, deshalb gibt es nirgendwo magische Schwellenwerte. Eine Wissensbasis ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) trägt den Ein-Zeilen-Nutzen jedes Befehls und eine Reihe von Kombi-Playbooks; das Modell liest sie bei Bedarf, also kostet sie pro Prompt nichts. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Enthaltene Skills: `tutor` (geführte Tour) · `doctor` (prüfen, ob alles läuft) · `config` (stumm/Modi) · `evolve` (deine Belege zu Regeln destillieren) · `profile` (das Nutzen-Dashboard) · `whats-new` (neue Befehle und ungenutzte Skills, erklärt nach Nutzen).

## Voraussetzungen

Python 3.8+ für das volle Erlebnis. Ohne Python läuft der Autopilot im zustandslosen Modus: Kernverhalten intakt, Lernen pausiert.

## FAQ

**Werden meine Daten irgendwohin gesendet?** Nein. Null Telemetrie. Alles liegt in lokalen Dateien unter `~/.claude/command-autopilot/`, die du öffnen, prüfen und löschen kannst. Die Deinstallation entfernt alles.

**Verbirgt er etwas vor mir?** Nein. Frag Claude „was leitet dich gerade?“ oder bitte ihn, die Anweisung zu zeigen, die dieses Plugin einspeist, und er sagt sie dir vollständig: Die Regeln sind Klartext in [`plugins/command-autopilot/rules/`](plugins/command-autopilot/rules), und die Anleitung weist Claude ausdrücklich an, transparent zu sein, wann immer du fragst. Nichts an dem Plugin ist vor dir geheim.

**Wird er mich nerven?** Die harten Verträge sagen Nein: höchstens ein Vorschlag pro Antwort, derselbe Befehl höchstens einmal pro Sitzung, und Vorschläge, die du immer wieder wegwischst, verblassen von selbst. Mit „Autopilot stummschalten“ wird er komplett still.

**Was kostet es?** Er speist je nach Modus rund 300 bis 500 Tokens an Regeln pro Nachricht ein (leise ≈ 300, stumm = 0). Das ist der ehrliche Preis für Verlässlichkeit; den Regler hast du in der Hand.

**Funktioniert es in Claude Code im Web / für mein Team?** Ja: Binde seine Regeln mit einem einzigen Befehl in das `.claude/` deines Repos ein (`vendor-to-repo.sh`, siehe [Funktioniert in der Cloud und im Team](#funktioniert-in-der-cloud-und-im-team)). Cloud-Sitzungen klonen das Repo frisch und übernehmen sie, sodass jeder, der in diesem Repo arbeitet, sie bekommt.

**Ich habe kein Python, funktioniert es trotzdem?** Ja, im zustandslosen Modus: Das gesamte Kernverhalten funktioniert, nur die Lernschicht pausiert, bis Python 3.8+ verfügbar ist.

**Wie deinstalliere ich es?** Führe `claude plugin uninstall command-autopilot@claude-code-command-autopilot` aus (oder bitte Claude darum) und lösche `~/.claude/command-autopilot/`. Es bleibt nichts zurück.

**Was unterscheidet das von ein paar Regeln in der CLAUDE.md?** Genau das haben wir zuerst versucht, zweimal. Regeln in der CLAUDE.md unterliegen konkurrierenden Anweisungen; die Hook-Einspeisung bei jedem Prompt ist die einzige Platzierung, von der wir nachweisen konnten, dass sie das Modell zu 100 % erreicht. Dieser Befund, zusammen mit dem Lern-Design ohne magische Schwellenwerte, ist der ganze Grund, warum das ein Plugin ist und kein Markdown-Schnipsel. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Mitmachen

**Erster PR in 5 Minuten:** Verbessere die Formulierung eines Vorschlags in `plugins/command-autopilot/rules/*.txt` oder füge den Ein-Zeilen-Nutzen eines Befehls zu `plugins/command-autopilot/knowledge/commands.json` hinzu, führe den passenden Schritt in [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) aus und reiche ein. README-Übersetzungen sind ebenso willkommen. Das Verhalten lebt in Textdateien, nicht im Code: siehe [docs/TUNING.md](docs/TUNING.md) für die Iterationsdisziplin.

MIT-lizenziert.
