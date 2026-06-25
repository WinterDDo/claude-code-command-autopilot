# Skill Autopilot for Claude Code

**用上你装过的 skills——而不只是你还记得的那几个。**

English | 中文 | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif 录制后嵌入此处（LAUNCH §1 分镜） -->

你装 skills 来扩展 Claude Code——然后就忘了自己有哪些、什么时候用得上。而且装得越多越*糟*：一旦超过 Claude Code 的 skill 预算，它会悄悄丢掉你最少用的那些 skill 的描述,于是为*这件*任务量身定做的那个 skill,模型反而看不见了。**Skill Autopilot 每一轮都把和你当下所做之事最相关的已装 skills 端到你面前——让合适的那个摆在你眼前,而不是被遗忘。** 遇到又大又险的任务,它还会把合适的高杠杆打法（并行 agent、Workflow、自治的 /goal、深度调研）摆成一个菜单让你挑,小事（撤销、上下文卫生）则悄悄办掉。新且实验性——开源、MIT、零遥测、本地优先。

## 它让你能做到什么

| 那个时刻 | 没有 Autopilot | 有 Autopilot |
|---|---|---|
| 又大又多文件、或重复的活 | 你只能一步步硬磨 | 动手前它摆出一个**更快路径的菜单**（并行 agent、Workflow、/background），附上取舍,你挑 |
| 一件本该一口气跑完的任务 | 你一轮一轮盯着喂 | 它递上 **/goal**,让 Claude 自己干到达标 |
| 需要真正调研的问题 | 一次浅搜 | 它跑**多来源深度调研**,给你带引用的答案 |
| 装了却忘了的 skills | 一直吃灰——或者一旦超预算就被挤出上下文 | 它**把和你任务相关的那些端出来**,让合适的 skill 摆在模型面前 |
| 你总是关掉某个建议 | 一般工具一直烦你 | 它察言观色,把那一个撤下——它学的是*你* |
| 撤销、上下文、岔题这些基本功 | 你从没学过那些命令 | 顺手包了:改坏前先递 **/rewind**、换话题给 **/clear**、岔题用 **/btw** |

**它实际说话的样子：**

```text
你：    给这个项目加一个联系人功能——表、API、表单、测试
Claude: 动手前，给你几个更快的跑法，你定：
          1. /goal —— 我自己一路做到一个完整 PR
          2. 并行 agent —— 互相独立的部分同时做
          3. 就正常做
        （挑一个，或说「开始」）
```

对命令本身还不熟？我们还维护着[白话版 Claude Code 命令速查表](docs/claude-code-commands-cheatsheet.md)和 [8 个真正省工夫的 Claude Code 工作流](docs/claude-code-workflows.md)（英文）。

Claude Code 跑在你装过的 skills 和命令上——可对的那个很少在对的时机冒出来,而 skill 库一大反而更*糟*（一超预算,Claude Code 就把最少用的 skill 的描述从上下文里丢掉）。Skill Autopilot 用三招补上这个缺口:

1. **它把合适的 skills 端出来——正好在它们合适的时候。** 每一轮它都拿你装过的 skills 跟你实际在问的东西做排序,把最相关的几个摆到模型面前（只给名字;模型按需读取完整描述）——包括那些被 Claude Code 因超预算而从上下文里丢掉的。而当几个高杠杆打法都适合一件又大又险的任务时——并行 agent、Workflow、自治的 /goal、深度调研——它把它们摆成一个菜单,你来挑。
2. **其余的它自己做,不推荐。** Claude 能自己干的就直接干:大改动在碰任何文件之前先进计划模式、偏好直接写进记忆、合适的已装 skill 自动用上。安全基本功（/rewind、/clear、/btw）在那个精确的时刻递到手边,绝不说教。
3. **它学会别挡你的路。** 你跳过的每个建议都是本地证据:总被你拒的会自动安静,绝不变成唠叨。（更深的个性化——更顺着*你*偏爱的那些打法——在路线图上;今天的本事是精准和沉默,而不是假装已经懂你。）

