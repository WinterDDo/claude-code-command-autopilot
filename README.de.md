# Skill Autopilot für Claude Code

**Nutze die Skills, die du installiert hast – nicht nur die, an die du dich erinnerst.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | Deutsch

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Du installierst Skills, um Claude Code zu erweitern – und vergisst dann, welche du hast oder wann sie passen. Und es wird *schlimmer*, je mehr du installierst: Jenseits von Claude Codes Skill-Budget verwirft es still die Beschreibungen der Skills, die du am seltensten nutzt, sodass der perfekte Skill für *diese* Aufgabe für das Modell unsichtbar sein kann. **Skill Autopilot legt dir bei jedem Zug die installierten Skills vor, die für dein aktuelles Vorhaben am relevantesten sind – sodass ein passender vor dir liegt, statt vergessen zu sein.** Er breitet außerdem die wirkungsvollen Züge, die zu einer großen oder riskanten Aufgabe passen (parallele Agenten, ein Workflow, ein autonomes /goal, tiefe Recherche), als Menü vor dir aus, aus dem du auswählst, und die Kleinigkeiten (Rückgängig, Kontext-Hygiene) erledigt er still. Neu und experimentell – Open Source, MIT, null Telemetrie, lokal zuerst.

## Was es möglich macht

| Der Moment | Ohne Autopilot | Mit Autopilot |
|---|---|---|
| Eine große, mehrdateiige oder repetitive Aufgabe | Du arbeitest dich Schritt für Schritt durch | Er legt ein **Menü schnellerer Wege** vor (parallele Agenten, ein Workflow, /background), bevor es losgeht: mit den Abwägungen, du wählst |
| Eine Aufgabe, die einfach bis zum Ende durchlaufen sollte | Du betreust sie Zug um Zug | Er bietet **/goal** an, damit Claude von selbst bis zum Ende arbeitet |
| Eine Frage, die echte Recherche braucht | Eine oberflächliche Suche | Er führt **tiefe Recherche aus mehreren Quellen** durch und reicht dir eine belegte Antwort |
| Skills, die du installiert, aber vergessen hast | Sie liegen ungenutzt – oder werden aus dem Kontext verworfen, sobald du über dem Budget bist | Er **legt dir die für deine Aufgabe relevanten vor**, sodass ein passender Skill vor dem Modell liegt |
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

Claude Code läuft auf den Skills und Befehlen, die du installiert hast – aber der richtige taucht selten im richtigen Moment auf, und eine große Skill-Bibliothek macht es *schlimmer* (über dem Budget verwirft Claude Code die Beschreibungen der am wenigsten genutzten Skills aus dem Kontext). Skill Autopilot schließt diese Lücke mit drei Kniffen:

1. **Er legt dir die passenden Skills vor – genau dann, wenn sie passen.** Bei jedem Zug bewertet er deine installierten Skills gegen das, was du tatsächlich verlangst, und stellt die relevantesten vor das Modell (mit Namen; das Modell liest die vollständige Beschreibung bei Bedarf) – darunter auch solche, die Claude Code wegen Budget-Überschreitung aus dem Kontext verworfen hat. Und wenn mehrere wirkungsvolle Züge zu einer großen oder riskanten Aufgabe passen – parallele Agenten, ein Workflow, ein autonomes /goal, tiefe Recherche – legt er sie als Menü vor und du wählst.
2. **Den Rest macht er selbst, statt ihn zu empfehlen.** Was Claude von sich aus tun kann, tut er einfach: Große Änderungen gehen in den Planmodus, bevor eine Datei angefasst wird, Vorlieben wandern ins Gedächtnis, ein passender installierter Skill wird genutzt. Die Sicherheits-Grundlagen (/rewind, /clear, /btw) reicht er dir im exakten Moment, nie als Vortrag.
3. **Er lernt, dir aus dem Weg zu gehen.** Jeder Vorschlag, den du überspringst, ist lokaler Beleg: Was du immer wieder ablehnst, verstummt, sodass es nie zum Genörgel wird. (Tiefere Personalisierung, das Hineinlehnen in genau die Züge, die *du* bevorzugst, steht auf der Roadmap; der Gewinn von heute ist Präzision und Stille, nicht so zu tun, als kenne er dich schon.)

Er arbeitet nie eine feste Checkliste von Tipps ab. Er denkt über jeden Zug neu nach, weist höchstens einmal auf etwas hin, wenn es wirklich hilft, und bleibt ansonsten still. Das Ziel ist, dass du ihn gar nicht mehr bemerkst.

