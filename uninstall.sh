#!/bin/sh
set -e
echo "Uninstalling command-autopilot..."
claude plugin uninstall command-autopilot@claude-code-command-autopilot || true
echo "Removing local data (state, evidence, learned rules)..."
rm -rf "$HOME/.claude/command-autopilot"
echo "Note: plugin data under Claude Code's plugin-data directory is removed by Claude Code itself."
echo "Done. Nothing of the autopilot remains."
