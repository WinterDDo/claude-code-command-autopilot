#!/bin/sh
# Vendored cloud moment-nudge for Command Autopilot (Layer 2 — the in-the-moment
# half of the capability checkpoint). Committed into a repo's .claude/ so cloud
# sessions get it WITHOUT the marketplace cache.
#
# Wired to PostToolUse with matcher "Agent|Task|ExitPlanMode": fires the instant
# the model spawns a subagent or finishes planning a multi-step task, and surfaces
# the parallel/fan-out option BEFORE it grinds independent work serially.
#
# Same guard as autopilot-cloud.sh: stay silent only when NOT in cloud AND the
# full user-scope plugin is installed (it handles this locally). In cloud
# ($CLAUDE_CODE_REMOTE=true) always inject.
if [ "$CLAUDE_CODE_REMOTE" != "true" ] && [ -d "$HOME/.claude/plugins/cache/claude-code-command-autopilot" ]; then
  exit 0
fi

IN=$(cat)

# The settings matcher already restricts to Agent|Task|ExitPlanMode; re-check the
# exact tool_name defensively so a broad match on the TaskCreate/TaskList family
# can never fire the nudge.
case "$IN" in
  *'"tool_name":"Agent"'*|*'"tool_name": "Agent"'*) : ;;
  *'"tool_name":"Task"'*|*'"tool_name": "Task"'*) : ;;
  *'"tool_name":"ExitPlanMode"'*|*'"tool_name": "ExitPlanMode"'*) : ;;
  *) exit 0 ;;
esac

# Once per session (best-effort; cloud sessions are ephemeral): marker keyed by id.
SID=$(printf '%s' "$IN" | sed -n 's/.*"session_id"[ ]*:[ ]*"\([^"]*\)".*/\1/p' | head -1)
MARK="${TMPDIR:-/tmp}/autopilot-nudge.${SID:-nosid}"
[ -f "$MARK" ] && exit 0
: > "$MARK" 2>/dev/null || true

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"[AUTOPILOT] You're about to take on substantial, multi-part work. Before doing the pieces one by one: if they are (a) independent of each other's output, or (b) the same operation repeated across many items, you MUST offer ONCE to run them at once (parallel /fork or a Workflow fan-out: faster, more tokens, the user's call), state the tradeoff, and wait. Skip this ONLY if the rest is genuinely one coupled thread where each step needs the previous step's result; then continue silently."}}
JSON
exit 0
