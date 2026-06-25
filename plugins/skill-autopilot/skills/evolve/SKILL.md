---
name: evolve
description: Distill Skill Autopilot's accumulated usage evidence into personalized rules — the self-evolution step. Use when the autopilot announces an evolution window, or the user says "evolve", "学习一下我的习惯", "update your instincts", "distill autopilot".
---

# Evolution pass (prompt-space gradient descent)

You are updating this system's weights: the personalized rules injected into every prompt. Be conservative — a wrong learned rule costs the user on every message.

## Procedure

1. Read `~/.claude/command-autopilot/events.jsonl`. Also read `learned.json` if present (schema below).
2. Cluster events by task-type × command/skill. Look for consistent patterns, for example:
   - a command suggested repeatedly and consistently dismissed → candidate negative rule
   - a skill invoked on the same kind of task again and again → candidate positive rule ("invoke X early for Y-type tasks")
   - a habit self-used regularly → mastered, teaching for it should stop
3. Apply the discipline:
   - **Promote** only patterns with ≥3 consistent observations and no contradicting evidence → `status: "in_force"`.
   - **Demote** existing in_force rules contradicted by new evidence (decrement `evidence`; at 0, set `status: "candidate"`).
   - **Decay**: rules not reconfirmed for ~60 days → delete.
   - Max 5 in_force rules; each `text` ≤ 25 tokens, English, imperative, generic phrasing ("research-type tasks: offer /fork early").
   - NEVER write rules that override the safety net (/rewind) or the one-suggestion contract.
4. Write `learned.json`:

```json
{
  "updated": "<ISO>",
  "rules": [
    {"text": "...", "evidence": 4, "first": "<ISO>", "last": "<ISO>", "status": "in_force"}
  ]
}
```

5. Archive processed events — rotate FIRST to avoid racing concurrent appends: rename `events.jsonl` to `events-archive-<timestamp>.jsonl`, and only then read the renamed file for the distillation. New events land in a fresh `events.jsonl` untouched. (If you already read before rotating, rotate anyway and accept the tiny overlap.)
6. Report to the user in their language: what was learned (each rule + its evidence), what was demoted or deleted, and one line on what will change. If nothing met the bar, say so plainly — no fabricated learnings.
