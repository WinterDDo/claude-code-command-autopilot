---
name: tutor
description: Guided first tour of Skill Autopilot — see auto plan mode happen, learn the 4 habit commands (/clear, /btw, /rewind, plan mode), and what Claude now handles silently. Use when the user asks how the autopilot works, what commands they should learn, how to undo Claude's changes, says "tour", "教我命令", "怎么用命令", or right after installation.
---

# Skill Autopilot tour (2 minutes, hands-on)

Run a short interactive tour. Speak the user's language. Keep every step to 2-3 sentences. Never lecture.

## Step 1 — the magic moment (auto plan mode)
Ask the user to type a deliberately big request, for example: "design and build a statistics feature for this project" (or let them invent one). When they send it, Claude enters plan mode by itself before touching any file. Tell them to REJECT the plan afterwards: nothing changed, and they just watched the autopilot think before acting.

## Step 2 — the undo button
Create a throwaway file (test-autopilot.md, three lines). Then tell the user: "say 'undo that'". The autopilot's first reaction is to hand them /rewind (press Esc twice) instead of patching forward. Let them open the rewind menu and look — selecting nothing changes nothing.

## Step 3 — the habit card
Render this table, translated to the user's language:

| Command | When | How |
|---|---|---|
| /clear | Starting an unrelated new task | type `/clear` — new task carries no old baggage |
| /btw | A side question mid-task | type `/btw <question>` — zero pollution of the main thread |
| /rewind | Dissatisfied with a change | press `Esc` twice — back to before the damage |
| plan mode | Any big change | press `Shift+Tab` — review the plan before any file changes |

Close with one line: "Everything else you don't need to learn. What Claude can do, it just does; what only you can press, it hands you before the moment — with the reason why."

## Step 4 — wrap
Mention once: the profile skill shows what the autopilot did for them; the config skill mutes or quiets it in one word.
