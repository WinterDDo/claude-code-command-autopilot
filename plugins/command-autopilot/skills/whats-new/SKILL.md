---
name: whats-new
description: Explain what's newly possible — new Claude Code commands after a knowledge-base update, and installed-but-never-used skills. Use when the autopilot announces a knowledge update, or the user asks "what's new", "有什么新功能", "我装了哪些没用过的 skill".
---

# What's newly possible

Two sources, both local. Speak the user's language, lead with benefit, never list for listing's sake.

## New commands (after a knowledge-base update)
Read `${CLAUDE_PLUGIN_ROOT}/knowledge/commands.json` and `playbooks.json`. Compare against what the user has actually seen used (counters in `~/.claude/command-autopilot/state.json`). Pick the 2-3 entries most relevant to how this user works (their evidence shows what they do) and present each as: **what it is → what it does for YOU → the one-line way to try it**. Mention the version it arrived in.

## Installed-but-unused skills
Read `~/.claude/command-autopilot/skills-index.json`; cross-reference with `state.json` skill counters. Skills with zero invocations are dormant value the user already owns. Pick the 1-2 most relevant to their evidence profile: "You installed X — it can ... — next time you ..., I'll use it automatically."

## Rules
Max 5 items total per run. Relevance over completeness; the rest stays for next time. End with: "Ask again any time — this list updates itself."
