# Command Autopilot for Claude Code

**Use 100% of Claude Code while memorizing zero commands.**

[中文文档](README.zh.md)

Claude Code has ~100 built-in slash commands, plus every skill you've installed. Beginners know almost none of them — so they lose work they could have rewound with one keystroke, burn context they could have cleared, and watch Claude charge into big edits that deserved a plan first.

Command Autopilot fixes this with three moves:

1. **It does, instead of recommending.** What Claude can do itself, it just does: big changes automatically enter plan mode before any file is touched, preferences get written to memory, your installed skills get used (and it tells you, in one line, which skill just helped you).
2. **It hands you the command before the moment, never after.** Commands only you can press (/rewind, /clear...) arrive as clickable choices at the exact fork they resolve — each with a one-line benefit, so you know why you're pressing it.
3. **It evolves with you.** Every suggestion you accept or ignore is local evidence. The autopilot reads the room: what you keep dismissing goes quiet, what helps you gets offered earlier, and roughly every 10 sessions it distills your usage into personalized rules — visible, evidence-backed, deletable.

It teaches exactly **four habits** (/clear, /btw, /rewind, plan mode), each at most a few times, then goes quiet. The goal is that you stop noticing it.

## Install

**Easiest — let Claude install it for you.** Copy this whole block, paste it into any Claude Code conversation, press enter:

```
Install the Command Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Run: claude plugin install command-autopilot@claude-code-command-autopilot
4. Show me both success confirmations, then remind me to fully quit and reopen Claude Code.
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

Then restart Claude Code (quit fully — hooks load at startup) and try the 2-minute tour: ask Claude "give me the autopilot tour".

## See it work in 2 minutes

1. Ask for something big: *"design and build a statistics feature for this project."* → Claude enters **plan mode by itself**, before touching any file. Reject the plan; nothing changed.
2. Have it create a throwaway file, then say *"undo that."* → Its first reaction is to hand you **/rewind (Esc Esc)**, not to patch forward.

## What it will never do

- **No telemetry.** All evidence lives in local files you can open, audit, and delete. Uninstall removes everything.
- **No nagging.** Hard contracts: at most one suggestion per response, the same command at most once per session, and "quiet" or full mute is one sentence away ("mute autopilot"). Repeatedly dismissed suggestions fade out on their own.
- **No fabricated value.** Ask "what has the autopilot done for me" — every number in the report traces to a real logged event.

## Honest cost

The autopilot injects its rules into every prompt: roughly 250–450 tokens depending on mode (quiet ≈ 230, muted = 0). That is the price of the one placement that demonstrably works. You control the dial: `teaching` → `normal` → `quiet` → mute.

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

No Claude Code at all? [portable/PROMPT.md](portable/PROMPT.md) carries the core rules to claude.ai, Cursor, or any assistant — paste and go.

## How it works (for the curious)

One `UserPromptSubmit` hook assembles the context every message: factory rules + your learned rules + a compact evidence digest. Scripts only record and compress — **all judgment belongs to the model**, which is why there are no magic thresholds anywhere. A knowledge base ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) carries every command's one-line benefit and 8 combo playbooks; the model reads it on demand, so it costs nothing per prompt. Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills included: `tutor` (guided tour) · `doctor` (verify it's working) · `config` (mute/modes) · `evolve` (distill your evidence into rules) · `profile` (the value dashboard) · `whats-new` (new commands & unused skills, explained by benefit).

## Requirements

Python 3.8+ for the full experience. Without Python, the autopilot runs in stateless mode: core behavior intact, learning paused.

## Contributing

Behavior lives in text files, not code — most improvements are wording changes to `rules/*.txt` or entries in `knowledge/*.json`. Read [docs/TUNING.md](docs/TUNING.md) for the iteration discipline, run [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) before proposing behavior changes.

MIT licensed.
