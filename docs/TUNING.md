# Tuning manual (the official iteration discipline)

Behavior lives in text, not code. This file is how maintainers and contributors evolve it without breaking it.

## What you edit, per kind of change

| You want to... | Edit | Code change? |
|---|---|---|
| Make a rule fire more/less reliably | `rules/core.en.txt` + `core.zh.txt` (keep both in sync) | No |
| Add/fix a command benefit line | `knowledge/commands.json` | No |
| Add a combo playbook | `knowledge/playbooks.json` (must cite an official-docs basis in the PR) | No |
| Change teach phrasing | `rules/*.txt` TEACH section | No |
| Change what evidence is collected | `hooks/tracker.py` | Yes — tests required |
| Change injection composition/budget | `hooks/router.py` | Yes — tests required |

## The iteration loop (validated on this project's own history)

1. Make ONE wording change at a time.
2. `sh tests/run-tests.sh` — must stay green.
3. Restart Claude Code, run the relevant steps of [ACCEPTANCE.md](ACCEPTANCE.md) **cold-start** (rules load at startup; testing in a warm session proves nothing).
4. **One failure → tune the wording and retest. The same step failing twice in a row → it's a design problem, not a wording problem. Stop editing text and rethink the mechanism.**
5. Token check: `python3 plugins/skill-autopilot/hooks/router.py <tmpdir> <<< '{"prompt":"x"}' | wc -c` — teaching mode must stay under ~2300 chars (~470 tokens).

## Single source of truth (a hard rule)

Command and leverage data lives in exactly one place: `knowledge/commands.json`. Hooks must **never** hard-code a parallel list of commands — derive at runtime via `apcommon.kb_command_names()` / `apcommon.kb_high_leverage()`. We learned this the hard way: a hand-picked 33-command list shipped with /loop missing, and separate hard-coded subsets in the tracker (26 commands) and the power-intro (6) silently went blind to most of the catalog. `tests/test_kb_single_source.py` guards the invariant — if a subset drifts from the KB, it goes red. When Claude Code ships new commands, update only `commands.json` (the monthly kb-sync CI opens that PR); everything else follows.

## Hard lines (do not cross in any PR)

- No keyword/regex intent detection in scripts. The model judges; scripts record.
- No mechanical judgment thresholds ("ignored N times → stop"). Contracts yes (≤1 suggestion/response, mute), judgments no.
- No telemetry, no network calls from hooks. Ever.
- The /rewind safety offer and the one-suggestion contract cannot be weakened by learned rules or config.
- Every value claim shown to users must trace to an events.jsonl line.

## Shipping learnings back to factory defaults

Maintainers who use the autopilot daily: when your own `learned.json` contains a rule that is clearly universal (not personal), generalize it into `rules/core.*.txt` or a playbook in the next minor release — ship the learnings, never the data.

## Keeping the knowledge base fresh

`kb-sync.yml` checks the official commands documentation monthly and opens an issue when it drifts from `knowledge/commands.json`. Update the JSON, bump `version` (e.g. `2026.07`), release as a minor — installed users get a whats-new announcement automatically via the kb_version change.
