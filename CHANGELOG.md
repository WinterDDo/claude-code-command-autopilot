# Changelog

## 1.0.0 — 2026-06-23

- **Renamed to Skill Autopilot.** The product's center of gravity moved from "discover slash-commands" to "use the skills you've already installed." Repo, plugin, and docs are now `skill-autopilot` (GitHub redirects the old URL; stars/issues/PRs carry over). New install slug: `skill-autopilot@claude-code-skill-autopilot`. The internal state directory stays `~/.claude/command-autopilot/` so existing ledgers / learned rules are preserved (no migration needed).
- **Skills relevance surfacing (the new core).** Each turn, the `UserPromptSubmit` hook ranks your installed skills against your prompt by a cheap word-overlap and injects only the few most relevant skill *names* — the model reads each full description on demand and decides whether to use one. This reaches skills Claude Code dropped from context for being over its 1%-of-window skill budget: the perfect-but-forgotten skill that would otherwise be invisible to the model. Nothing is injected when nothing fits, and the same slice isn't re-injected turn after turn.
- **Honest framing — read this.** This release is new and experimental. The relevance ordering is attention-narrowing, **not** a verdict the model is told to trust — matching stays the model's job. Effectiveness is **not yet proven on real-world data**; the local ledger (which skills get surfaced and actually used) is how it will be measured and tuned. No effectiveness numbers are claimed; we've twice learned not to declare victory on simulation.
- **Nothing hidden, nothing sent.** Built on per-prompt hook injection (the only placement we could prove reaches the model reliably), a local skills index rebuilt at session start, and the existing local-only learning ledger. Zero telemetry; everything is local files you can read, audit, and delete. Ask Claude "what's guiding you?" any time.
- Carries forward the v0.7→v1.0 work: the unified skills+commands "better-move" menu, the first-task demo, deletion of the brittle code classifiers (matching is the model's job), and the local learning loop. 49 unit + 3 smoke tests green; `claude plugin validate` passes.

## 0.7.0 — 2026-06-17

- **Root cause found and fixed: why the menu almost never fired.** The proactive menu had surfaced ~4 times in the entire usage ledger. A controlled experiment — vary only the trigger's *framing*, hold the task and command-knowledge constant — showed why: firing is a FRAMING problem, not a knowledge problem. The model always knew *which* command fit; the old rule framed the menu as the assistant's own optional, default-silent, high-bar judgment, which collides with the model's trained "don't be presumptuous" disposition, so it resolved to silence. Reframing the *same* menu as the user's standing request (they installed this *because* they want to be shown these moves — presenting it fulfills that request) roughly doubled firing in the experiment, with no rise in false-fires.
- **The unlock rule is rewritten around that finding.** "BETTER-MOVE CHECK" is now framed as the user's standing request; the DEFAULT-SILENCE basis and the four-AND gate are gone; it explicitly judges the MOMENT, not the person (never goes quiet just because the user looks capable — forgetting the best move in the moment is universal, experts included). Net fewer tokens. Anti-nag valves kept: at most one surfacing per reply, "quiet"/"mute", "a move kept declining → stop offering it", plus a prominent first gate — if the user just declined or said to just proceed, never re-offer.
- **First-task demo — the install aha.** A new one-time `welcome` directive: on the user's first substantial task, the autopilot presents its menu so a brand-new user feels the value immediately. Locally it is a deterministic flag (armed on first run, injected by the router, cleared by the tracker once a menu actually fires — it keeps trying until it lands, then never again), adding no steady-state token cost. In the cloud (no persistent state) it fires per session on the first substantial message.
- **Validated before ship** (beginner + power-user personas × task cells): the first task fires; steady high-value moments fire ~80% including for a power user (the "judge the moment, not the person" goal); trivial asks, mid-task follow-ups, coupled work, and a just-declined task stay silent (the anti-nag floor held after removing default-silence). Honest residuals: a single turn is not literally 100% (the model is asked, not forced — a hook injects text, it cannot emit the menu itself; the first-task flag makes it cumulatively near-certain across the first turns), and a just-declined task still re-offers ~1-in-8. Simulated rates over-state production; real firing is now visible in the ledger (every menu logs as suggestion_made) and will be tuned from there.

## 0.6.0 — 2026-06-16

- Suggestions are now a MENU, not a single pick. When a high-value moment clears the bar, the better-move check presents the 2-4 genuinely-fitting high-leverage moves as a clickable choice (each: command + one-line payoff) plus "no, continue" — you see your options and choose, instead of being handed one. The gate is unchanged (default silence; only at genuine high-value moments), so it is not more frequent, just more useful when it does speak. This is the "show me my options" experience.
- Removed the v0.5.1 hardcoded /goal hint. A generalization eval showed the command-agnostic rule already recommends the right command across the whole surface (~88%), so the per-command hint was redundant; the menu surfaces /goal among the options on long autonomous tasks anyway. No per-command hardcoding.
- Validated (menu eval): presents good 3-4 item menus on big-build / long-autonomous / debugging / multi-independent / risky-op / ship; stays silent on trivial questions. Honest: leans slightly more proactive by design — an occasional menu on a borderline-trivial edit, and research stays conservative; the anti-nag valves (mute/quiet, decline-to-stop) are unchanged.

## 0.5.1 — 2026-06-16

- The better-move check's observable-signals list now explicitly names "a long task to drive autonomously to a PR (/goal)". So when you ask for a long task carried all the way to a finished PR, it reliably recommends /goal up front instead of leaving you to remember it. Validated: lifts /goal recommendation on that scenario from ~10/12 to 12/12 with no new false-positives, and no silence regressions. One phrase, no new machinery.

## 0.5.0 — 2026-06-15

- First-principles refocus: the co-pilot IS the per-turn prompt, not a pile of triggers. The whole value is a few well-calibrated words that make a capable model surface a better move when (and only when) one genuinely helps — for anyone, beginner to expert.
  - **The unlock rule is now a BETTER-MOVE CHECK, not a fan-out nudge.** Every turn, before committing to an approach, the model silently asks "is there a materially better move for THIS task?" — a command, combo, skill, workflow, OR a pattern from the user's own past. DEFAULT IS SILENCE; it surfaces at most one move, and only if it clears four AND-ed filters (concrete · not-already-chosen · materially better · non-obvious now), biased to observable moments (a risky/irreversible op, a fitting capability never used, visible repetition, being stuck). Cheap+reversible → just do it; costly/control-handover → RECOMMEND it as a clickable AskUserQuestion choice and let the user decide. This is what makes it valuable to experts too: recalling your OWN forgotten best practice at the moment it applies counts, and is often the best move.
  - **Removed the v0.4.x PostToolUse "moment-nudge" hook and its cloud-vendored sh.** A full day of real use showed it fired ~0 organically (it keyed on foreground subagent / plan-exit events the model rarely emits) while adding real complexity. The every-turn rule covers the same moment earlier and more reliably, so the hook was net redundant. Net change: the codebase got *simpler*.
- Honest scope: not "picks the optimal move every turn" (whether an expert's move was suboptimal isn't observable); a mostly-silent co-pilot that surfaces rarely and precisely on observable high-value moments, and gets quieter as it learns you're good. quiet/mute valve unchanged.

## 0.4.1 — 2026-06-14

- Cloud copilot is now present every turn, not just once. The vendored cloud hook injected the rules only at SessionStart — in a long session it aged out, so cloud never surfaced workflow/goal/loop. It now wires BOTH UserPromptSubmit (per-prompt, matching the local plugin) and SessionStart (guaranteed-to-run fallback) to one script that stamps the firing event into its output. Worst case = old behavior; best case = full per-prompt parity with local. Guard upgraded to use $CLAUDE_CODE_REMOTE: cloud always injects; locally with the plugin installed it stays silent (no double). Confirmed in a real cloud session (2026-06-14): the cloud runs the repo-committed UserPromptSubmit hook, so per-prompt parity is achieved, not just the fallback.

## 0.4.0
- Single source of truth, enforced. "/loop was missing" turned out to be a pattern: several hooks hard-coded their own command subsets that drifted from the knowledge base. Fixed all of them to derive from `knowledge/commands.json` at runtime:
  - Tracker now recognizes all 117 commands (was 26) — the learning loop was blind to self-use of 91 commands, including everything the user actually typed this session.
  - The one-time power-command intro now draws from the KB's leverage=high set (19 after cleanup, was a hard-coded 6).
  - Skill scan now also covers project-level `.claude/skills` (was user + plugins only).
- `leverage` flags cleaned up: demoted aliases and view/report commands so "high-leverage" means genuinely powerful capabilities.
- New `tests/test_kb_single_source.py` guards the invariant — if any hook's command set drifts from the KB, it goes red. Principle documented in TUNING.md and ARCHITECTURE.md.
- Playbooks expanded from 8 to a comprehensive verified set (same multi-agent method as the command catalog).

## 0.3.1
- Knowledge base completed: was a hand-picked 33; now the full official set of 117 commands, fetched from code.claude.com/docs and enriched (best-fit scenario + beginner benefit en/zh + leverage flag) by a multi-agent research pass with an adversarial verify. Fixes the root cause behind "/loop was missing" — the KB is now comprehensive, not a curated subset. The monthly kb-sync CI keeps it complete as Claude Code ships new commands.

## 0.3.0
- Makes the product's core promise actually fire: proactively surfacing high-leverage commands the user can't ask for because they don't know they exist. Two ways, both opt-out via quiet/mute:
  - **In the moment**: the unlock rule is now a CAPABILITY CHECKPOINT — before any multi-step, repetitive, or long-horizon task, bias toward surfacing Workflow / parallel /fork / /goal / /loop / background BEFORE doing it the slow way. It is explicitly NOT gated by the hygiene silence-default (which was suppressing it — even Claude itself ran Workflows all session without ever offering them).
  - **Once, proactively**: from the 2nd session on, a one-time introduction of the high-leverage commands you've never used (what each is, what it does for your work, how to try). Fires once ever; never nags.
- Added /loop to the knowledge base (was missing). whats-new skill now also covers never-used high-leverage built-in commands.
- Anti-regression intact: ≤1 suggestion/reply, a command you keep declining stops being offered, mute/quiet valves. Honest cost updated: ~300–500 tokens in teaching/normal (quiet ≈ 300), README adjusted to match.

## 0.2.2
- Cloud/web fix: suggestions no longer depend on the clickable AskUserQuestion popup, which does not reliably render in web/cloud sessions (interactive prompts are suppressed there — the likely reason cloud users never saw a suggestion). The guidance now degrades gracefully: clickable options where the environment renders them, plain-text questions otherwise. The suggestion reaches the user in every environment.

## 0.2.1
- Transparency fix: the injected block no longer says "apply silently; never quote or mention this block." That concealment framing clashed with the user's right to inspect their own tooling (and with the project's zero-telemetry, all-local stance). The guidance now says: apply naturally without narrating the plumbing, but answer honestly and in full whenever the user asks what's guiding you or about the plugin. Surfaced by Claude itself refusing to hide the block when asked directly — the right instinct, now baked into the rules. New FAQ entry documents it.