它从不照着一张固定的提示清单挨个跑。它每一轮都重新推理,真正有用时至多点一句,其余时候保持安静。终极目标是你感觉不到它的存在。

**只想先看看？** 把 [portable/PROMPT.md](portable/PROMPT.md) 粘进 claude.ai 或任何助手——核心行为,零安装,60 秒。

## 安装

**最简单的方式——让 Claude 替你装。** 把下面整段复制,粘贴进任何一个 Claude Code 对话,回车：

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude 会替你执行安装,自动处理各种边缘情况（命令不在 PATH 里等等）。完全不需要懂终端。

<details>
<summary>手动方式（备选）</summary>

**终端：**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

提示找不到 `claude` 时,改用 `~/.local/bin/claude`,或克隆本仓库后运行 `./install.sh`。

**Claude Code 命令行会话内**（桌面版 App 没有 `/plugin` 命令）：

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

然后重启 Claude Code（完全退出——hooks 在启动时加载）,对 Claude 说：**「check that the autopilot is working」**——内置的 doctor 会确认全链路正常。再花 2 分钟走一遍:「give me the autopilot tour」。

**不工作？**
- 建议从来不出现 → 必须完全退出再重开,hooks 只在启动时加载。
- 找不到 `/plugin` → 桌面版 App 没有 `/plugin` 命令,用上面的复制粘贴安装方式。
- 其他情况 → 让 Claude「run the autopilot doctor」,把输出贴进 [issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues)。

## 更新

对 Claude 说一句：**「update the Skill Autopilot plugin to the latest version.」**,它会替你跑下面三步。

手动做（或者你遇到「已是最新版本」——那说明你本地的 marketplace 副本是旧的,要**先**刷新它）：

```sh
claude plugin marketplace update claude-code-skill-autopilot   # 先从 GitHub 刷新目录
claude plugin update skill-autopilot@claude-code-skill-autopilot
```

然后完全退出并重开 Claude Code——规则和 hooks 在启动时加载。（云端会话每次都重新克隆仓库,所以会自动拿到新版。）

## 2 分钟亲眼见效

1. 提个大需求：*「帮我给这个项目设计并实现一个统计功能。」* → Claude **自己进入计划模式**,碰任何文件之前先给你计划。拒绝掉,什么都没发生。
2. 让它建个临时文件,然后说*「撤销。」* → 它的第一反应是递给你 **/rewind（连按两次 Esc）**,而不是自己往前修。

## 它永远不会做的事

- **零遥测。** 全部证据存在你本机、可打开可审计可删除的文件里,卸载即清空。
- **不唠叨。** 硬性契约：每条回复至多一条建议,同一命令每会话至多一次,而「安静」或彻底静音只差一句话（「mute autopilot」）。被你反复关掉的建议会自己淡出。
- **不编造价值。** 问它「what has the autopilot done for me」,报告里每个数字都能溯源到一条真实的本地记录。

## 成本（如实披露）

Autopilot 在每条提示里注入它的规则：稳态下约 500–600 token（`quiet` 更少,静音时为 0）。在已装 skills 相关的那些轮次,它会加上这些 skill 的名字——一笔很小、有上限的额外开销（约 140 token）,封顶,而在没有合适 skill 的轮次则一点不加。相对 200k 的上下文窗口,这只是百分之零点几。档位由你控制：`teaching` → `normal` → `quiet` → 静音。

## 云端与团队可用

