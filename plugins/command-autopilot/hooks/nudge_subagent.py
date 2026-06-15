"""Moment-nudge — the in-the-moment half of the capability checkpoint.

The turn-start rule block gets buried by the time the model is deep in a task, so
a static reminder loses to "just do the work". This fires at the behavioral moment
instead, keyed on STRUCTURAL FACTS (never a task classification):
  - the model spawned a subagent (Agent/Task) — it reached for independent help, or
  - the model just exited plan mode (ExitPlanMode) — it finished planning a
    multi-step task and is about to execute it.
Either way, surface the higher-leverage parallel path BEFORE it grinds the pieces
serially. Once per session; silent in quiet/mute. Stdlib only; no-op without Python.
"""
import json
import sys

import apcommon as ap

# The matcher in hooks.json (Agent|Task|ExitPlanMode) is intentionally a little
# broad to cover version differences in the subagent tool's name; gate exactly
# here so the matcher can't fire the nudge on the TaskCreate/TaskList/etc. family.
TRIGGER_TOOLS = {"Agent", "Task", "ExitPlanMode"}

NUDGE = (
    "[AUTOPILOT] You're about to take on substantial, multi-part work. Before doing the "
    "pieces one by one: if they are (a) independent of each other's output, or (b) the "
    "same operation repeated across many items, you MUST offer ONCE to run them at once "
    "— parallel /fork or a Workflow fan-out (faster, more tokens, the user's call) — "
    "state the tradeoff and wait. Skip this ONLY if the rest is genuinely one coupled "
    "thread where each step needs the previous step's result — then continue silently."
)


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}

    tool = payload.get("tool_name") or payload.get("toolName") or ""
    if tool not in TRIGGER_TOOLS:
        return  # broad matcher caught a non-trigger tool (e.g. TaskCreate) — ignore

    data_dir = ap.data_dir_from_argv()
    state = ap.load_state(data_dir)

    cfg = state.get("config", {})
    if cfg.get("muted") or cfg.get("aggressiveness") == "quiet":
        return  # the unlock track is off in quiet/mute — respect the valve

    session_id = payload.get("session_id") or ""
    nudge_state = state.setdefault("nudge", {})
    if session_id and nudge_state.get("last_session") == session_id:
        return  # one moment-nudge per session — never a repeating, naggy reminder
    nudge_state["last_session"] = session_id
    ap.save_state(data_dir, state)
    ap.append_event(data_dir, {"type": "leverage_nudge", "key": tool})

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": NUDGE,
        }
    }))


if __name__ == "__main__":
    main()
