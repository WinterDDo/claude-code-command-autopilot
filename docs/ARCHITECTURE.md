# Architecture

## Design philosophy (Karpathy-style)

0. **Cognition every turn, not a scenario library.** The autopilot does NOT carry a "if the task looks like X, suggest command Y" lookup table — that approach is brittle, endless to maintain, and the opposite of intelligent. Instead, every turn the model reads what the user is actually doing and reasons fresh: can I do this myself? would a higher-leverage capability make THIS task materially better? The knowledge base is *reference* (what exists, how to phrase its benefit), never a trigger table. This is why the rules are a short thinking discipline, not a catalog — and why fixing "it never suggested the powerful commands" meant *removing* the narrow triggers that gated capability-consideration, not adding more.
0b. **Single source of truth.** All command/leverage data lives only in `knowledge/commands.json`. Hooks derive their command sets from it at runtime (`apcommon.kb_command_names` / `kb_high_leverage`) — never a hard-coded parallel subset. A drift test enforces it. (This is why "/loop was missing" and why the tracker was blind to 91 of 117 commands — both were hand-picked subsets that fell out of sync.)
1. **The model is the runtime.** Intent, timing, and phrasing judgments belong to the model. Scripts only do state and IO — no keyword regex anywhere.
2. **Knowledge is data.** Command benefits, combo playbooks, and rule wording live in JSON/text. Tuning behavior means editing text, not code.
3. **The prompt is the weights.** The injected block is this system's learnable parameter. Self-evolution = gradient descent in prompt space: usage logs are training data, periodic distillation is the optimizer step, learned rules are weights, contradiction demotion is regularization, idle decay is forgetting.
4. **Thin harness, pay-per-use.** Hard token budget per prompt; the full knowledge base is lazy-loaded by the model (Read tool) only when recommending.
5. **Silence is the default for hygiene tips — but capability discovery is the opposite.** The silence-default governs low-value hygiene nudges. High-leverage capabilities the user doesn't know exist (Workflow, sub-agents, /goal, /loop, parallel /fork) are the product's core value and are surfaced via a near-mandatory CAPABILITY CHECKPOINT before multi-step/repetitive/long-horizon tasks — explicitly NOT gated by the silence-default, plus a once-ever proactive introduction. (We learned the hard way that a blanket silence-default suppressed the core feature entirely — even Claude itself ran Workflows without ever offering them.) The anti-nag valve here is per-capability: one the user keeps declining stops being offered. A hygiene suggestion needs a reason to exist. But high-leverage capabilities the user doesn't know exist (Workflow orchestration, sub-agents, /goal, parallel /fork) are the whole point of the product: the user can't ask for what they've never heard of. So the per-turn cognition actively asks "would a more effective capability fit THIS task?" and surfaces it — cheap+reversible ones it just uses; costly or control-handover ones it offers via AskUserQuestion before acting and waits. Evidence DOWN-ranks capabilities the user keeps declining; it is never a precondition for first exposure (a brand-new user has zero evidence for everything). Mechanical things are *contracts* (≤1 suggestion/response, instant mute), never *judgments* (no "dismissed twice → banned forever" thresholds).

## Empirical laws this design is built on

These came from two days of real testing on the founder's machine, and they are the project's moat:

1. **Per-prompt `UserPromptSubmit` injection is the only placement proven 100% reachable.** The same rules placed in CLAUDE.md / SessionStart lost twice to competing instructions (an auto-triggering skill won the behavioral slot). Rules must appear at the moment of competition.
2. **Built-in commands are user-typed only.** Hooks can't trigger them; the model can't run them (exceptions: /init, /review, /security-review via the Skill tool; plan mode via EnterPlanMode). Hence layer 2's popup design — and the popup's click result is transcript-visible, which becomes the learning signal.
3. **Cloud sessions load only repo-level config.** A checked-in `.claude/settings.json` is the only path to cloud and teams.
4. **Skills are signal-rich; commands are signal-poor.** Skill invocations pass through PostToolUse (ground truth); command usage is invisible to hooks (indirect popup evidence only).

## Dataflow

```
every prompt   UserPromptSubmit → run.sh → router.py
               = factory rules (mode-sliced) + learned rules (≤5) + evidence digest (≤80tk) + KB pointers
session start  SessionStart → session-start.py
               = state housekeeping, skills-index scan/diff, one-time announcements (first run, milestones,
                 KB updates, evolution window). Never carries behavior rules (law #1).
turn end       Stop → tracker.py             = transcript-tail scan: suggestions made/accepted/dismissed,
                                               auto plan-mode (value ledger), tips delivered, self-use traces
skill used     PostToolUse(Skill) → tracker.py = ground-truth skill invocation record
~10 sessions   evolve skill (model-executed)  = events.jsonl → learned.json (evidence-backed rules), archive events
on demand      profile / whats-new / config / doctor / tutor skills
```

## State (all local, ~/.claude/command-autopilot/)

- `state.json` — config, counters (commands/skills/habits), milestones, canary, sessions (7-day prune). Atomic writes, corrupt files self-heal (preserved as `.bad-*`).
- `events.jsonl` — the append-only evidence ledger; archived into `events-archive.jsonl` by evolve.
- `learned.json` — personalized rules with evidence metadata; max 5 in force; user-deletable.
- `skills-index.json` — per-user installed-skills scan, rebuilt each session.

## Degradation ladder

Full (python3) → stateless (`fallback-context.json`: core rules survive, learning paused) → muted (zero output, zero tokens). Every script path is wrapped: a hook must never surface an error to a beginner.

## Platform contracts

- `userConfig` answers surface to hook processes as `CLAUDE_PLUGIN_OPTION_*` env vars; session-start probes them ONCE to seed `state.json.config`, which stays authoritative afterwards (the config skill is the reliable lever either way).
- There is no `${CLAUDE_PLUGIN_DATA}` substitution in Claude Code; all personal data lives at the fixed path `~/.claude/command-autopilot/` (passed explicitly by hooks.json).
- UNVERIFIED: transcript JSONL format stability across CLI versions → tracker is enhancement-only; total parse failure costs learning, never function.
