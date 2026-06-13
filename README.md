# Command Autopilot for Claude Code

**Use 100% of Claude Code while memorizing zero commands.**

English | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

A free Claude Code plugin for beginners: it knows all the commands so you don't have to. If you've ever lost work you didn't know you could undo, or watched Claude charge into a big change you wished it had planned first — this is for you. Open source, MIT, zero telemetry: everything it learns lives in local files you can open and delete, and saying "mute autopilot" always works.

## What actually changes after you install it

| The moment | Without Autopilot | With Autopilot |
|---|---|---|
| Claude breaks something | You don't know undo exists; Claude keeps "fixing" | It hands you **/rewind** first: press Esc twice, back to before the damage |
| You ask for something big | Claude starts editing immediately | It **plans first, automatically** — nothing changes until you approve |
| You switch topics mid-session | Old context slows you down and burns money | Clickable choice appears: continue / clean start / spin off — each with the reason |
| Skills you installed sit unused | You forgot you have them | It uses them and tells you: "used your pdf skill — read the file directly" |
| There's a far more powerful way you've never heard of | You grind through the slow path | It surfaces the high-leverage capability (parallel agents, Workflow) at the right moment, with the trade-off |
| You keep dismissing a suggestion | Most tools nag forever | It reads the room and goes quiet — it learns *you* |

**What it actually sounds like:**

```text
You:    undo that — the file was better before
Claude: Before I attempt any repair: you can rewind to before that edit.
        Press Esc twice (/rewind) — it restores the files and the
        conversation together. Want me to wait?
```

New to the commands themselves? We also maintain [the plain-English Claude Code command cheat sheet](docs/claude-code-commands-cheatsheet.md) and [8 Claude Code workflows that save real work](docs/claude-code-workflows.md).

Claude Code has ~100 built-in slash commands, plus every skill you've installed. Beginners know almost none of them — so they lose work they could have rewound with one keystroke, burn context they could have cleared, and watch Claude charge into big edits that deserved a plan first.

Command Autopilot fixes this with three moves:

1. **It does, instead of recommending.** What Claude can do itself, it just does: big changes automatically enter plan mode before any file is touched, preferences get written to memory, your installed skills get used (and it tells you, in one line, which skill just helped you).
2. **It hands you the command before the moment, never after.** Commands only you can press (/rewind, /clear...) arrive as clickable choices at the exact fork they resolve — each with a one-line benefit, so you know why you're pressing it.
3. **It evolves with you.** Every suggestion you accept or ignore is local evidence. The autopilot reads the room: what you keep dismissing goes quiet, what helps you gets offered earlier, and roughly every 10 sessions it distills your usage into personalized rules — visible, evidence-backed, deletable.

It never runs through a fixed checklist of tips. It reasons about each turn, points something out at most once when it genuinely helps, and otherwise stays quiet. The goal is that you stop noticing it.

**Just browsing?** Paste [portable/PROMPT.md](portable/PROMPT.md) into claude.ai or any assistant — the core behavior, nothing installed, 60 seconds.

## Install

**Easiest — let Claude install it for you.** Copy this whole block, paste it into any Claude Code conversation, press enter:

