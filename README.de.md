# Command Autopilot für Claude Code

**Nutze 100 % von Claude Code, ohne dir einen einzigen Befehl zu merken.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | Deutsch

Gemacht für alle, die Claude Code benutzen, aber die `/`-Befehle noch nie angefasst haben. Wenn du schon einmal Arbeit verloren hast, ohne zu wissen, dass du sie hättest zurückholen können, oder zugesehen hast, wie Claude sich in eine große Änderung stürzt, die du dir lieber erst geplant gewünscht hättest: Das hier ist für dich.

## Was sich nach der Installation tatsächlich ändert

| Der Moment | Ohne Autopilot | Mit Autopilot |
|---|---|---|
| Claude macht etwas kaputt | Du weißt nicht, dass es ein Rückgängig gibt; Claude „repariert“ weiter | Er reicht dir zuerst **/rewind**: zweimal Esc drücken, und du bist zurück vor dem Schaden |
| Du bittest um etwas Großes | Claude fängt sofort an zu ändern | Er **plant zuerst, automatisch**: Nichts ändert sich, bis du zustimmst |
| Du wechselst mitten in der Sitzung das Thema | Alter Kontext bremst dich und kostet Geld | Eine klickbare Auswahl erscheint: weitermachen / frisch starten / auslagern, jeweils mit Begründung |
| Deine installierten Skills liegen brach | Du hast vergessen, dass du sie hast | Er nutzt sie und sagt es dir: „dein pdf-Skill kam zum Einsatz: Datei direkt gelesen“ |
| Du wischst einen Vorschlag immer wieder weg | Die meisten Tools nerven ewig | Er versteht den Wink und wird still: Er lernt *dich* kennen |

Claude Code hat rund 100 eingebaute Slash-Befehle, dazu jeden Skill, den du installiert hast. Einsteiger kennen fast keinen davon: Sie verlieren Arbeit, die ein einziger Tastendruck zurückgeholt hätte, verbrennen Kontext, den sie hätten aufräumen können, und sehen zu, wie Claude sich in große Änderungen stürzt, die erst einen Plan verdient hätten.

Command Autopilot löst das mit drei Kniffen:

1. **Er macht, statt zu empfehlen.** Was Claude selbst tun kann, tut er einfach: Große Änderungen gehen automatisch in den Planmodus, bevor irgendeine Datei angefasst wird, Vorlieben wandern ins Gedächtnis, deine installierten Skills werden genutzt (und er sagt dir in einer Zeile, welcher Skill dir gerade geholfen hat).
2. **Er reicht dir den Befehl vor dem Moment, nie danach.** Befehle, die nur du drücken kannst (/rewind, /clear...), erscheinen als klickbare Auswahl genau an der Weggabelung, die sie auflösen, jeweils mit dem Nutzen in einer Zeile, damit du weißt, warum du drückst.
3. **Er entwickelt sich mit dir.** Jeder Vorschlag, den du annimmst oder ignorierst, ist ein lokaler Beleg. Der Autopilot liest die Stimmung: Was du immer wieder wegwischst, verstummt, was dir hilft, kommt früher, und ungefähr alle 10 Sitzungen destilliert er deine Nutzung zu persönlichen Regeln: sichtbar, belegt, löschbar.

Er bringt dir genau **vier Gewohnheiten** bei (/clear, /btw, /rewind, Planmodus), jede höchstens ein paar Mal, dann wird er still. Das Ziel ist, dass du ihn gar nicht mehr bemerkst.

## Installation

**Am einfachsten: Lass Claude die Installation für dich erledigen.** Kopiere diesen ganzen Block, füge ihn in eine beliebige Claude-Code-Unterhaltung ein und drücke Enter:

```
Installiere das Command-Autopilot-Plugin für mich:
1. Finde mein claude-CLI: Probiere `command -v claude`; falls es nicht im PATH ist, probiere `~/.local/bin/claude`
   (der übliche Ort unter macOS/Linux). Verwende bei Bedarf in den nächsten Schritten den vollen Pfad.
2. Führe aus: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Führe aus: claude plugin install command-autopilot@claude-code-command-autopilot
4. Zeig mir beide Erfolgsbestätigungen und erinnere mich dann daran, Claude Code komplett zu beenden und neu zu öffnen.
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

Starte Claude Code danach neu (komplett beenden: Hooks laden beim Start) und probiere die 2-Minuten-Tour: Frag Claude „gib mir die Autopilot-Tour“.

## In 2 Minuten in Aktion erleben

1. Bitte um etwas Großes: *„Entwirf und baue eine Statistik-Funktion für dieses Projekt.“* → Claude geht **von selbst in den Planmodus**, bevor er eine Datei anfasst. Lehne den Plan ab; nichts hat sich geändert.
2. Lass ihn eine Wegwerf-Datei erstellen und sag dann *„mach das rückgängig.“* → Seine erste Reaktion ist, dir **/rewind (Esc Esc)** zu reichen, statt vorwärts zu flicken.

## Was er niemals tun wird

- **Keine Telemetrie.** Alle Belege liegen in lokalen Dateien, die du öffnen, prüfen und löschen kannst. Die Deinstallation entfernt alles.
- **Kein Genörgel.** Harte Verträge: höchstens ein Vorschlag pro Antwort, derselbe Befehl höchstens einmal pro Sitzung, und „leise“ oder komplett stumm ist nur einen Satz entfernt („Autopilot stummschalten“). Wiederholt weggewischte Vorschläge verblassen von selbst.
- **Kein erfundener Nutzen.** Frag „was hat der Autopilot für mich getan“: Jede Zahl im Bericht lässt sich auf ein echtes, protokolliertes Ereignis zurückführen.

## Die ehrlichen Kosten

Der Autopilot speist seine Regeln in jeden Prompt ein: rund 250 bis 450 Tokens je nach Modus (leise ≈ 230, stumm = 0). Das ist der Preis für die eine Platzierung, die nachweislich funktioniert. Den Regler hast du in der Hand: `teaching` → `normal` → `quiet` → stumm.

## Funktioniert in der Cloud und im Team

Cloud-Sitzungen laden deine persönliche Konfiguration nicht. Für Claude Code im Web und für Teamkollegen committest du deshalb Folgendes in die `.claude/settings.json` deines Repositories (vollständiger Ausschnitt in [templates/team-settings.json](templates/team-settings.json)):

```json
{
  "extraKnownMarketplaces": {
    "claude-code-command-autopilot": {
      "source": { "source": "github", "repo": "WinterDDo/claude-code-command-autopilot" }
    }
  },
  "enabledPlugins": { "command-autopilot@claude-code-command-autopilot": true }
}
```

Jeder, der dem Arbeitsbereich vertraut, bekommt den Autopiloten: lokal und in Cloud-Sitzungen. (Cloud-Einschränkungen: Einstellungsdialoge erscheinen dort nicht, also gelten die Standardwerte; der Lernstand wird pro Cloud-Sitzung zurückgesetzt.)

Gar kein Claude Code? [portable/PROMPT.md](portable/PROMPT.md) trägt die Kernregeln zu claude.ai, Cursor oder jedem anderen Assistenten: einfügen, loslegen.

## Wie es funktioniert (für Neugierige)

Ein einziger `UserPromptSubmit`-Hook baut bei jeder Nachricht den Kontext zusammen: Werksregeln + deine gelernten Regeln + ein kompakter Beleg-Auszug. Skripte zeichnen nur auf und komprimieren: **Das gesamte Urteilsvermögen liegt beim Modell**, deshalb gibt es nirgendwo magische Schwellenwerte. Eine Wissensbasis ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) enthält den Ein-Zeilen-Nutzen jedes Befehls und 8 Kombi-Playbooks; das Modell liest sie bei Bedarf, also kostet sie pro Prompt nichts. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Enthaltene Skills: `tutor` (geführte Tour) · `doctor` (prüfen, ob alles läuft) · `config` (stumm/Modi) · `evolve` (deine Belege zu Regeln destillieren) · `profile` (das Nutzen-Dashboard) · `whats-new` (neue Befehle und ungenutzte Skills, erklärt nach Nutzen).

## Voraussetzungen

Python 3.8+ für das volle Erlebnis. Ohne Python läuft der Autopilot im zustandslosen Modus: Kernverhalten intakt, Lernen pausiert.

## FAQ

**Werden meine Daten irgendwohin gesendet?** Nein. Null Telemetrie. Alles liegt in lokalen Dateien unter `~/.claude/command-autopilot/`, die du öffnen, prüfen und löschen kannst. Die Deinstallation entfernt alles.

**Wird er mich nerven?** Die harten Verträge sagen Nein: höchstens ein Vorschlag pro Antwort, derselbe Befehl höchstens einmal pro Sitzung, und Vorschläge, die du immer wieder wegwischst, verblassen von selbst. Mit „Autopilot stummschalten“ wird er komplett still.

**Was kostet es?** Er speist je nach Modus rund 250 bis 450 Tokens an Regeln pro Nachricht ein (leise ≈ 230, stumm = 0). Das ist der ehrliche Preis für Verlässlichkeit; den Regler hast du in der Hand.

**Funktioniert es in Claude Code im Web / für mein Team?** Ja: Committe zwei kleine Blöcke in die `.claude/settings.json` deines Repos ([Ausschnitt hier](templates/team-settings.json)), und jeder, der dem Arbeitsbereich vertraut, bekommt es, Cloud-Sitzungen eingeschlossen.

**Ich habe kein Python, funktioniert es trotzdem?** Ja, im zustandslosen Modus: Das gesamte Kernverhalten funktioniert, nur die Lernschicht pausiert, bis Python 3.8+ verfügbar ist.

**Wie deinstalliere ich es?** Führe `claude plugin uninstall command-autopilot@claude-code-command-autopilot` aus (oder bitte Claude darum) und lösche `~/.claude/command-autopilot/`. Es bleibt nichts zurück.

**Was unterscheidet das von ein paar Regeln in der CLAUDE.md?** Genau das haben wir zuerst versucht, zweimal. Regeln in der CLAUDE.md unterliegen konkurrierenden Anweisungen; die Hook-Einspeisung bei jedem Prompt ist die einzige Platzierung, von der wir nachweisen konnten, dass sie das Modell zu 100 % erreicht. Dieser Befund, zusammen mit dem Lern-Design ohne magische Schwellenwerte, ist der ganze Grund, warum das ein Plugin ist und kein Markdown-Schnipsel. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Mitmachen

Das Verhalten lebt in Textdateien, nicht im Code: Die meisten Verbesserungen sind Formulierungsänderungen in `rules/*.txt` oder Einträge in `knowledge/*.json`. Lies [docs/TUNING.md](docs/TUNING.md) für die Iterationsdisziplin und arbeite [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) durch, bevor du Verhaltensänderungen vorschlägst. Übersetzungen der Gewohnheitskarte und der READMEs sind der freundlichste erste PR.

MIT-lizenziert.