**Nur am Stöbern?** Füge [portable/PROMPT.md](portable/PROMPT.md) in claude.ai oder einen beliebigen Assistenten ein: das Kernverhalten, nichts installiert, 60 Sekunden.

## Installation

**Am einfachsten: Lass Claude die Installation für dich erledigen.** Kopiere diesen ganzen Block, füge ihn in eine beliebige Claude-Code-Unterhaltung ein und drücke Enter:

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude führt die Installation aus und kümmert sich um die Sonderfälle (CLI nicht im PATH usw.). Du brauchst keinerlei Terminal-Kenntnisse.

<details>
<summary>Manuelle Alternativen</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

Falls `claude` nicht gefunden wird, verwende stattdessen `~/.local/bin/claude` oder führe `./install.sh` aus einem Klon dieses Repos aus.

**In einer Claude-Code-CLI-Sitzung** (der Befehl `/plugin` ist in der Desktop-App nicht verfügbar):

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

Starte Claude Code danach neu (komplett beenden: Hooks laden beim Start) und frag Claude: **„prüf, ob der Autopilot funktioniert“** – der eingebaute Doctor bestätigt, dass alles von Anfang bis Ende greift. Mach dann die 2-Minuten-Tour: „gib mir die Autopilot-Tour“.

**Funktioniert nicht?**
- Vorschläge erscheinen nie → du musst Claude Code komplett beenden und neu öffnen; Hooks laden nur beim Start.
- `/plugin` nicht gefunden → die Desktop-App hat keinen `/plugin`-Befehl; nutze die Copy-Paste-Installation oben.
- Alles andere → bitte Claude, „den Autopilot-Doctor auszuführen“, und füge dessen Ausgabe in ein [Issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues) ein.

## Aktualisieren

Frag Claude: **„aktualisiere das Skill-Autopilot-Plugin auf die neueste Version.“** Er führt die drei Schritte unten für dich aus.

Von Hand (oder falls du auf „bereits in der neuesten Version“ stößt – das bedeutet, deine lokale Kopie des Marketplace ist veraltet, also frische sie *zuerst* auf):

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
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

Der Autopilot speist seine Regeln in jeden Prompt ein: rund 500 bis 600 Tokens im Dauerbetrieb (weniger im `quiet`-Modus, 0 wenn stummgeschaltet). In Zügen, in denen installierte Skills relevant sind, kommen deren Namen hinzu – ein kleiner, begrenzter Zuschlag (~140 Tokens), gedeckelt, und nichts in Zügen, in denen keiner passt. Gegen ein 200k-Kontextfenster ist das ein Bruchteil eines Prozents. Den Regler hast du in der Hand: `teaching` → `normal` → `quiet` → stumm.

## Funktioniert in der Cloud und im Team

Cloud-Sitzungen laden deine persönlichen Plugins nicht, und sie frischen den Marketplace-Cache nicht auf. Der verlässliche Weg, den Autopiloten in Claude Code im Web und für Teamkollegen zu bekommen, ist deshalb, **seine Regeln in dein Repo einzubinden (zu „vendoren“)**: Committe eine kleine `.claude/autopilot-context.json` (die Regeln) plus `.claude/autopilot-cloud.sh` und verdrahte in der `.claude/settings.json` deines Repos die Hooks `SessionStart` + `UserPromptSubmit` damit. Aus einem Klon dieses Repos kopiert ein einziger Befehl die Dateien und gibt die exakten Hook-Zeilen aus:

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

Neue Cloud-Sitzungen klonen dein Repo frisch und übernehmen die Regeln automatisch – für jeden, der in diesem Repo arbeitet. (Cloud-Einschränkung: Der Lernstand ist dort pro Sitzung; das In-the-Moment-Menü funktioniert trotzdem.)

## Wie es funktioniert (für Neugierige)

