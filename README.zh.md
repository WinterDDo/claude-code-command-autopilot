# Command Autopilot for Claude Code

**用上 Claude Code 的全部能力——不只是你会的那几个命令。**

[English](README.md) | 中文 | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif 录制后嵌入此处（LAUNCH §1 分镜） -->

Claude Code 能扇出并行 agent、能自己奔着一个目标跑、能跑整套多步骤 workflow、能跨网做深度调研——但在当下,哪怕高手也常常默认埋头硬磨。Command Autopilot 看着你正在做的事,在对的时机把**几个合适的高杠杆打法摆成菜单,让你挑**。撤销、清理上下文这些小事它顺手就办。它不只是给「没听说过这些命令」的新手——哪怕高手也会在当下忘了最优解,而那第 10 次正是它的价值所在。开源、MIT、零遥测。

## 它让你能做到什么

| 那个时刻 | 没有 Autopilot | 有 Autopilot |
|---|---|---|
| 又大又多文件、或重复的活 | 你只能一步步硬磨 | 动手前它摆出一个**更快路径的菜单**(并行 agent、Workflow、/background),附上代价,你挑 |
| 一件本该一口气跑完的任务 | 你一轮一轮盯着喂 | 它递上 **/goal**,让 Claude 自己干到达标 |
| 需要真正调研的问题 | 一次浅搜 | 它跑**多来源深度调研**,给你带引用的答案 |
| 装了却忘了的 skills | 一直吃灰 | 它**直接用上**并告诉你是哪个:「用了你的 pdf skill,直接读了文件」 |
| 你总是关掉某个建议 | 一般工具一直烦你 | 它察言观色,把那一个撤下——它学的是**你** |
| 撤销、上下文、岔题这些基本功 | 你从没学过那些命令 | 顺手包了:改坏先递 **/rewind**、换话题给 **/clear**、岔题用 **/btw** |

**它实际说话的样子：**

```text
你：    给这个项目加一个联系人功能——表、API、表单、测试
Claude: 动手前，给你几个更快的跑法，你定：
          1. /goal —— 我自己一路做到一个完整 PR
          2. 并行 agent —— 互相独立的部分同时做
          3. 就正常做
        （挑一个，或说「开始」）
```

想了解命令本身？我们还维护着[白话版 Claude Code 命令速查表](docs/claude-code-commands-cheatsheet.md)和 [8 个真正省工夫的 Claude Code 工作流](docs/claude-code-workflows.md)（英文）。

Claude Code 有约 100 个内置斜杠命令,加上你装的每个 skill,而其中最强的那些——编排、并行、自治——恰恰是没人会去发现的。Command Autopilot 用三招补上这个缺口:

1. **在对的时机,把你的选项摆成菜单。** 在又大、重复、长周期、或有风险的任务开工前,它把 2-4 个真正合适的高杠杆打法端给你——并行 agent、Workflow、自治的 /goal、深度调研、/background——每个附上代价,你来挑。不是单条「要不要」,是一个菜单,让你选。(对高手也一样——价值在于你**此刻**没想到的那一招,而非你没听过的命令。)
2. **其余的它自己做,不推荐。** 能自己干的就直接干:大改动先进计划模式再动文件、偏好直接写进记忆、你装的 skill 自动用上(并告诉你是哪个)。撤销/清桌/岔题这些安全基本功,在那一刻递到手边,而不是说教。
3. **它学会别挡你的路。** 你跳过的每个建议都是本地证据:总被你拒的自动安静,绝不变成唠叨。(更深的个性化——更懂你偏爱哪些招——在路线图上;现在的本事是精准和沉默,不假装已经懂你。)

它不会照着一张固定清单挨个提示。它每一轮都重新判断，真正有用时至多点一句，其余时候保持安静。终极目标是你感觉不到它的存在。

**只想先感受一下？** 把 [portable/PROMPT.md](portable/PROMPT.md) 粘进 claude.ai 或任何助手——核心行为零安装体验，60 秒。

## 安装

**最简单的方式：让 Claude 替你装。** 把下面整段复制，粘贴进任何一个 Claude Code 对话，回车：

```
帮我安装 Command Autopilot 插件：
1. 先定位我的 claude 命令行工具：试试 `command -v claude`，找不到就试 `~/.local/bin/claude`
   （macOS/Linux 的常见位置）。后面的步骤按需使用完整路径。
2. 运行：claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. 运行：claude plugin install command-autopilot@claude-code-command-autopilot
4. 把两条成功确认给我看，然后提醒我完全退出并重新打开 Claude Code，
   再运行 autopilot doctor 验证安装。
```

Claude 会替你执行安装，自动处理各种边缘情况（命令不在 PATH 里等等）。完全不需要懂终端。

<details>
<summary>手动方式（备选）</summary>

**终端：**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

提示找不到 `claude` 时，改用 `~/.local/bin/claude`，或克隆本仓库后运行 `./install.sh`。

**Claude Code 命令行会话内**（桌面版 App 没有 `/plugin` 命令）：

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

然后完全退出并重启 Claude Code（hooks 在启动时加载），对 Claude 说：**「check autopilot」**——内置的 doctor 会确认全链路正常。再说「带我做一遍 autopilot 引导」，2 分钟看懂全部。

