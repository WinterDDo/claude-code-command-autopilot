#!/bin/sh
# Fallback installer for users who prefer the terminal over /plugin commands.
# The recommended path is still:
#   /plugin marketplace add WinterDDo/claude-code-command-autopilot
#   /plugin install command-autopilot@claude-code-command-autopilot
set -e
REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found. Install Claude Code first: https://code.claude.com"
  exit 1
fi

echo "Registering local marketplace..."
claude plugin marketplace add "$REPO_DIR" || true
echo "Installing plugin..."
claude plugin install command-autopilot@claude-code-command-autopilot

echo ""
echo "Done. Restart Claude Code, then say: \"give me the autopilot tour\""
echo "Requirements note: Python 3.8+ enables learning; without it the autopilot runs stateless."
