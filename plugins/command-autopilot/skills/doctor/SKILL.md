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

## Verdict
- Both pass → "Autopilot is healthy." Show the config line so the user sees their current mode.
- Check 1 fails but files look fine → restart needed, or another hook is crowding the context; suggest restart first.
- Python missing in check 2 → explain stateless mode honestly: core rules still work, learning and evidence are paused until Python 3.8+ is installed.
