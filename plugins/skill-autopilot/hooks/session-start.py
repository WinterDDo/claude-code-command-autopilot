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
EVOLVE_EVENT_THRESHOLD = 15  # cost-control constant: when to suggest a distillation pass (lowered to turn the learning loop on sooner)
SKILL_SCAN_LIMIT = 400


def parse_frontmatter(path):
    name, description, desc_full, dmi = path.parent.name, "", "", False
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]
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
                # keep enough to capture the Triggers list (the router matches a
                # prompt against these to surface the right skill proactively).
                desc_full = line.split(":", 1)[1].strip()
                description = desc_full[:400]
            if in_fm:
                # disable-model-invocation:true keeps the description OUT of native
                # context (native can't auto-fire it) — that's "parked".
                flat = line.strip().replace(" ", "")
                if flat.startswith("disable-model-invocation:"):
                    dmi = flat.split(":", 1)[1].lower().startswith("true")
    except Exception:
        pass
    # desc budget cost mirrors native's per-skill cap (maxSkillDescriptionChars)
    return name, description, dmi, min(len(desc_full), 1536)


def read_skill_overrides():
    """Merge skillOverrides from user + project settings.json (read-only).

    Reflects the user's current native skill visibility into the index so the
    router knows which skills are PARKED. We never write settings here.
    """
    overrides = {}
    for p in (Path.home() / ".claude" / "settings.json",
              Path.cwd() / ".claude" / "settings.json"):
        try:
            ov = json.loads(p.read_text(encoding="utf-8")).get("skillOverrides", {})
            if isinstance(ov, dict):
                overrides.update(ov)
        except Exception:
            pass
    return overrides


# skillOverrides values that drop a skill's DESCRIPTION from native context —
# i.e. native can no longer auto-fire it ("parked"). "on"/absent keep it active.
PARKED_OVERRIDES = {"name-only", "user-invocable-only", "off"}


