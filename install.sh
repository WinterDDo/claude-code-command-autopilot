#!/bin/sh
# Fallback installer for users who prefer the terminal over /plugin commands.
# The recommended path is still:
#   /plugin marketplace add WinterDDo/claude-code-command-autopilot
#   /plugin install command-autopilot@claude-code-command-autopilot
set -e
REPO_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

# Locate the claude CLI: PATH first, then the default install location
# (desktop-app users often have the binary without it being on PATH).
CLAUDE_BIN=$(command -v claude 2>/dev/null || true)
if [ -z "$CLAUDE_BIN" ] && [ -x "$HOME/.local/bin/claude" ]; then
  CLAUDE_BIN="$HOME/.local/bin/claude"
fi
if [ -z "$CLAUDE_BIN" ]; then
  echo "claude CLI not found (checked PATH and ~/.local/bin/claude)."
  echo "Install Claude Code first: https://code.claude.com"
  exit 1
fi

echo "Using claude at: $CLAUDE_BIN"
echo "Registering local marketplace..."
"$CLAUDE_BIN" plugin marketplace add "$REPO_DIR" || true
echo "Installing plugin..."
"$CLAUDE_BIN" plugin install command-autopilot@claude-code-command-autopilot

echo ""
echo "Done. Restart Claude Code, then say: \"give me the autopilot tour\""
echo "Requirements note: Python 3.8+ enables learning; without it the autopilot runs stateless."
