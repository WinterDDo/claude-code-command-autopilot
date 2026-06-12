#!/usr/bin/env python3
"""SessionStart hook: state housekeeping only — never carries behavior rules.

Builds the per-user skills index, detects knowledge-base updates and newly
installed skills, surfaces one-time announcements (first run, milestones,
evolution window). Behavioral rules live in router.py's per-prompt injection,
the only placement proven to reach the model reliably.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apcommon as ap

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
EVOLVE_EVENT_THRESHOLD = 30  # cost-control constant: when to suggest a distillation pass
SKILL_SCAN_LIMIT = 400


def parse_frontmatter(path):
    name, description = path.parent.name, ""
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:30]
        in_fm = False
        for line in lines:
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm and line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            if in_fm and line.startswith("description:"):
                description = line.split(":", 1)[1].strip()[:120]
    except Exception:
        pass
    return name, description


def scan_skills():
    skills, seen = [], set()
    roots = [
        (Path.home() / ".claude" / "skills", "user"),
        (Path.home() / ".claude" / "plugins", "plugin"),
    ]
    count = 0
    for root, source in roots:
        if not root.is_dir():
            continue
        for skill_md in root.glob("**/SKILL.md"):
            count += 1
            if count > SKILL_SCAN_LIMIT:
                break
            name, description = parse_frontmatter(skill_md)
            if name in seen:
                continue
            seen.add(name)
            skills.append({"name": name, "description": description, "source": source})
    skills.sort(key=lambda s: s["name"])
    return skills


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    data_dir = ap.data_dir_from_argv()
    state = ap.load_state(data_dir)
    ap.touch_session(state, payload.get("session_id", ""))

    # One-time probe: plugin userConfig answers surface as CLAUDE_PLUGIN_OPTION_*
    # env vars. Seed config from them once; state.json stays authoritative after.
    if not state.get("user_config_seeded"):
        state["user_config_seeded"] = True
        for key, allowed in (("aggressiveness", {"teaching", "normal", "quiet"}),
                             ("language", {"en", "zh"}),
                             ("enable_plan_gate", {"true", "false"})):
            value = (os.environ.get("CLAUDE_PLUGIN_OPTION_" + key)
                     or os.environ.get(("CLAUDE_PLUGIN_OPTION_" + key).upper()) or "").strip().lower()
            if value in allowed:
                state["config"][key] = value == "true" if value in ("true", "false") else value

    notes = []
    lang = state["config"].get("language", "en")
    zh = lang == "zh"

    # Skills index + diff
    index_path = data_dir / "skills-index.json"
    old_names = set()
    try:
        old_names = {s["name"] for s in json.loads(index_path.read_text(encoding="utf-8"))["skills"]}
    except Exception:
        pass
    skills = scan_skills()
    index_path.write_text(json.dumps({"generated": ap.now_iso(), "skills": skills}, ensure_ascii=False, indent=1), encoding="utf-8")
    new_names = [s["name"] for s in skills if s["name"] not in old_names]
    if old_names and new_names:
        joined = ", ".join(new_names[:5])
        notes.append(("[AUTOPILOT one-time] User installed new skill(s) since last session: %s. "
                      "When natural, mention ONE of them with what it can do for them.") % joined)

    # Knowledge-base version change -> whats-new announcement
    try:
        kb_version = json.loads((PLUGIN_ROOT / "knowledge" / "commands.json").read_text(encoding="utf-8")).get("version", "")
    except Exception:
        kb_version = ""
    if kb_version and state.get("kb_version") and kb_version != state["kb_version"]:
        notes.append("[AUTOPILOT one-time] The command knowledge base was updated to %s. "
                     "When natural, offer the whats-new skill to show what is newly possible." % kb_version)
    state["kb_version"] = kb_version

    # First run
    if not state.get("first_run_done"):
        if zh:
            notes.append("[AUTOPILOT one-time] 这是 Command Autopilot 安装后的第一个会话。"
                         "用两句话自我介绍（自动执行能力 + 动作前递命令），并提议运行 tutor skill 做 2 分钟引导。仅此一次，不要说教。")
        else:
            notes.append("[AUTOPILOT one-time] First session since Command Autopilot was installed. "
                         "Introduce it in two sentences (silent automation + commands handed over before the moment), "
                         "and offer the tutor skill for a 2-minute tour. Once only, no lecturing.")
        state["first_run_done"] = True

    # Milestones recorded by tracker but not yet announced
    pending = [k for k, v in state.get("milestones", {}).items() if v == "pending"]
    for key in pending:
        notes.append("[AUTOPILOT one-time] Milestone reached: %s. Celebrate in ONE line and say what it means." % key)
        state["milestones"][key] = "announced"

    # Evolution window (cost control, not judgment)
    if state["evolve"].get("events_since_distill", 0) >= EVOLVE_EVENT_THRESHOLD:
        notes.append("[AUTOPILOT one-time] Enough usage evidence has accumulated. When natural, "
                     "offer to run the evolve skill to distill it into personalized rules.")
        state["evolve"]["events_since_distill"] = 0  # re-arm after one announcement

    # Print BEFORE saving: if stdout fails, the one-time flags are not yet
    # consumed and the announcements survive for the next session.
    if notes:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(notes),
            }
        }))
    else:
        print(json.dumps({}))
    ap.save_state(data_dir, state)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(json.dumps({}))