def scan_skills():
    skills, seen = [], set()
    overrides = read_skill_overrides()
    roots = [
        (Path.home() / ".claude" / "skills", "user"),
        (Path.home() / ".claude" / "plugins", "plugin"),
        (Path.cwd() / ".claude" / "skills", "project"),
    ]
    count = 0
    for root, source in roots:
        if not root.is_dir():
            continue
        for skill_md in root.glob("**/SKILL.md"):
            count += 1
            if count > SKILL_SCAN_LIMIT:
                break
            name, description, dmi, desc_chars = parse_frontmatter(skill_md)
            if name in seen:
                continue
            seen.add(name)
            ov = overrides.get(name, "")
            if ov in PARKED_OVERRIDES:
                parked, reason = True, "override:" + ov
            elif dmi and ov != "on":
                parked, reason = True, "frontmatter:disable-model-invocation"
            else:
                parked, reason = False, ""
            rec = {"name": name, "description": description, "source": source,
                   "parked": parked, "desc_chars": desc_chars}
            if parked:
                rec["park_reason"] = reason
            skills.append(rec)
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
    # Budget facts (advisory): native spends ~1% of the context window on skill
    # descriptions; over that, it shortens then DROPS least-used ones. We compute
    # in chars (~4/token) against a conservative 200k window — the value isn't
    # precision, it's flagging when the active set is crowding the matcher.
    budget_chars = int(200_000 * 0.01 * 4)
    active_chars = sum(s["desc_chars"] for s in skills if not s["parked"])
    budget = {"window_tokens": 200_000, "listing_budget_chars": budget_chars,
              "active_desc_chars": active_chars,
              "parked_count": sum(1 for s in skills if s["parked"]),
              "over_budget": active_chars > budget_chars,
              "pressure": "tight" if active_chars > budget_chars * 0.8 else "ok"}
    index_path.write_text(json.dumps({"generated": ap.now_iso(), "budget": budget, "skills": skills}, ensure_ascii=False, indent=1), encoding="utf-8")
    new_names = [s["name"] for s in skills if s["name"] not in old_names]
    if old_names and new_names:
        joined = ", ".join(new_names[:5])
        notes.append(("[AUTOPILOT one-time] User installed new skill(s) since last session: %s. "
                      "When natural, mention ONE of them with what it can do for them.") % joined)

    # One-time heads-up (the user asked to be told up front, not silently optimized):
    # explain the skill layer + its tiny, only-when-relevant per-turn cost. Once ever.
    if not state.get("skills_headsup_done") and skills:
        n, m = len(skills), budget["parked_count"]
        if zh:
            notes.append(("[AUTOPILOT one-time] 跟用户说一次:Skills Autopilot 已启用。他装了 %d 个 skill"
                          "(其中约 %d 个 native 因预算看不见)。每一轮我会把与当下任务最相关的几个浮出来、合适就用——"
                          "只有真有相关 skill 的那一轮才多花一点点上下文(相对窗口可忽略),无关时一个不加。随时 /doctor 看状态。") % (n, m))
        else:
            notes.append(("[AUTOPILOT one-time] Tell the user once, plainly: Skills Autopilot is active. They have %d installed skills"
                          " (~%d invisible to native due to its budget). Each turn I surface the few most relevant to the task and use one if it fits"
                          " — adding a little context ONLY on turns where a skill fits (negligible vs the window), nothing otherwise. Run /doctor anytime.") % (n, m))
        state["skills_headsup_done"] = True

    # Knowledge-base version change -> whats-new announcement
    try:
        kb_version = json.loads((PLUGIN_ROOT / "knowledge" / "commands.json").read_text(encoding="utf-8")).get("version", "")
    except Exception:
        kb_version = ""
    if kb_version and state.get("kb_version") and kb_version != state["kb_version"]:
        notes.append("[AUTOPILOT one-time] The command knowledge base was updated to %s. "
                     "When natural, offer the whats-new skill to show what is newly possible." % kb_version)
    state["kb_version"] = kb_version

    # First run: arm the one-time first-task demo (the guaranteed aha). The forced
    # welcome menu is injected by router.py on the first substantial task and
    # cleared by tracker.py once it fires — a stronger first impression than a
    # prose self-introduction the model may or may not deliver well.
    if not state.get("first_run_done"):
        state["first_task_pending"] = True
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

    # One-time power-command introduction: from the 2nd session on, if the user
    # has never used or been offered the high-leverage commands, introduce them
    # ONCE — these are the capabilities a beginner can't ask for because they
    # don't know they exist. Fires once ever (flag), never nags.
    if not state.get("power_intro_done") and len(state.get("sessions", {})) >= 2:
        cmds = state.get("counters", {}).get("commands", {})
        # derive the high-leverage pool from the KB (single source of truth),
        # not a hard-coded subset — so the intro can cover all 30+, not 6
        high_leverage = ap.kb_high_leverage(PLUGIN_ROOT)
        unused = [c for c in high_leverage
                  if not (cmds.get(c, {}).get("self_used") or cmds.get(c, {}).get("suggested"))]
        if unused:
            joined = ", ".join(unused[:4])
            if zh:
                notes.append(("[AUTOPILOT one-time] 借这次机会主动介绍：用户多步骤工作做得不少，但这几个高杠杆命令从没用过：%s。"
                              "读 knowledge/commands.json + playbooks.json，用大白话讲清其中 2-3 个是什么、对他这种工作有什么用、怎么试一次。仅此一次，别堆清单、别说教。") % joined)
            else:
                notes.append(("[AUTOPILOT one-time] Proactively introduce: the user does multi-step work but has never used these high-leverage commands: %s. "
                              "Read knowledge/commands.json + playbooks.json and explain 2-3 of them in plain words — what each is, what it does for THEIR kind of work, how to try one. Once only, no list-dumping, no lecturing.") % joined)
            state["power_intro_done"] = True

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