```
Install the Command Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Run: claude plugin install command-autopilot@claude-code-command-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude runs the install and handles the edge cases (CLI not on PATH, etc.) for you. No terminal knowledge needed.

<details>
<summary>Manual alternatives</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

If `claude` is not found, use `~/.local/bin/claude` instead, or run `./install.sh` from a clone of this repo.

**Inside a Claude Code CLI session** (the `/plugin` command is not available in the desktop app):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

Then restart Claude Code (quit fully — hooks load at startup) and ask Claude: **"check that the autopilot is working"** — the built-in doctor confirms everything is firing end-to-end. Then take the 2-minute tour: "give me the autopilot tour".

**Not working?**
- Suggestions never appear → you must fully quit and reopen; hooks only load at startup.
- `/plugin` not found → the desktop app has no `/plugin` command; use the copy-paste install above.
- Anything else → ask Claude to "run the autopilot doctor" and paste its output into an [issue](https://github.com/WinterDDo/claude-code-command-autopilot/issues).

## Updating

Ask Claude: **"update the command-autopilot plugin to the latest version."** It runs the three steps below for you.

Doing it by hand (or if you hit "already at the latest version" — that means your local copy of the marketplace is stale, so refresh it *first*):

```sh
claude plugin marketplace update claude-code-command-autopilot   # refresh the catalog from GitHub
claude plugin update command-autopilot@claude-code-command-autopilot
```

Then fully quit and reopen Claude Code — rules and hooks load at startup. (Cloud sessions always clone the repo fresh, so they pick up new versions on their own.)

## See it work in 2 minutes

1. Ask for something big: *"design and build a statistics feature for this project."* → Claude enters **plan mode by itself**, before touching any file. Reject the plan; nothing changed.
2. Have it create a throwaway file, then say *"undo that."* → Its first reaction is to hand you **/rewind (Esc Esc)**, not to patch forward.

## What it will never do

- **No telemetry.** All evidence lives in local files you can open, audit, and delete. Uninstall removes everything.
- **No nagging.** Hard contracts: at most one suggestion per response, the same command at most once per session, and "quiet" or full mute is one sentence away ("mute autopilot"). Repeatedly dismissed suggestions fade out on their own.
- **No fabricated value.** Ask "what has the autopilot done for me" — every number in the report traces to a real logged event.

## Honest cost

The autopilot injects its rules into every prompt: roughly 300–500 tokens depending on mode (quiet ≈ 300, muted = 0). That is the price of the one placement that demonstrably works. You control the dial: `teaching` → `normal` → `quiet` → mute.

## Works in the cloud and for teams

Cloud sessions don't load your personal config — so for Claude Code on the web and teammates, commit this to your repository's `.claude/settings.json` (full snippet in [templates/team-settings.json](templates/team-settings.json)):

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

Everyone who trusts the workspace gets the autopilot — locally and in cloud sessions. (Cloud caveats: settings prompts don't fire there, so defaults apply; learning state resets per cloud session.)

## How it works (for the curious)

One `UserPromptSubmit` hook assembles the context every message: a short thinking discipline + your learned rules + a compact evidence digest. There is **no scenario→command lookup table** — the model reasons fresh each turn about what *your* task needs; the knowledge base is reference, not triggers. Scripts only record and compress — **all judgment belongs to the model**, which is why there are no magic thresholds anywhere. A knowledge base ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) carries every command's one-line benefit and 8 combo playbooks; the model reads it on demand, so it costs nothing per prompt. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills included: `tutor` (guided tour) · `doctor` (verify it's working) · `config` (mute/modes) · `evolve` (distill your evidence into rules) · `profile` (the value dashboard) · `whats-new` (new commands & unused skills, explained by benefit).

## Requirements

Python 3.8+ for the full experience. Without Python, the autopilot runs in stateless mode: core behavior intact, learning paused.

## FAQ

**Is my data sent anywhere?** No. Zero telemetry. Everything lives in local files at `~/.claude/command-autopilot/` that you can open, audit, and delete. Uninstalling removes it all.

**Does it hide anything from me?** No. Ask Claude "what's guiding you?" or to show the instruction this plugin injects, and it will tell you in full — the rules are plain text in [`plugins/command-autopilot/rules/`](plugins/command-autopilot/rules), and the guidance explicitly tells Claude to be transparent whenever you ask. Nothing about the plugin is secret from you.

**Will it nag me?** Hard contracts say no: at most one suggestion per response, the same command at most once per session, and suggestions you keep dismissing fade out on their own. Saying "mute autopilot" silences it completely.

**What does it cost?** It injects roughly 300–500 tokens of rules per message depending on mode (quiet ≈ 300, muted = 0). That's the honest price of reliability; you control the dial.

**Does it work in Claude Code on the web / for my team?** Yes — commit two small blocks to your repo's `.claude/settings.json` ([snippet here](templates/team-settings.json)) and everyone who trusts the workspace gets it, cloud sessions included.

**I don't have Python — does it still work?** Yes, in stateless mode: all core behavior works, only the learning layer pauses until Python 3.8+ is available.

**How do I uninstall?** Run `claude plugin uninstall command-autopilot@claude-code-command-autopilot` (or ask Claude to do it), delete `~/.claude/command-autopilot/`. Nothing remains.

**How is this different from just writing rules in CLAUDE.md?** We tried that first — twice. Rules in CLAUDE.md lose to competing instructions; per-prompt hook injection is the only placement we could prove reaches the model 100% of the time. That finding, plus the no-magic-thresholds learning design, is the whole reason this is a plugin and not a markdown snippet. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contributing

**First PR in 5 minutes:** improve one suggestion's wording in `plugins/command-autopilot/rules/*.txt`, or add a command's one-line benefit to `plugins/command-autopilot/knowledge/commands.json`, run the matching step in [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md), submit. README translations are equally welcome. Behavior lives in text files, not code — see [docs/TUNING.md](docs/TUNING.md) for the iteration discipline.

MIT licensed.