Ein einziger `UserPromptSubmit`-Hook baut bei jeder Nachricht den Kontext zusammen: eine kurze Denk-Disziplin + die installierten Skills, die für deinen Prompt am relevantesten sind + deine gelernten Regeln + ein kompakter Beleg-Auszug. Das Vorlegen der Skills ist bewusst schlicht-und-ehrlich: Bei Sitzungsbeginn baut er einen lokalen Index deiner installierten Skills, und bei jedem Zug bewertet er sie über eine günstige Wort-Überschneidung mit deinem Prompt und speist nur die wenigen relevantesten *Namen* ein (das Modell liest jede vollständige Beschreibung bei Bedarf und entscheidet, ob es einen nutzt) – nichts wird eingespeist, wenn nichts passt. Es gibt **keine Szenario→Befehl-Nachschlagetabelle** und keinen Ähnlichkeits-Scorer, dem das Modell vertrauen soll – das Modell überlegt sich bei jedem Zug neu, was *deine* Aufgabe braucht; die Wissensbasis ist Referenz, nicht Auslöser. Skripte zeichnen nur auf und komprimieren – **das gesamte Urteilsvermögen liegt beim Modell**, deshalb gibt es nirgendwo magische Schwellenwerte. Eine Wissensbasis ([commands.json](plugins/skill-autopilot/knowledge/commands.json), [playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json)) trägt den Ein-Zeilen-Nutzen jedes Befehls und eine Reihe von Kombi-Playbooks; das Modell liest sie bei Bedarf, also kostet sie pro Prompt nichts. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Enthaltene Skills: `tutor` (geführte Tour) · `doctor` (prüfen, ob alles läuft) · `config` (stumm/Modi) · `evolve` (deine Belege zu Regeln destillieren) · `profile` (das Nutzen-Dashboard) · `whats-new` (neue Befehle und ungenutzte Skills, erklärt nach Nutzen).

## Voraussetzungen

Python 3.8+ für das volle Erlebnis. Ohne Python läuft der Autopilot im zustandslosen Modus: Kernverhalten intakt, Lernen pausiert.

## FAQ

**Werden meine Daten irgendwohin gesendet?** Nein. Null Telemetrie. Alles liegt in lokalen Dateien unter `~/.claude/command-autopilot/`, die du öffnen, prüfen und löschen kannst. Die Deinstallation entfernt alles.

**Verbirgt er etwas vor mir?** Nein. Frag Claude „was leitet dich gerade?“ oder bitte ihn, die Anweisung zu zeigen, die dieses Plugin einspeist, und er sagt sie dir vollständig: Die Regeln sind Klartext in [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules), und die Anleitung weist Claude ausdrücklich an, transparent zu sein, wann immer du fragst. Nichts an dem Plugin ist vor dir geheim.

**Wird er mich nerven?** Die harten Verträge sagen Nein: höchstens ein Vorschlag pro Antwort, derselbe Befehl höchstens einmal pro Sitzung, und Vorschläge, die du immer wieder wegwischst, verblassen von selbst. Mit „Autopilot stummschalten“ wird er komplett still.

**Was kostet es?** Rund 500 bis 600 Tokens an Regeln pro Nachricht im Dauerbetrieb (weniger im quiet-Modus, 0 wenn stummgeschaltet), plus einen kleinen, begrenzten Zuschlag (~140 Tokens) in Zügen, in denen installierte Skills relevant sind – ein Bruchteil eines Prozents eines 200k-Fensters. Den Regler hast du in der Hand.

**Funktioniert es in Claude Code im Web / für mein Team?** Ja: Binde seine Regeln mit einem einzigen Befehl in das `.claude/` deines Repos ein (`vendor-to-repo.sh`, siehe [Funktioniert in der Cloud und im Team](#funktioniert-in-der-cloud-und-im-team)). Cloud-Sitzungen klonen das Repo frisch und übernehmen sie, sodass jeder, der in diesem Repo arbeitet, sie bekommt.

**Ich habe kein Python, funktioniert es trotzdem?** Ja, im zustandslosen Modus: Das gesamte Kernverhalten funktioniert, nur die Lernschicht pausiert, bis Python 3.8+ verfügbar ist.

**Wie deinstalliere ich es?** Führe `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot` aus (oder bitte Claude darum) und lösche `~/.claude/command-autopilot/`. Es bleibt nichts zurück.

**Was unterscheidet das von ein paar Regeln in der CLAUDE.md?** Genau das haben wir zuerst versucht, zweimal. Regeln in der CLAUDE.md unterliegen konkurrierenden Anweisungen; die Hook-Einspeisung bei jedem Prompt ist die einzige Platzierung, von der wir nachweisen konnten, dass sie das Modell zu 100 % erreicht. Dieser Befund, zusammen mit dem Lern-Design ohne magische Schwellenwerte, ist der ganze Grund, warum das ein Plugin ist und kein Markdown-Schnipsel. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Mitmachen

**Erster PR in 5 Minuten:** Verbessere die Formulierung eines Vorschlags in `plugins/skill-autopilot/rules/*.txt` oder füge den Ein-Zeilen-Nutzen eines Befehls zu `plugins/skill-autopilot/knowledge/commands.json` hinzu, führe den passenden Schritt in [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) aus und reiche ein. README-Übersetzungen sind ebenso willkommen. Das Verhalten lebt in Textdateien, nicht im Code: siehe [docs/TUNING.md](docs/TUNING.md) für die Iterationsdisziplin.

MIT-lizenziert.
