# Skill Autopilot for Claude Code

**Use the skills you've installed — not just the ones you remember.**

English | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

You install skills to extend Claude Code — then forget which ones you have, or when they fit. And it gets *worse* as you install more: past Claude Code's skill budget, it silently drops the descriptions of the skills you use least, so the perfect skill for *this* task can be invisible to the model. **Skill Autopilot surfaces the installed skills most relevant to what you're doing, each turn — so a fitting one is in front of you instead of forgotten.** It also lays out the high-leverage moves that fit a big or risky task (parallel agents, a Workflow, an autonomous /goal, deep research) as a menu you pick from, and handles the small stuff (undo, context hygiene) quietly. New and experimental — open source, MIT, zero telemetry, local-first.

## What it makes possible

| The moment | Without Autopilot | With Autopilot |
|---|---|---|
| A big, multi-file, or repetitive job | You grind through it one step at a time | It lays out a **menu of faster paths** (parallel agents, a Workflow, /background) before starting — with the trade-offs, you pick |
| A task that should just run to the finish | You babysit it turn by turn | It offers **/goal** so Claude works to the finish on its own |
| A question that needs real research | One shallow search | It runs **deep multi-source research** and hands you a cited answer |
| Skills you installed but forgot | They sit unused — or get dropped from context once you're over budget | It **surfaces the ones relevant to your task**, so a fitting skill is in front of the model |
| You keep declining a suggestion | Most tools nag forever | It reads the room and drops that one — it learns *you* |
| The basics — undo, context, asides | You never learned the commands | Handled quietly: **/rewind** before any repair, **/clear** at topic switches, **/btw** for asides |

**What it actually sounds like:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

New to the commands themselves? We also maintain [the plain-English Claude Code command cheat sheet](docs/claude-code-commands-cheatsheet.md) and [8 Claude Code workflows that save real work](docs/claude-code-workflows.md).

Claude Code runs on the skills and commands you've installed — but the right one rarely surfaces at the right moment, and a large skill library makes it *worse* (over budget, Claude Code drops the least-used skills' descriptions from context). Skill Autopilot closes that gap with three moves:

1. **It surfaces the skills that fit — right when they fit.** Each turn it ranks your installed skills against what you're actually asking and puts the most relevant ones in front of the model (by name; the model reads the full description on demand) — including ones Claude Code dropped from context for being over budget. And when several high-leverage moves fit a big or risky task — parallel agents, a Workflow, an autonomous /goal, deep research — it lays them out as a menu and you pick.
2. **It does the rest itself, instead of recommending.** What Claude can do on its own it just does: big changes enter plan mode before any file is touched, preferences get written to memory, a fitting installed skill gets used. The safety basics (/rewind, /clear, /btw) are handed over at the exact moment, never as a lecture.
3. **It learns to stay out of your way.** Every suggestion you skip is local evidence — what you keep declining goes quiet, so it never becomes a nag. (Deeper personalization — leaning into the moves *you* specifically favor — is on the roadmap; today's win is precision and silence, not pretending it already knows you.)

It never runs through a fixed checklist of tips. It reasons about each turn, points something out at most once when it genuinely helps, and otherwise stays quiet. The goal is that you stop noticing it.

**Just browsing?** Paste [portable/PROMPT.md](portable/PROMPT.md) into claude.ai or any assistant — the core behavior, nothing installed, 60 seconds.

## Install

**Easiest — let Claude install it for you.** Copy this whole block, paste it into any Claude Code conversation, press enter:

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude runs the install and handles the edge cases (CLI not on PATH, etc.) for you. No terminal knowledge needed.

<details>
<summary>Manual alternatives</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

If `claude` is not found, use `~/.local/bin/claude` instead, or run `./install.sh` from a clone of this repo.

**Inside a Claude Code CLI session** (the `/plugin` command is not available in the desktop app):

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

Then restart Claude Code (quit fully — hooks load at startup) and ask Claude: **"check that the autopilot is working"** — the built-in doctor confirms everything is firing end-to-end. Then take the 2-minute tour: "give me the autopilot tour".

**Not working?**
- Suggestions never appear → you must fully quit and reopen; hooks only load at startup.
- `/plugin` not found → the desktop app has no `/plugin` command; use the copy-paste install above.
- Anything else → ask Claude to "run the autopilot doctor" and paste its output into an [issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues).

## Updating

Ask Claude: **"update the Skill Autopilot plugin to the latest version."** It runs the three steps below for you.

Doing it by hand (or if you hit "already at the latest version" — that means your local copy of the marketplace is stale, so refresh it *first*):

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
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

The autopilot injects its rules into every prompt: roughly 500–600 tokens in steady state (less in `quiet`, 0 when muted). On turns where installed skills are relevant it adds their names — a small, bounded extra (~140 tokens), capped, and nothing on turns where none fit. Against a 200k context window that's a fraction of a percent. You control the dial: `teaching` → `normal` → `quiet` → mute.

## Works in the cloud and for teams

Cloud sessions don't load your personal plugins, and they don't refresh the marketplace cache — so the reliable way to get the autopilot in Claude Code on the web and for teammates is to **vendor its rules into your repo**: commit a small `.claude/autopilot-context.json` (the rules) plus `.claude/autopilot-cloud.sh`, and wire `SessionStart` + `UserPromptSubmit` hooks to it in your repo's `.claude/settings.json`. From a clone of this repo, one command copies the files and prints the exact hook lines:

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

New cloud sessions clone your repo fresh, so they pick up the rules automatically — for everyone who works in that repo. (Cloud caveat: the learning state is per-session there; the in-the-moment menu still works.)

## How it works (for the curious)

One `UserPromptSubmit` hook assembles the context every message: a short thinking discipline + the installed skills most relevant to your prompt + your learned rules + a compact evidence digest. The skill surfacing is deliberately dumb-and-honest: at session start it builds a local index of your installed skills, and each turn it ranks them by a cheap word-overlap with your prompt and injects only the few most relevant *names* (the model reads each full description on demand and decides whether to use one) — nothing is injected when nothing fits. There is **no scenario→command lookup table** and no similarity scorer the model is told to trust — the model reasons fresh each turn about what *your* task needs; the knowledge base is reference, not triggers. Scripts only record and compress — **all judgment belongs to the model**, which is why there are no magic thresholds anywhere. A knowledge base ([commands.json](plugins/skill-autopilot/knowledge/commands.json), [playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json)) carries every command's one-line benefit and a set of combo playbooks; the model reads it on demand, so it costs nothing per prompt. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills included: `tutor` (guided tour) · `doctor` (verify it's working) · `config` (mute/modes) · `evolve` (distill your evidence into rules) · `profile` (the value dashboard) · `whats-new` (new commands & unused skills, explained by benefit).

