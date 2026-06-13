# Acceptance test script (release gate)

Run in a **fresh session** after a **restart** of Claude Code (hooks and rules load at startup). Every release must pass cold-start. Iteration rule: one step failing = tune wording in `rules/*.txt` and retest; the same step failing twice in a row = design problem, stop and rethink.

Record each step ✅/❌. English inputs shown; Chinese equivalents in parentheses work identically.

| # | Layer | Input | Pass criteria |
|---|---|---|---|
| 0 | health | "check autopilot" | doctor skill runs; self-report confirms `[AUTOPILOT]` block arrived; canary shows this session |
| 1 | L1 plan gate | "design and build a stats feature for this project" (帮我设计并实现一个统计功能) — do NOT type /plan | Plan mode UI appears BEFORE any file edit; reject → nothing changed |
| 2 | boundary | "create test.md with three lines" (建个 test.md 写三行) | Done directly; no plan mode, no popups (over-triggering is also a failure) |
| 3 | L2 safety | "you broke it, take me back to before test.md" (你改坏了，回到建文件之前) | First reaction offers /rewind (Esc Esc); does NOT self-repair |
| 4 | L3 teach | mid-task aside: "what time is it in São Paulo?" (圣保罗现在几点) | Answers first; at most ONE light /btw tip |
| 5 | frequency | second aside: "weather in NYC?" (纽约天气) | Answers; no second tip in this session |
| 6 | L1 memory | "remember: use US spelling in my emails" (记住：邮件用美式拼写) | Written to memory directly + one-line confirmation; not redirected to /memory |
| 7 | L1 history | "find what we decided about X in a past session" (找找之前会话里关于 X 的结论) | Searches history itself; not redirected to /resume |
| 8 | L2 fork | after the previous steps, switch topic abruptly: "analyze coffee-shop competition in São Paulo" (帮我分析圣保罗咖啡店竞争) | BEFORE starting: clickable options (continue / /clear / spin off), each option carrying a benefit line |
| 9 | benefit lines | inspect any suggestion popup from steps above | Every suggested command carries a ≤15-word benefit (sourced from knowledge/commands.json) |
| 10 | skills L1 | install any sample skill, send a matching task | Skill auto-invoked + one-line disclosure of which skill and what it did |
| 11 | evidence behavior | dismiss the same suggestion in 2-3 separate sessions, then create the trigger again | Suggestion has become rare/absent — UNLESS the moment is clearly high-value, where it may reappear with acknowledgment |
| 12 | evolve | after ~10 sessions (or seed events.jsonl synthetically): run evolve skill | learned.json written; rules have evidence counts; profile shows them; bogus patterns NOT invented |
| 13 | value | "what has the autopilot done for me?" | Dashboard report; spot-check 2 numbers against events.jsonl lines — must match exactly |
| 14 | mute | "mute autopilot", then send any prompt | No `[AUTOPILOT]` behavior; doctor confirms empty injection; "unmute autopilot" restores |
| 15 | unlock (costly) | ask for a big multi-file job, e.g. "rename this API across the whole codebase" | BEFORE acting, offers the high-leverage path (parallel agents / Workflow) via clickable options WITH the token/time cost; waits for your choice — does not just start |
| 16 | unlock (cheap) | ask something research-heavy, e.g. "compare three approaches to X across the docs" | Just uses a sub-agent / deep research and says so in one line — no popup for the cheap reversible path |
| 17 | no over-trigger | ask a plain small task, e.g. "fix this typo" | Does it directly; no capability popup, no habit nagging |
| 18 | cognition not catalog | ask "why did you suggest that?" right after an unlock offer | Explains it reasoned about THIS task's leverage, not a preset rule; the answer is task-specific |

Cleanup: delete test.md (or /rewind), delete the test memory entry, `config.py set muted false`.
