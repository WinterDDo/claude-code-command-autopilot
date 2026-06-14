#!/bin/sh
# Vendored cloud injection for Command Autopilot.
# Committed into a repo's .claude/ so cloud sessions get the current rules
# WITHOUT depending on the marketplace cache (which does not auto-refresh).
#
# Guard: if the full user-scope plugin is installed on THIS machine, do nothing
# and let it take over (avoids double injection locally). In cloud — where the
# user-scope plugin is not present — this emits the vendored rules instead.
[ -d "$HOME/.claude/plugins/cache/claude-code-command-autopilot" ] && exit 0

DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
CTX="$DIR/autopilot-context.json"
[ -f "$CTX" ] && cat "$CTX"
exit 0
