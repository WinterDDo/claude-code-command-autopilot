#!/usr/bin/env python3
"""Health check. Usage: doctor.py <data_dir> [current_session_id]"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
import apcommon as ap

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def main():
    data_dir = ap.data_dir_from_argv()
    session_id = sys.argv[2] if len(sys.argv) > 2 else ""
    checks = []

    checks.append(("python", "ok %d.%d" % sys.version_info[:2]))
    try:
        state = ap.load_state(data_dir)
        checks.append(("state.json", "ok (schema %s)" % state.get("schema")))
        fired = state.get("last_fired", {})
        if fired.get("ts"):
            note = "ok, last fired %s" % fired["ts"]
            if session_id and fired.get("session_id") == session_id:
                note += " (THIS session — injection confirmed end-to-end)"
            checks.append(("router canary", note))
        else:
            checks.append(("router canary", "NEVER FIRED — hook may not be active; restart Claude Code"))
        checks.append(("config", json.dumps(state["config"], ensure_ascii=False)))
    except Exception as exc:
        checks.append(("state.json", "FAIL: %s" % exc))
    try:
        kb = json.loads((PLUGIN_ROOT / "knowledge" / "commands.json").read_text(encoding="utf-8"))
        checks.append(("knowledge", "ok (version %s, %d commands)" % (kb.get("version"), len(kb.get("commands", [])))))
    except Exception as exc:
        checks.append(("knowledge", "FAIL: %s" % exc))
    idx = data_dir / "skills-index.json"
    if idx.is_file():
        try:
            count = len(json.loads(idx.read_text(encoding="utf-8")).get("skills", []))
            checks.append(("skills index", "ok (%d skills)" % count))
        except Exception as exc:
            checks.append(("skills index", "FAIL: %s" % exc))
    else:
        checks.append(("skills index", "missing — will be built at next session start"))
    try:
        probe = data_dir / ".write-probe"
        probe.write_text("ok")
        probe.unlink()
        checks.append(("data dir writable", "ok (%s)" % data_dir))
    except Exception as exc:
        checks.append(("data dir writable", "FAIL: %s" % exc))

    for name, result in checks:
        print("%-20s %s" % (name + ":", result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
