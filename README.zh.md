# Command Autopilot for Claude Code

**一条命令不用记，Claude Code 的全部能力为你所用。**

[English](README.md)

Claude Code 有约 100 个内置斜杠命令，加上你装的每一个 skill。新手几乎一个都不认识——于是本可一键倒带的工作丢了，本可清掉的上下文白白烧钱，本该先出计划的大改动直接开干。

Command Autopilot 用三招解决：

1. **能替你做的直接做，不推荐。** 大改动自动先进计划模式再动文件；你说「记住……」就直接写入记忆；你装过的 skill 被自动用上，并用一句话告诉你刚才是哪个 skill 帮了你。
2. **该你按的，在动作前递到手边，绝不事后诸葛。** 只有你能按的命令（/rewind、/clear……）在分岔路口以可点击选项出现，每个都带一句收益说明，你知道为什么按。
3. **越用越懂你。** 你接受或忽略的每个建议都是本地证据。它会察言观色：你总是拒绝的自动安静，对你有用的更早出现；约每 10 个会话做一次蒸馏，把你的使用习惯变成个性化规则——可查看、有证据、随时可删。

它只教**四个习惯**（/clear、/btw、/rewind、计划模式），每个最多提几次，然后闭嘴。终极目标是你感觉不到它的存在。

## 安装（30 秒）

**终端方式（所有人可用，包括桌面版 App 用户）：**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

**或者在 Claude Code 命令行会话里输入**（注意：桌面版 App 没有 `/plugin` 命令，桌面版用户请用上面的终端方式）：

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

完全退出并重启 Claude Code（hooks 在启动时加载），然后对 Claude 说「带我做一遍 autopilot 引导」，2 分钟看懂全部。

## 2 分钟亲眼见效

1. 提个大需求：「帮我给这个项目设计并实现一个统计功能」→ Claude **自己进入计划模式**，碰任何文件之前先给你计划。拒绝掉，什么都没发生。
2. 让它建个临时文件，然后说「撤销」→ 它的第一反应是递给你 **/rewind（连按两次 Esc）**，而不是自己往前修。

## 它永远不会做的事

- **零遥测。** 全部证据存在你本机、可打开可审计可删除的文件里，卸载即清空。
- **不唠叨。** 硬性契约：每条回复至多一条建议，同一命令每会话至多一次，一句「mute autopilot」彻底闭嘴。被你反复拒绝的建议会自己淡出。
- **不编造价值。** 问它「你帮我做了什么」，报告里每个数字都能溯源到一条真实的本地记录。

## 成本（如实披露）

它在每条消息注入约 250–450 token 的规则（安静模式约 230，静音为 0）。这是唯一被实测证明可靠的注入位置的代价。档位由你控制：teaching → normal → quiet → 静音。

## 云端与团队

云端会话不加载个人配置——所以 Claude Code 网页版和团队成员要靠仓库级配置：把 [templates/team-settings.json](templates/team-settings.json) 里的两段合进你仓库的 `.claude/settings.json`，所有信任该工作区的人（含云端会话）都会自动获得 Autopilot。（云端注意：设置弹窗不会出现，使用默认值；学习状态每个云端会话重置。）

完全不用 Claude Code？[portable/PROMPT.md](portable/PROMPT.md) 可以把核心规则手动贴进 claude.ai、Cursor 等任何助手。

## 工作原理（给好奇的人）

一个 `UserPromptSubmit` hook 在每条消息组装上下文：出厂规则 + 你的个性化规则 + 精简证据摘要。脚本只记录和压缩——**全部判断交给模型**，所以系统里没有任何魔法阈值。知识库（[commands.json](plugins/command-autopilot/knowledge/commands.json)、[playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)）存着每个命令的一句话收益和 8 个组合玩法，模型按需读取，每条消息零成本。详见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

内置 skills：`tutor`（引导）· `doctor`（自检）· `config`（静音/档位）· `evolve`（蒸馏你的证据）· `profile`（价值驾驶舱）· `whats-new`（新命令与闲置 skill，按收益讲解）。

## 环境要求

完整体验需要 Python 3.8+。没有 Python 时进入无状态模式：核心行为不变，学习暂停。

## 参与贡献

行为写在文本文件里，不在代码里——大部分改进只是改 `rules/*.txt` 的措辞或 `knowledge/*.json` 的条目。迭代纪律见 [docs/TUNING.md](docs/TUNING.md)，提行为改动前先跑 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md)。

MIT 协议。
