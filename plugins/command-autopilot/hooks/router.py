#!/usr/bin/env python3
"""UserPromptSubmit hook: assemble the [AUTOPILOT] context block.

Composition: factory rules (sections by mode) + learned in-force rules
+ evidence digest + knowledge pointers. Scripts never judge; they only
read state and format evidence. All judgment belongs to the model.
"""
import calendar
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apcommon as ap

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
DIGEST_MAX_CHARS = 600
LEARNED_MAX_RULES = 5


def parse_sections(text):
    sections, current = {}, None
    for line in text.splitlines():
        if line.startswith("#=SECTION "):
            current = line.split(" ", 1)[1].strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def days_ago(iso):
    try:
        then = calendar.timegm(time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ"))
        return max(0, int((time.time() - then) / 86400))
    except Exception:
        return None


def fmt_recency(iso):
    days = days_ago(iso)
    if days is None:
        return ""
    return "today" if days == 0 else "%dd ago" % days


def build_digest(state):
    lines = []
    for cmd, c in sorted(state["counters"].get("commands", {}).items()):
        bits = []
        for field in ("suggested", "accepted", "dismissed", "self_used"):
            if c.get(field):
                bits.append("%s %d" % (field.replace("_", "-"), c[field]))
        if bits:
            lines.append("%s: %s (%s)" % (cmd, ", ".join(bits), fmt_recency(c.get("last", ""))))
    for habit, h in sorted(state["counters"].get("habits", {}).items()):
        if h.get("tips_shown") or h.get("self_used"):
            lines.append("habit %s: tipped %d, self-used %d" % (habit, h.get("tips_shown", 0), h.get("self_used", 0)))
    skills = [(s, c) for s, c in state["counters"].get("skills", {}).items() if c.get("invoked")]
    skills.sort(key=lambda x: -x[1]["invoked"])
    for name, c in skills[:5]:
        lines.append("skill %s: invoked %d (%s)" % (name, c["invoked"], fmt_recency(c.get("last", ""))))
    digest = "\n".join("- " + l for l in lines)
    return digest[:DIGEST_MAX_CHARS]


def build_learned(data_dir):
    try:
        learned = json.loads((data_dir / "learned.json").read_text(encoding="utf-8"))
    except Exception:
        return ""
    # learned.json is model-written (evolve skill): tolerate malformed entries,
    # never let one bad rule crash the router into fallback forever.
    rules = [r for r in learned.get("rules", [])
             if isinstance(r, dict) and r.get("status") == "in_force" and r.get("text")]
    rules.sort(key=lambda r: -(r.get("evidence") or 0))
    return "\n".join("- %s (evidence: %d)" % (r["text"], r.get("evidence") or 0)
                     for r in rules[:LEARNED_MAX_RULES])


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    data_dir = ap.data_dir_from_argv()
    state = ap.load_state(data_dir)
    if state["config"].get("muted"):
        ap.emit(None)
        return

    lang = state["config"].get("language", "en")
    mode = state["config"].get("aggressiveness", "teaching")
    rules_path = PLUGIN_ROOT / "rules" / ("core.%s.txt" % lang)
    if not rules_path.exists():
        rules_path = PLUGIN_ROOT / "rules" / "core.en.txt"
    sections = parse_sections(rules_path.read_text(encoding="utf-8"))

    parts = [sections.get("core", ""), sections.get("safety", "")]
    if mode in ("normal", "teaching"):
        parts.append(sections.get("recommend", ""))
    if mode == "teaching":
        parts.append(sections.get("teach", ""))
    text = "\n".join(p for p in parts if p)

    if not state["config"].get("enable_plan_gate", True):
        text = "\n".join(l for l in text.splitlines() if "EnterPlanMode" not in l)

    text = text.replace("{KB}", str(PLUGIN_ROOT / "knowledge"))
    text = text.replace("{INDEX}", str(data_dir / "skills-index.json"))

    learned = build_learned(data_dir)
    if learned:
        header = "LEARNED — this user's confirmed patterns:" if lang == "en" else "已学到的该用户模式："
        text += "\n" + header + "\n" + learned
    digest = build_digest(state)
    if digest:
        header = ("EVIDENCE — this user's observed behavior (weigh it; current context wins):"
                  if lang == "en" else "行为证据（请权衡；当下语境优先）：")
        text += "\n" + header + "\n" + digest
    text += "\nRespond in the user's language."

    state["last_fired"] = {"ts": ap.now_iso(), "session_id": payload.get("session_id", "")}
    ap.touch_session(state, payload.get("session_id", ""))
    ap.save_state(data_dir, state)
    ap.emit(text)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        try:
            fallback = (Path(__file__).resolve().parent / "fallback-context.json").read_text(encoding="utf-8")
            print(fallback)
        except Exception:
            print(json.dumps({}))
