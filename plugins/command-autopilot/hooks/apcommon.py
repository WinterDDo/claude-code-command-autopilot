"""Shared state helpers for command-autopilot hooks. Stdlib only."""
import calendar
import json
import os
import sys
import time
from pathlib import Path

SCHEMA = 1
SESSION_RETENTION_DAYS = 7

DEFAULT_STATE = {
    "schema": SCHEMA,
    "config": {
        "aggressiveness": "teaching",
        "language": "en",
        "enable_plan_gate": True,
        "muted": False,
    },
    "first_run_done": False,
    "kb_version": "",
    "counters": {"commands": {}, "skills": {}, "habits": {}},
    "milestones": {},
    "evolve": {"events_since_distill": 0, "last_distill": ""},
    "last_fired": {"ts": "", "session_id": ""},
    "last_review": "",
    "sessions": {},
}


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def data_dir_from_argv():
    raw = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else ""
    # An unsubstituted "${CLAUDE_PLUGIN_DATA}" literal means the harness did not
    # expand the variable; fall back rather than creating a directory named "${...}".
    if not raw or "$" in raw or "{" in raw:
        path = Path.home() / ".claude" / "command-autopilot"
    else:
        path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_state(data_dir):
    path = data_dir / "state.json"
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(state, dict) or state.get("schema") != SCHEMA:
            raise ValueError("schema mismatch")
    except FileNotFoundError:
        state = json.loads(json.dumps(DEFAULT_STATE))
    except Exception:
        try:
            path.rename(path.with_name("state.json.bad-%d" % int(time.time())))
        except Exception:
            pass
        state = json.loads(json.dumps(DEFAULT_STATE))
    for key, value in DEFAULT_STATE.items():
        state.setdefault(key, json.loads(json.dumps(value)))
    return state


def save_state(data_dir, state):
    path = data_dir / "state.json"
    # Per-process tmp name: the async tracker and the router may write
    # concurrently; a shared tmp file could publish a truncated state.
    tmp = path.with_name("state.json.%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def append_event(data_dir, event):
    event.setdefault("ts", now_iso())
    with open(data_dir / "events.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def touch_session(state, session_id):
    if not session_id:
        return
    sessions = state.setdefault("sessions", {})
    sessions.setdefault(session_id, {"first_seen": now_iso()})["last_seen"] = now_iso()
    cutoff = time.time() - SESSION_RETENTION_DAYS * 86400
    for sid in list(sessions):
        try:
            # timestamps are UTC; calendar.timegm parses them as UTC (mktime would use local time)
            seen = calendar.timegm(time.strptime(sessions[sid]["last_seen"], "%Y-%m-%dT%H:%M:%SZ"))
            if seen < cutoff:
                del sessions[sid]
        except Exception:
            del sessions[sid]


def bump(counters, group, key, field):
    entry = counters.setdefault(group, {}).setdefault(key, {})
    entry[field] = entry.get(field, 0) + 1
    entry["last"] = now_iso()


def emit(context_text=None):
    # Default ensure_ascii=True: \u escapes survive any stdout codepage
    # (Windows ANSI locales would crash on raw CJK) and decode identically.
    if context_text:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context_text,
            }
        }))
    else:
        print(json.dumps({}))
