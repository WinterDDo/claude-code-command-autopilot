# 8 Claude Code workflows that save real work

Individual Claude Code commands are useful; combined, they change how you work. These eight workflows are the combinations we verified against the official docs and use daily. Each one answers a real "how do I..." moment for beginners and power users alike.

(They're encoded in the [Command Autopilot plugin](../README.md)'s knowledge base — install it and the right workflow gets suggested at the right moment, with reasons.)

## 1. The safe big change

**When:** any refactor, feature, or edit you'd hate to get wrong.

1. Ask for the change — with [Command Autopilot](../README.md), Claude enters **plan mode** by itself (or press Shift+Tab)
2. Review and approve the plan — nothing is touched until you do
3. `/goal tests pass and the feature works` — Claude keeps working until it's true
4. `/diff` to inspect what changed
5. Anything wrong? `/rewind` (Esc twice) — back to before the damage

**Why it works:** a review gate, a finish line, and an undo button around every risky change.

## 2. Long session stamina

**When:** the session gets slow or expensive but you can't stop now.

1. `/context` — see what's eating the window
2. At a natural milestone: `/compact focus on the decisions and the remaining steps`
3. Continue the same task with room to breathe

**Why it works:** you outlive the context window without losing the decisions that matter — and *you* choose what the summary keeps, instead of letting automatic compaction guess.

## 3. Parallel exploration

**When:** two plausible approaches, no obvious winner.

1. `/branch` — try option A yourself in a copy of the conversation
2. `/fork try option B with a different architecture` — a background agent that knows your full context chases option B
3. Your main thread keeps moving; compare results when the fork reports back

**Why it works:** you stop betting the session on a guess.

## 4. The pre-heavy-task tuneup

**When:** about to start something genuinely hard or expensive.

1. `/usage` — check you have the headroom
2. `/model` or `/effort` — match the brain to the job
3. `/advisor on` — a stronger model reviews the work at key moments
4. Now start

**Why it works:** expensive work begins with the right setup and a second pair of eyes, instead of discovering the mismatch halfway through.

## 5. The clean finish

**When:** a task is done and another is coming.

1. `/export` — keep the full record
2. `/recap` (one line) or `/insights` (full retrospective)
3. `/clear` — clean desk; the old session stays reachable via `/resume`

**Why it works:** a record, a summary, and a fresh start — the next task doesn't pay for the last one's context.

## 6. Aside isolation

**When:** a random question pops into your head mid-task.

1. `/btw what's the time difference between São Paulo and Beijing?`

That's the whole workflow. The answer appears in an overlay; your session's context never hears about it.

## 7. Unattended work

**When:** the work doesn't need you watching.

1. `/schedule check my repo's new issues every morning and triage them` — Claude can set this up for you
2. `/background` — detach a long-running task
3. `/tasks` — check progress whenever you come back

**Why it works:** work continues while you sleep; you just read results.

## 8. The mass change

**When:** the same edit needs to happen across dozens of files.

1. Describe the repetitive change once
2. Claude orchestrates parallel agents across the codebase
3. `/workflows` — watch the fleet's progress live

**Why it works:** a hundred-file chore becomes one instruction plus a progress bar.

---

**Want these suggested automatically?** [Command Autopilot](../README.md) watches for the moments above and offers the right move with a one-line reason — then learns which ones you actually use. Free, MIT, zero telemetry. See also: [the plain-English command cheat sheet](claude-code-commands-cheatsheet.md).