## Requirements

Python 3.8+ for the full experience. Without Python, the autopilot runs in stateless mode: core behavior intact, learning paused.

## FAQ

**Is my data sent anywhere?** No. Zero telemetry. Everything lives in local files at `~/.claude/command-autopilot/` that you can open, audit, and delete. Uninstalling removes it all.

**Does it hide anything from me?** No. Ask Claude "what's guiding you?" or to show the instruction this plugin injects, and it will tell you in full — the rules are plain text in [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules), and the guidance explicitly tells Claude to be transparent whenever you ask. Nothing about the plugin is secret from you.

**Will it nag me?** Hard contracts say no: at most one suggestion per response, the same command at most once per session, and suggestions you keep dismissing fade out on their own. Saying "mute autopilot" silences it completely.

**What does it cost?** Roughly 500–600 tokens of rules per message in steady state (less in quiet, 0 when muted), plus a small bounded extra (~140 tokens) on turns where installed skills are relevant — a fraction of a percent of a 200k window. You control the dial.

**Does it work in Claude Code on the web / for my team?** Yes — vendor its rules into your repo's `.claude/` with one command (`vendor-to-repo.sh`, see [Works in the cloud and for teams](#works-in-the-cloud-and-for-teams)). Cloud sessions clone the repo fresh and pick them up, so everyone who works in that repo gets it.

**I don't have Python — does it still work?** Yes, in stateless mode: all core behavior works, only the learning layer pauses until Python 3.8+ is available.

**How do I uninstall?** Run `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot` (or ask Claude to do it), delete `~/.claude/command-autopilot/`. Nothing remains.

**How is this different from just writing rules in CLAUDE.md?** We tried that first — twice. Rules in CLAUDE.md lose to competing instructions; per-prompt hook injection is the only placement we could prove reaches the model 100% of the time. That finding, plus the no-magic-thresholds learning design, is the whole reason this is a plugin and not a markdown snippet. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contributing

**First PR in 5 minutes:** improve one suggestion's wording in `plugins/skill-autopilot/rules/*.txt`, or add a command's one-line benefit to `plugins/skill-autopilot/knowledge/commands.json`, run the matching step in [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md), submit. README translations are equally welcome. Behavior lives in text files, not code — see [docs/TUNING.md](docs/TUNING.md) for the iteration discipline.

MIT licensed.
