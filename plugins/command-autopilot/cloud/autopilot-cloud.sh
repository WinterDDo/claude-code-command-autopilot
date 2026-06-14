#!/bin/sh
# Vendored cloud injection for Command Autopilot.
# Committed into a repo's .claude/ so cloud sessions get the current rules
# WITHOUT depending on the marketplace cache (which does not auto-refresh).
#
# Wired to BOTH UserPromptSubmit (per-prompt — keeps the copilot present every
# turn, like the local plugin) and SessionStart (guaranteed-to-run fallback).
# $1 = the hook event name; we stamp it into the output so it matches.
#
# Guard: stay silent only when NOT in cloud AND the full user-scope plugin is
# installed (it takes over locally — no double injection). In cloud
# ($CLAUDE_CODE_REMOTE=true) always inject; on a machine without the plugin,
# inject too.
if [ "$CLAUDE_CODE_REMOTE" != "true" ] && [ -d "$HOME/.claude/plugins/cache/claude-code-command-autopilot" ]; then
  exit 0
fi

EVENT="${1:-UserPromptSubmit}"
DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
CTX="$DIR/autopilot-context.json"
[ -f "$CTX" ] || exit 0
# one context file serves both events: swap hookEventName to the firing event
sed "s/\"hookEventName\": \"[^\"]*\"/\"hookEventName\": \"$EVENT\"/" "$CTX"
exit 0
