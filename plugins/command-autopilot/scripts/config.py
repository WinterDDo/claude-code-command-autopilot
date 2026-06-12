#!/usr/bin/env python3
"""Read/write command-autopilot config. Usage:
  config.py <data_dir> get
  config.py <data_dir> set <key> <value>     (keys: aggressiveness|language|enable_plan_gate|muted)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
import apcommon as ap

VALID = {
    "aggressiveness": {"teaching", "normal", "quiet"},
    "language": {"en", "zh"},
    "enable_plan_gate": {"true", "false"},
    "muted": {"true", "false"},
}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    data_dir = ap.data_dir_from_argv()
    state = ap.load_state(data_dir)
    action = sys.argv[2]
    if action == "get":
        print(json.dumps(state["config"], ensure_ascii=False, indent=1))
        return 0
    if action == "set" and len(sys.argv) >= 5:
        key, value = sys.argv[3], sys.argv[4].lower()
        if key not in VALID or value not in VALID[key]:
            print("invalid: %s=%s (allowed: %s)" % (key, value, sorted(VALID.get(key, []))))
            return 1
        state["config"][key] = value == "true" if value in ("true", "false") else value
        ap.save_state(data_dir, state)
        print("ok: %s=%s (takes effect next prompt)" % (key, value))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