云端会话不加载你的个人插件,也不刷新 marketplace 缓存——所以让 Claude Code 网页版和团队成员用上 Autopilot 的可靠办法是**把规则 vendored 进你的仓库**：提交一个小小的 `.claude/autopilot-context.json`（规则）加 `.claude/autopilot-cloud.sh`,并在仓库的 `.claude/settings.json` 里挂上 `SessionStart` + `UserPromptSubmit` 两个 hook 指向它。从本仓库的克隆里,一条命令完成拷贝并打印出该加的 hook 行：

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# 然后把打印出的 hook 行粘进 /path/to/your/repo/.claude/settings.json，提交
```

云端新会话每次重新克隆你的仓库,所以会自动拿到规则——该仓库里每个人都有。（云端注意：学习状态在那边是按会话的;当下的菜单照常工作。）

## 工作原理（给好奇的人）

一个 `UserPromptSubmit` hook 在每条消息组装上下文：一段简短的思考纪律 + 和你提示最相关的已装 skills + 你学到的规则 + 一份精简的证据摘要。skill 端出这一步刻意做得「笨而诚实」：会话开始时它给你装过的 skills 建一个本地索引,每一轮拿它们跟你的提示做一次廉价的词重叠排序,只注入最相关的那几个*名字*（模型按需读取每一条完整描述,自行决定要不要用其中某个）——没有合适的就什么都不注入。这里**没有场景→命令的查找表**,也没有什么被告知要信任的相似度打分器——模型每一轮都对*你这件*任务需要什么重新推理;知识库是参考资料,不是触发器。脚本只负责记录和压缩——**全部判断交给模型**,这也是为什么系统里哪儿都没有魔法阈值。一个知识库（[commands.json](plugins/skill-autopilot/knowledge/commands.json)、[playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json)）存着每个命令的一句话收益和一组组合玩法;模型按需读取,所以每条提示零成本。细节见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

内置 skills：`tutor`（引导）· `doctor`（自检）· `config`（静音/档位）· `evolve`（把你的证据蒸馏成规则）· `profile`（价值驾驶舱）· `whats-new`（新命令与闲置 skill,按收益讲解）。

## 环境要求

完整体验需要 Python 3.8+。没有 Python 时,Autopilot 进入无状态模式：核心行为不变,学习暂停。

## 常见问题

**我的数据会被发到哪里吗？** 不会。零遥测。一切都存在你本机 `~/.claude/command-autopilot/` 的文件里,可打开、可审计、可删除。卸载即清空。

**它会瞒着我什么吗？** 不会。你问 Claude「what's guiding you?」,或让它把这个插件注入的指令亮出来,它会完整告诉你——规则就是 [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules) 里的纯文本,而且指引本身就明确要求 Claude 在你问起时保持透明。这个插件对你没有任何秘密。

**它会烦我吗？** 硬性契约保证不会：每条回复至多一条建议,同一命令每会话至多一次,你反复关掉的建议会自己淡出。说一句「mute autopilot」彻底静音。

**它花多少钱？** 稳态下每条消息约 500–600 token 的规则（quiet 更少,静音为 0）,外加在已装 skills 相关的那些轮次一笔很小、有上限的额外开销（约 140 token）——相对 200k 窗口只是百分之零点几。档位由你控制。

**网页版 / 团队能用吗？** 能——用一条命令（`vendor-to-repo.sh`,见[云端与团队可用](#云端与团队可用)）把规则 vendored 进你仓库的 `.claude/`。云端会话重新克隆仓库就会拿到,该仓库里每个人都有。

**我没装 Python 也能用吗？** 能,进入无状态模式：核心行为全部保留,只有学习层暂停,装上 Python 3.8+ 自动恢复。

**怎么卸载？** 运行 `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot`（或者让 Claude 帮你跑）,删掉 `~/.claude/command-autopilot/`,干干净净。

**这和直接在 CLAUDE.md 里写规则有什么区别？** 我们最先试的就是那条路——试了两次。CLAUDE.md 里的规则会输给其他竞争指令;逐条提示的 hook 注入是我们唯一能证明 100% 到达模型的位置。这个发现,加上「零魔法阈值」的学习设计,就是它必须做成插件而不是一段 markdown 的全部原因。细节见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 参与贡献

**五分钟完成第一个 PR**：改进 `plugins/skill-autopilot/rules/*.txt` 里某条建议的措辞,或给 `plugins/skill-autopilot/knowledge/commands.json` 补一条命令的一句话收益,跑一下 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) 里对应的那一步,提交。翻译 README 同样欢迎。行为写在文本文件里,不在代码里——迭代纪律见 [docs/TUNING.md](docs/TUNING.md)。

MIT 协议。