**不工作？**
- 建议从来不出现 → 必须完全退出再重开，hooks 只在启动时加载。
- 找不到 `/plugin` → 桌面版 App 没有这个命令，用上面的复制粘贴安装方式。
- 其他情况 → 让 Claude「跑一下 autopilot doctor」，把输出贴进 [issue](https://github.com/WinterDDo/claude-code-command-autopilot/issues)。

## 更新

对 Claude 说一句：**「把 command-autopilot 插件更新到最新版」**，它会替你跑下面三步。

手动做（或者你遇到「已是最新版本」——那说明你本地的 marketplace 清单是旧的，要**先**刷新它）：

```sh
claude plugin marketplace update claude-code-command-autopilot   # 先从 GitHub 刷新目录
claude plugin update command-autopilot@claude-code-command-autopilot
```

然后完全退出并重开 Claude Code——规则和 hooks 在启动时加载。（云端会话每次都重新克隆仓库，所以会自动拿到新版。）

## 2 分钟亲眼见效

1. 提个大需求：「帮我给这个项目设计并实现一个统计功能」→ Claude **自己进入计划模式**，碰任何文件之前先给你计划。拒绝掉，什么都没发生。
2. 让它建个临时文件，然后说「撤销」→ 它的第一反应是递给你 **/rewind（连按两次 Esc）**，而不是自己往前修。

## 它永远不会做的事

- **零遥测。** 全部证据存在你本机、可打开可审计可删除的文件里，卸载即清空。
- **不唠叨。** 硬性契约：每条回复至多一条建议，同一命令每会话至多一次，一句「mute autopilot」彻底闭嘴。被你反复拒绝的建议会自己淡出。
- **不编造价值。** 问它「你帮我做了什么」，报告里每个数字都能溯源到一条真实的本地记录。

## 成本（如实披露）

它在每条消息注入约 300–500 token 的规则（安静模式约 300，静音为 0）。这是唯一被实测证明可靠的注入位置的代价。档位由你控制：teaching → normal → quiet → 静音。

## 云端与团队

云端会话不加载个人插件，也不刷新 marketplace 缓存——所以让 Claude Code 网页版和团队成员用上 Autopilot 的可靠办法是**把规则 vendored 进你的仓库**：提交一个小小的 `.claude/autopilot-context.json`（规则）加 `.claude/autopilot-cloud.sh`，并在仓库的 `.claude/settings.json` 里挂上 `SessionStart` + `UserPromptSubmit` 两个 hook 指向它。从本仓库的克隆里，一条命令完成拷贝并打印出该加的 hook 行：

```sh
plugins/command-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# 然后把打印出的 hook 行粘进 /path/to/your/repo/.claude/settings.json，提交
```

云端新会话每次重新克隆你的仓库，所以会自动拿到规则——该仓库里每个人都有。（云端注意：学习状态在那边是按会话的；当下的菜单照常工作。）


## 工作原理（给好奇的人）

一个 `UserPromptSubmit` hook 在每条消息组装上下文：出厂规则 + 你的个性化规则 + 精简证据摘要。脚本只记录和压缩——**全部判断交给模型**，所以系统里没有任何魔法阈值。知识库（[commands.json](plugins/command-autopilot/knowledge/commands.json)、[playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)）存着每个命令的一句话收益和一组组合玩法，模型按需读取，每条消息零成本。详见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

内置 skills：`tutor`（引导）· `doctor`（自检）· `config`（静音/档位）· `evolve`（蒸馏你的证据）· `profile`（价值驾驶舱）· `whats-new`（新命令与闲置 skill，按收益讲解）。

## 环境要求

完整体验需要 Python 3.8+。没有 Python 时进入无状态模式：核心行为不变，学习暂停。

## 常见问题

**我的数据会被发到哪里吗？** 不会。零遥测。一切都存在你本机 `~/.claude/command-autopilot/` 的文件里，可打开、可审计、可删除。卸载即清空。

**它会瞒着我什么吗？** 不会。你问 Claude「是什么在指引你」，或让它把这个插件注入的指令亮出来，它会完整告诉你——规则就是 [`plugins/command-autopilot/rules/`](plugins/command-autopilot/rules) 里的纯文本，而且指令本身就明确要求 Claude 在你问起时保持透明。这个插件对你没有任何秘密。

**它会烦我吗？** 硬性契约保证不会：每条回复至多一条建议，同一命令每会话至多一次，你反复关掉的建议会自己淡出。说一句「mute autopilot」彻底静音。

**它花多少钱？** 每条消息注入约 300–500 token 的规则（安静模式约 300，静音为 0）。这是可靠性的真实价格，档位由你控制。

**网页版 / 团队能用吗？** 能——用一条命令（`vendor-to-repo.sh`，见[云端与团队](#云端与团队)）把规则 vendored 进你仓库的 `.claude/`。云端会话重新克隆仓库就会拿到，该仓库里每个人都有。

**我没装 Python 也能用吗？** 能，进入无状态模式：核心行为全部保留，只有学习层暂停，装上 Python 3.8+ 自动恢复。

**怎么卸载？** 运行 `claude plugin uninstall command-autopilot@claude-code-command-autopilot`（或者让 Claude 帮你跑），删掉 `~/.claude/command-autopilot/`，干干净净。

**这和直接在 CLAUDE.md 里写规则有什么区别？** 我们最先试的就是那条路，失败了两次：CLAUDE.md 里的规则会输给其他竞争指令，逐条消息的 hook 注入是唯一被实测证明 100% 到达模型的位置。这个发现加上「零魔法阈值」的学习设计，就是它必须做成插件而不是一段 markdown 的全部原因。细节见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 参与贡献

**五分钟完成第一个 PR**：改进 `plugins/command-autopilot/rules/*.txt` 里某条建议的措辞，或给 `plugins/command-autopilot/knowledge/commands.json` 补一条命令收益句，跑一下 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) 里对应的那步，提交。翻译 README 同样欢迎。行为写在文本文件里，不在代码里——迭代纪律见 [docs/TUNING.md](docs/TUNING.md)。

MIT 协议。
