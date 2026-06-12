---
name: config
description: Adjust Command Autopilot settings — mute it, change aggressiveness (teaching/normal/quiet), switch guidance language (en/zh), or toggle the auto plan-mode gate. Use when the user says the autopilot is too noisy, too quiet, "mute autopilot", "autopilot太烦了", "别再提示了", or wants teaching tips back.
---

# Autopilot settings

Map the user's request to one command, run it, read the value back, confirm in one line.

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" "$HOME/.claude/command-autopilot" get
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" "$HOME/.claude/command-autopilot" set <key> <value>
```



| User intent | Setting |
|---|---|
| "太烦了 / too noisy / stop suggesting" | `set aggressiveness quiet` (silent help + /rewind safety only) |
| "完全闭嘴 / mute it" | `set muted true` (zero injection, zero tokens) |
| "把提示打开 / teach me again" | `set aggressiveness teaching` |
| "正常模式" | `set aggressiveness normal` |
| "中文提示 / English guidance" | `set language zh` / `set language en` |
| "别自动进计划模式" | `set enable_plan_gate false` |

Always mention: changes take effect from the next message, no restart needed. If the user muted it, tell them the one phrase that brings it back ("unmute autopilot").
