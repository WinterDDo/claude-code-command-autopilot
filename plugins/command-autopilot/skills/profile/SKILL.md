---
name: profile
description: Show the Command Autopilot dashboard — what it did for you, before/after comparison, learned rules with evidence, mastered commands. Also drafts a feedback issue. Use when the user asks "what has the autopilot done", "show my profile", "驾驶舱", "autopilot 报告", "学到了什么", or wants to give feedback about suggestions.
---

# Autopilot dashboard

Every number MUST be traceable to a real entry in the data files. Never fabricate or extrapolate a value claim. If a number is zero, show zero.

## Data sources
Read from `~/.claude/command-autopilot/`: `state.json` (counters, milestones, config), `events.jsonl` + `events-archive.jsonl` (the ledger), `learned.json` (rules), `skills-index.json`.

## Report (user's language, compact)

1. **Value ledger** — counts from events: auto plan-mode entries, skills auto-invoked (top 3 by count, with names), suggestions accepted vs made. One line each, with the period covered.
2. **Before/after** — compare the oldest 7 days of events against the newest 7 (only if ≥14 days of data; otherwise say "still collecting"): self-used commands per week then vs now. This is the user's own growth, shown from their own data.
3. **Learned rules** — each in_force rule with its evidence count and last-confirmed date. If none: "still observing, first rules typically appear after ~10 sessions."
4. **Mastered** — habits with self-use evidence; note that teaching for them has naturally stopped.
5. **Controls** — one line: config skill to quiet/mute, evolve skill to re-distill, "delete rule N" works right here.

## Feedback draft
If the user is dissatisfied with any suggestion behavior, offer to draft a GitHub issue for `WinterDDo/claude-code-command-autopilot`: title, what happened, expected behavior, and (only with explicit consent) the relevant anonymized evidence lines. Show the draft; the user files it themselves.

## Rule deletion
"Delete rule N" → remove it from learned.json, confirm in one line.