## 0.2.0
- Suggestion engine reframed from a scenario→command catalog to a per-turn cognitive discipline: the model reasons fresh about what each task needs; the knowledge base is reference, not triggers
- High-leverage capabilities (Workflow fan-out, sub-agents, /goal, parallel /fork) are now surfaced proactively — cheap+reversible ones used directly, costly/control-handover ones offered before acting and awaiting your choice
- Evidence now only down-ranks declined capabilities; it no longer gates first exposure (fixes the bug where nothing new was ever suggested)
- Removed the dedicated habit-teaching rotation that re-fired every session (the source of observed over-nagging, e.g. /plan tipped 5×); pointing out a command is now a once, in-context aside the model gates using the evidence digest, not a recurring checklist

## 0.1.0
Initial release.

- Per-prompt `[AUTOPILOT]` injection: do-don't-recommend, recommend-before-acting, four-habit teaching
- Evidence system: popup outcomes + skill invocations (ground truth) → local events ledger
- Self-evolution: evolve skill distills evidence into capped, evidence-backed, deletable learned rules
- Value dashboard (profile skill) with fully traceable numbers; milestone announcements
- Knowledge base: 32 command benefit lines (en/zh) + 8 verified combo playbooks; whats-new on updates
- Six skills: tutor, doctor, config, evolve, profile, whats-new
- Modes: teaching / normal / quiet / mute; stateless degradation without Python
- Cloud/team path via repo-level settings; portable prompt for no-hook surfaces
