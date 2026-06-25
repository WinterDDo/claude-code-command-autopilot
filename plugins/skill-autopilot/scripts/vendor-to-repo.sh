#!/bin/sh
# Vendor the cloud injection into a target repo's .claude/ so its cloud sessions
# run the current rules without depending on the marketplace cache.
# Re-run on every release to keep vendored repos current.
#
# Usage: vendor-to-repo.sh /path/to/target-repo
set -e
TARGET="$1"
[ -d "$TARGET" ] || { echo "usage: vendor-to-repo.sh /path/to/repo"; exit 1; }

PLUGIN=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
# regenerate the context from the single source of truth (rules/core.en.txt)
python3 "$PLUGIN/scripts/build-cloud-context.py" >/dev/null

mkdir -p "$TARGET/.claude"
cp "$PLUGIN/cloud/autopilot-context.json" "$TARGET/.claude/autopilot-context.json"
cp "$PLUGIN/cloud/autopilot-cloud.sh" "$TARGET/.claude/autopilot-cloud.sh"
chmod +x "$TARGET/.claude/autopilot-cloud.sh"

echo "Vendored into $TARGET/.claude/"
echo "Now ensure $TARGET/.claude/settings.json has these hooks:"
echo "  SessionStart    -> sh \"\$CLAUDE_PROJECT_DIR/.claude/autopilot-cloud.sh\" SessionStart"
echo "  UserPromptSubmit-> sh \"\$CLAUDE_PROJECT_DIR/.claude/autopilot-cloud.sh\" UserPromptSubmit"
echo "and drop any extraKnownMarketplaces/enabledPlugins for this plugin (the"
echo "marketplace path is the unreliable one this replaces)."
