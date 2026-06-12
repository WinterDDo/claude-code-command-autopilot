# Contributing

Most valuable contributions, in order:

1. **Acceptance reports** — run [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) on your machine/language and report failures with the step number.
2. **Benefit-line and translation fixes** — `knowledge/commands.json`, `rules/core.*.txt`. Wording is the product.
3. **Playbooks** — must cite an official docs basis (see [docs/TUNING.md](docs/TUNING.md)).
4. **Code** — only with tests; `sh tests/run-tests.sh` must stay green.

Hard lines (PRs crossing these are closed): no regex intent detection in scripts, no mechanical judgment thresholds, no telemetry or network calls from hooks, no weakening of the one-suggestion contract or the /rewind safety net.

Behavior changes require a cold-start ACCEPTANCE.md pass; say so in the PR description.
