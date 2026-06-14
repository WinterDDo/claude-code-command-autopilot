# Command Autopilot for Claude Code

**Use all of Claude Code — not just the few commands you know.**

English | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Claude Code can fan out parallel agents, chase a goal on its own, run multi-step workflows, research across the web — and almost nobody uses any of it, because **you can't ask for what you don't know exists.** Command Autopilot watches what you're actually doing and surfaces the high-leverage move at the moment it would help — then learns which ones you keep. The small stuff (undo, context hygiene) it just handles; that's the floor, not the pitch. Open source, MIT, zero telemetry.

## What it makes possible

| The moment | Without Autopilot | With Autopilot |
|---|---|---|
| A big, multi-file, or repetitive job | You grind through it one step at a time | It offers to **fan out parallel agents / a Workflow** before starting — with the token cost, your call |
| A task that should just run to the finish | You babysit it turn by turn | It offers **/goal** so Claude works to the finish on its own |
| A question that needs real research | One shallow search | It runs **deep multi-source research** and hands you a cited answer |
| Skills you installed but forgot | They sit unused | It **uses them** and says which one just helped: "used your pdf skill — read the file directly" |
| You keep declining a suggestion | Most tools nag forever | It reads the room and drops that one — it learns *you* |
| The basics — undo, context, asides | You never learned the commands | Handled quietly: **/rewind** before any repair, **/clear** at topic switches, **/btw** for asides |

**What it actually sounds like:**

```text
You:    undo that — the file was better before
Claude: Before I attempt any repair: you can rewind to before that edit.
        Press Esc twice (/rewind) — it restores the files and the
        conversation together. Want me to wait?
```

New to the commands themselves? We also maintain [the plain-English Claude Code command cheat sheet](docs/claude-code-commands-cheatsheet.md) and [8 Claude Code workflows that save real work](docs/claude-code-workflows.md).

Claude Code has ~100 built-in slash commands plus every skill you've installed, and the most powerful ones — orchestration, parallelism, autonomy — are exactly the ones nobody discovers. Command Autopilot closes that gap with three moves:

1. **It surfaces the powerful move you'd never think to ask for.** Before a big, repetitive, or long-running task, it offers the high-leverage path — parallel agents, a Workflow, an autonomous /goal, deep research — with the trade-off, so you choose it instead of grinding the slow way.
2. **It does the rest itself, instead of recommending.** What Claude can do on its own it just does: big changes enter plan mode before any file is touched, preferences get written to memory, your installed skills get used (and it says which one helped). The safety basics (/rewind, /clear, /btw) are handed over at the exact moment, never as a lecture.
3. **It evolves with you.** Every suggestion you take or skip is local evidence. What you keep declining goes quiet; what helps gets offered earlier; roughly every 10 sessions it distills your usage into personalized rules — visible, evidence-backed, deletable.

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
