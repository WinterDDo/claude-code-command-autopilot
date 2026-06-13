#!/usr/bin/env python3
"""Evidence collector. Records, never judges.

Two entry points (argv[2]):
  skill — PostToolUse(Skill): ground-truth record of a skill invocation.
  stop  — Stop: best-effort scan of the transcript tail for suggestion
          outcomes (AskUserQuestion accepted/dismissed), auto plan-mode
          entries (value ledger), habit tips delivered, and self-use traces.

Everything is enhancement-only: any parse failure exits silently. The
product keeps working if this file learns nothing.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apcommon as ap

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
HABITS = {"/clear": "clear", "/btw": "btw", "/rewind": "rewind", "/plan": "plan"}
# Recognize EVERY command in the KB (single source of truth), not a hard-coded
# subset — otherwise self-use of most commands is invisible to the learning loop.
# Longest-first so multi-word commands (code-review) win over prefixes.
_NAMES = sorted(ap.kb_command_names(PLUGIN_ROOT), key=len, reverse=True)
COMMAND_RE = re.compile(r"/(" + "|".join(re.escape(n) for n in _NAMES) + r")\b")
SCAN_TAIL_BYTES = 200_000


def record(state, data_dir, event_type, key, prompt_hint=""):
    ap.append_event(data_dir, {"type": event_type, "key": key, "hint": prompt_hint[:100]})
    state["evolve"]["events_since_distill"] = state["evolve"].get("events_since_distill", 0) + 1


def handle_skill(state, data_dir, payload):
    tool_input = payload.get("tool_input") or {}
    name = tool_input.get("skill") or tool_input.get("name") or ""
    if not name:
        return
    ap.bump(state["counters"], "skills", name, "invoked")
    record(state, data_dir, "skill_invoked", name, str(tool_input.get("args", ""))[:80])
    if not state["milestones"].get("first_skill_auto_used"):
        state["milestones"]["first_skill_auto_used"] = "pending"


def iter_new_transcript_lines(data_dir, payload):
    # Offsets live in their own file written ONLY by this script: the router's
    # concurrent state.json writes can never erase them and cause re-scanning.
    path = payload.get("transcript_path", "")
    sid = payload.get("session_id", "") or "unknown"
    if not path or not Path(path).is_file():
        return []
    offsets_path = data_dir / "offsets.json"
    try:
        offsets = json.loads(offsets_path.read_text(encoding="utf-8"))
    except Exception:
        offsets = {}
    offset = offsets.get(sid, 0)
    size = Path(path).stat().st_size
    if size <= offset:
        return []
    start = max(offset, size - SCAN_TAIL_BYTES)
    with open(path, "rb") as fh:
        fh.seek(start)
        chunk = fh.read().decode("utf-8", errors="ignore")
    offsets[sid] = size
    if len(offsets) > 50:
        offsets = dict(sorted(offsets.items())[-50:])
    tmp = offsets_path.with_name("offsets.%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(offsets), encoding="utf-8")
    os.replace(tmp, offsets_path)
    return chunk.splitlines()


def handle_stop(state, data_dir, payload):
    suggested, dismissed_all, answers = set(), False, []
    for raw in iter_new_transcript_lines(data_dir, payload):
        # tool_result lines also carry "type":"user"; file paths inside them
        # (src/export/x.js, app/context/y.ts) must never count as self-use.
        is_user = ('"type":"user"' in raw or '"type": "user"' in raw) and '"tool_result"' not in raw

        if '"name": "EnterPlanMode"' in raw or '"name":"EnterPlanMode"' in raw:
            record(state, data_dir, "value_auto_plan_mode", "/plan")
            if not state["milestones"].get("first_auto_plan_mode"):
                state["milestones"]["first_auto_plan_mode"] = "pending"

        if '"name": "AskUserQuestion"' in raw or '"name":"AskUserQuestion"' in raw:
            suggested.update(COMMAND_RE.findall(raw))
        if "questions have been answered" in raw or "has answered your questions" in raw:
            answers.extend(COMMAND_RE.findall(raw))
            if "User dismissed" in raw:
                dismissed_all = True

        # NOTE: we deliberately do NOT infer "a habit was taught" from prose
        # markers — that counted ordinary discussion of a command as teaching
        # (e.g. "/plan" mentioned beside the word "tip"). Only structural truth
        # is recorded: offers (AskUserQuestion), outcomes, and real self-use below.
        if is_user:
            for match in COMMAND_RE.findall(raw):
                cmd = "/" + match
                ap.bump(state["counters"], "commands", cmd, "self_used")
                if cmd in HABITS:
                    ap.bump(state["counters"], "habits", HABITS[cmd], "self_used")
                record(state, data_dir, "self_use_trace", cmd)

    for match in suggested:
        cmd = "/" + match
        ap.bump(state["counters"], "commands", cmd, "suggested")
        record(state, data_dir, "suggestion_made", cmd)
    accepted = {"/" + m for m in answers} if not dismissed_all else set()
    for cmd in accepted & {"/" + m for m in suggested}:
        ap.bump(state["counters"], "commands", cmd, "accepted")
        record(state, data_dir, "suggestion_accepted", cmd)
        if not state["milestones"].get("first_suggestion_accepted"):
            state["milestones"]["first_suggestion_accepted"] = "pending"
    if dismissed_all:
        for match in suggested:
            ap.bump(state["counters"], "commands", "/" + match, "dismissed")
            record(state, data_dir, "suggestion_dismissed", "/" + match)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    submode = sys.argv[2] if len(sys.argv) > 2 else "stop"
    data_dir = ap.data_dir_from_argv()
    state = ap.load_state(data_dir)
    if submode == "skill":
        handle_skill(state, data_dir, payload)
    else:
        handle_stop(state, data_dir, payload)
    ap.save_state(data_dir, state)
    print(json.dumps({}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(json.dumps({}))
