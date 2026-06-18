#!/usr/bin/env python3
"""Generate the vendored cloud injection from the plugin's own rules.

Single source of truth: the rules live in rules/core.en.txt. This bakes the
core+safety+unlock sections into a static hook-output JSON that repos commit
to .claude/, so cloud sessions get the current rules without depending on the
marketplace cache. Re-run on every release; vendor-to-repos.sh ships it.

Usage: build-cloud-context.py [output_path]
Default output: <plugin>/cloud/autopilot-context.json
"""
import json
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
RULES = PLUGIN / "rules" / "core.en.txt"


def parse_sections(text):
    sections, cur = {}, None
    for line in text.splitlines():
        if line.startswith("#=SECTION "):
            cur = line.split(" ", 1)[1].strip()
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def build():
    sec = parse_sections(RULES.read_text(encoding="utf-8"))
    # cloud = the stateless behavior that matters in ephemeral sessions:
    # core (self-help + discipline) + safety + unlock (better-move menu) +
    # welcome (first-task demo). Cloud has no persistent state, so the welcome
    # fires per session on the first substantial message (model-judged); the
    # local plugin gates the same text behind a once-ever flag instead.
    parts = [sec.get("core", ""), sec.get("safety", ""), sec.get("unlock", ""), sec.get("welcome", "")]
    body = "\n".join(p for p in parts if p)
    # KB/INDEX pointers don't exist in cloud; point at nothing rather than a stale path
    body = body.replace("{KB}", "the knowledge base (if present)").replace("{INDEX}", "your installed skills (if present)")
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else PLUGIN / "cloud" / "autopilot-context.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = build()
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    ctx = doc["hookSpecificOutput"]["additionalContext"]
    assert "BETTER-MOVE CHECK" in ctx, "unlock section missing from generated cloud context"
    assert "[AUTOPILOT]" in ctx, "core section missing"
    assert "/rewind" in ctx, "safety section missing"
    assert "FIRST TASK ONLY" in ctx, "welcome section missing"
    print("wrote %s (%d chars, all 4 sections present)" % (out, len(ctx)))


if __name__ == "__main__":
    main()
