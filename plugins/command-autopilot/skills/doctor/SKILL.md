---
name: doctor
description: Diagnose whether Command Autopilot's hooks are actually firing and config is valid. Use when the autopilot seems inactive, suggestions never appear, after install or update to verify setup, or the user says "autopilot不工作", "check autopilot", "autopilot broken".
---

# Autopilot health check

Two independent checks. Report both, then a one-line verdict.

## Check 1 — self report (only the model can confirm this)
State plainly, first: did the CURRENT prompt's context contain a block starting with `[AUTOPILOT]`? Yes or no. If yes, injection reaches the model — the core product works.

## Check 2 — the canary
Run:

```
sh "${CLAUDE_PLUGIN_ROOT}/hooks/run.sh" doctor-noop 2>/dev/null; python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py" "$HOME/.claude/command-autopilot" "<current session id if known>"
```



Read the output. Key line is `router canary`: if it shows THIS session, the hook fired end-to-end. If it says NEVER FIRED, tell the user to restart Claude Code (hooks load at startup) and run this skill again.

## Check 3 — skills surfacing (read-only; the Skills Autopilot layer)
Report what the skill layer sees and has done. All read-only, no writes:

```
python3 - <<'EOF'
import json, os
d = os.path.expanduser("~/.claude/command-autopilot")
try:
    idx = json.load(open(d + "/skills-index.json")); b = idx.get("budget", {})
    print("skills indexed:", len(idx.get("skills", [])),
          "| parked (native can't auto-fire these):", b.get("parked_count"),
          "| over native budget:", b.get("over_budget"))
except Exception:
    print("no skills index yet — restart Claude Code so SessionStart builds it")
try:
    s = json.load(open(d + "/state.json")); w = s.get("counters", {}).get("wake", {})
    f = lambda k: sum(v.get(k, 0) for v in w.values())
    print("wake popups — shown:", f("shown"), "accepted:", f("accepted"), "declined:", f("declined"))
except Exception:
    pass
EOF
```

Report in one line: N skills installed, M parked (invisible to native — the ones the autopilot uniquely surfaces), and the wake shown/accepted tally. If `shown` is still 0 after real use, surfacing isn't firing yet — say so honestly; the real ledger is the judge, not assumptions.

## Verdict
- Both pass → "Autopilot is healthy." Show the config line so the user sees their current mode.
- Check 1 fails but files look fine → restart needed, or another hook is crowding the context; suggest restart first.
- Python missing in check 2 → explain stateless mode honestly: core rules still work, learning and evidence are paused until Python 3.8+ is installed.
