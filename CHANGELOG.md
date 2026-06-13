# Changelog

## 0.3.0 — unreleased

- Makes the product's core promise actually fire: proactively surfacing high-leverage commands the user can't ask for because they don't know they exist. Two ways, both opt-out via quiet/mute:
  - **In the moment**: the unlock rule is now a CAPABILITY CHECKPOINT — before any multi-step, repetitive, or long-horizon task, bias toward surfacing Workflow / parallel /fork / /goal / /loop / background BEFORE doing it the slow way. It is explicitly NOT gated by the hygiene silence-default (which was suppressing it — even Claude itself ran Workflows all session without ever offering them).
  - **Once, proactively**: from the 2nd session on, a one-time introduction of the high-leverage commands you've never used (what each is, what it does for your work, how to try). Fires once ever; never nags.
- Added /loop to the knowledge base (was missing). whats-new skill now also covers never-used high-leverage built-in commands.
- Anti-regression intact: ≤1 suggestion/reply, a command you keep declining stops being offered, mute/quiet valves. Honest cost updated: ~300–500 tokens in teaching/normal (quiet ≈ 300), README adjusted to match.

## 0.2.2 — unreleased

- Cloud/web fix: suggestions no longer depend on the clickable AskUserQuestion popup, which does not reliably render in web/cloud sessions (interactive prompts are suppressed there — the likely reason cloud users never saw a suggestion). The guidance now degrades gracefully: clickable options where the environment renders them, plain-text questions otherwise. The suggestion reaches the user in every environment.

## 0.2.1 — unreleased

- Transparency fix: the injected block no longer says "apply silently; never quote or mention this block." That concealment framing clashed with the user's right to inspect their own tooling (and with the project's zero-telemetry, all-local stance). The guidance now says: apply naturally without narrating the plumbing, but answer honestly and in full whenever the user asks what's guiding you or about the plugin. Surfaced by Claude itself refusing to hide the block when asked directly — the right instinct, now baked into the rules. New FAQ entry documents it.

## 0.2.0 — unreleased

- Suggestion engine reframed from a scenario→command catalog to a per-turn cognitive discipline: the model reasons fresh about what each task needs; the knowledge base is reference, not triggers
- High-leverage capabilities (Workflow fan-out, sub-agents, /goal, parallel /fork) are now surfaced proactively — cheap+reversible ones used directly, costly/control-handover ones offered before acting and awaiting your choice
- Evidence now only down-ranks declined capabilities; it no longer gates first exposure (fixes the bug where nothing new was ever suggested)
- Removed the dedicated habit-teaching rotation that re-fired every session (the source of observed over-nagging, e.g. /plan tipped 5×); pointing out a command is now a once, in-context aside the model gates using the evidence digest, not a recurring checklist

## 0.1.0 — unreleased

Initial release.

- Per-prompt `[AUTOPILOT]` injection: do-don't-recommend, recommend-before-acting, four-habit teaching
- Evidence system: popup outcomes + skill invocations (ground truth) → local events ledger
- Self-evolution: evolve skill distills evidence into capped, evidence-backed, deletable learned rules
- Value dashboard (profile skill) with fully traceable numbers; milestone announcements
- Knowledge base: 32 command benefit lines (en/zh) + 8 verified combo playbooks; whats-new on updates
- Six skills: tutor, doctor, config, evolve, profile, whats-new
- Modes: teaching / normal / quiet / mute; stateless degradation without Python
- Cloud/team path via repo-level settings; portable prompt for no-hook surfaces
