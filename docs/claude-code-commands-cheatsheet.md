# Every Claude Code command in plain English — the beginner cheat sheet

Claude Code has around 100 slash commands, and most tutorials explain them in terms of other commands. This cheat sheet does the opposite: for each Claude Code command, it tells you **the moment you need it** and **what you actually get**, in plain English. No jargon, no prior knowledge assumed.

It is generated from the curated knowledge base of the [Skill Autopilot plugin](../README.md) and kept fresh as Claude Code updates. (If you'd rather memorize none of these: install the plugin and it will use or hand you the right command at the right moment.)

## Undo and safety — the ones that save your work

| Command | The moment you need it | What you get |
|---|---|---|
| `/rewind` | Claude broke something, or you just don't like the result | One step back to before the damage — no manual repair. Shortcut: press **Esc twice** |
| `/diff` | You want to see what changed before committing | Every uncommitted change in one interactive view |

If you learn exactly one thing from this page, learn `/rewind`. Checkpoints are created automatically before every edit; most people lose work simply because nobody told them undo exists in Claude Code.

## Sessions and context — keep Claude fast and cheap

| Command | The moment you need it | What you get |
|---|---|---|
| `/clear` | Starting an unrelated task in a long session | A fresh start: the new task won't drag the old context's noise or cost |
| `/resume` | You want to continue yesterday's conversation | Reopens a past session exactly where it left off |
| `/btw <question>` | A side question pops up mid-task | An answer with zero pollution of your main thread |
| `/compact` | Context is heavy but the same task must continue | Frees space while you choose what the summary keeps |
| `/context` | The session feels slow or expensive | Shows exactly what is eating your context window |
| `/export` | The session produced something worth keeping | Saves the full transcript, not a lossy retelling |
| `/branch` | You want to try an alternative approach | A copy to experiment in; the main thread stays intact |
| `/fork <task>` | A side-task deserves its own worker | A background agent that inherits your whole conversation and reports back |

## Planning and control — before the big work starts

| Command | The moment you need it | What you get |
|---|---|---|
| `/plan` | Any big change (or press **Shift+Tab**) | Claude plans first and shows you; nothing is edited until you approve |
| `/goal <condition>` | Multi-step work with a clear finish line | Claude keeps working unprompted until your condition is met |
| `/model` | The task clearly mismatches the current model | The right brain for the job: depth for hard work, speed for rote work |
| `/effort` | A hard problem deserves deeper thinking | A reasoning-depth dial you control |
| `/advisor` | High-stakes work where a second opinion helps | A stronger model double-checks the work at key moments |
| `/fast` | You want quicker output | Same model, faster responses |

## Background and automation — work that runs without you

| Command | The moment you need it | What you get |
|---|---|---|
| `/background` | A long task is blocking you | It keeps running while you do something else |
| `/tasks` | You wonder how background work is going | Every background task's progress in one place |
| `/schedule` | A job should repeat on a timer | Set once; runs on schedule in the cloud (Claude can set this up for you) |
| `/workflows` | A multi-agent run is in flight | Live progress for the whole fleet |

## Review and quality

| Command | The moment you need it | What you get |
|---|---|---|
| `/review` | Before shipping a change | Bugs caught in your diff before they reach users |
| `/security-review` | The change touches anything sensitive | A security audit of pending changes |
| `/init` | First serious session in a new project | Claude learns your project once; every future session benefits |

## Troubleshooting and account

| Command | The moment you need it | What you get |
|---|---|---|
| `/doctor` | Claude Code itself misbehaves | Tells apart a broken installation from a broken project |
| `/mcp` | A connector fails or auth expires | Reconnect or re-authenticate in seconds |
| `/permissions` | The same safe command keeps asking for approval | No more repeated popups for commands you trust |
| `/usage` | Before a big run, or after a rate-limit warning | How much plan headroom is left |
| `/bug` | You hit a real Claude Code defect | A report filed with diagnostics attached, one command |

## Learning and review

| Command | The moment you need it | What you get |
|---|---|---|
| `/powerup` | You want to learn features hands-on | Interactive lessons with animated demos — better than docs |
| `/insights` | Wrapping up a substantial session | An analysis report of how the session went |
| `/recap` | You need a quick record | A one-line summary of the session |
| `/install-github-app` | Your public repo starts getting issues and PRs | @claude triages them for you on GitHub |

## Or memorize none of this

These commands are powerful and almost nobody learns them — that's the actual problem. [Skill Autopilot](../README.md) is a free, open-source plugin that closes the gap: what Claude can do itself it just does (big changes auto-enter plan mode), and what only you can press arrives as a clickable suggestion at the exact moment, with one line on why. It learns your habits and goes quiet. [Install takes 30 seconds.](../README.md#install)

See also: [8 Claude Code workflows that save real work](claude-code-workflows.md).
