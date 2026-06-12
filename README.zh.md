# Command Autopilot for Claude Code

**一条命令不用记，Claude Code 的全部能力为你所用。**

[English](README.md) | 中文 | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif 录制后嵌入此处（LAUNCH §1 分镜） -->

这是给「用 Claude Code 但从来没碰过 `/` 命令」的人做的免费插件：它把所有命令都记熟了，所以你不用记。如果你曾经丢过本可以一键找回的工作，或者眼睁睁看着 Claude 没打招呼就开始大改你的东西——它就是为你准备的。开源、MIT、零遥测：它学到的一切都存在你本机可打开可删除的文件里，说一句「mute autopilot」永远管用。

## 装上之后，具体什么会变

| 那个时刻 | 没有 Autopilot | 有 Autopilot |
|---|---|---|
| Claude 改坏了东西 | 你不知道有撤销，它一个劲地「修」 | 它先把 **/rewind** 递给你：按两下 Esc，回到改坏之前 |
| 你提了个大需求 | 它立刻开始改文件 | **自动先出计划**，你批准之前什么都不动 |
| 你中途换了话题 | 旧上下文拖慢速度还烧钱 | 弹出可点的选择：继续 / 清桌重来 / 分出去，各带一句理由 |
| 装过的 skills 在吃灰 | 你忘了自己有什么 | 它自动用上并告诉你：「用了你的 pdf skill，直接读了文件」 |
| 你总是关掉某个建议 | 一般的工具会一直烦你 | 它会察言观色自己安静——它学的是**你** |

**它实际说话的样子：**

```text
你：    撤销刚才的改动，原来的更好
Claude: 在我尝试任何修复之前：你可以直接回到改动之前。
        连按两次 Esc（/rewind）——文件和对话一起恢复。
        需要我等你操作吗？
```

想了解命令本身？我们还维护着[白话版 Claude Code 命令速查表](docs/claude-code-commands-cheatsheet.md)和 [8 个真正省工夫的 Claude Code 工作流](docs/claude-code-workflows.md)（英文）。

Claude Code 有约 100 个内置斜杠命令，加上你装的每一个 skill。新手几乎一个都不认识——于是本可一键倒带的工作丢了，本可清掉的上下文白白烧钱，本该先出计划的大改动直接开干。

Command Autopilot 用三招解决：

1. **能替你做的直接做，不推荐。** 大改动自动先进计划模式再动文件；你说「记住……」就直接写入记忆；你装过的 skill 被自动用上，并用一句话告诉你刚才是哪个 skill 帮了你。
2. **该你按的，在动作前递到手边，绝不事后诸葛。** 只有你能按的命令（/rewind、/clear……）在分岔路口以可点击选项出现，每个都带一句收益说明，你知道为什么按。
3. **越用越懂你。** 你接受或忽略的每个建议都是本地证据。它会察言观色：你总是拒绝的自动安静，对你有用的更早出现；约每 10 个会话做一次蒸馏，把你的使用习惯变成个性化规则——可查看、有证据、随时可删。

它只教**四个习惯**（/clear、/btw、/rewind、计划模式），每个最多提几次，然后闭嘴。终极目标是你感觉不到它的存在。

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


## 工作原理（给好奇的人）

一个 `UserPromptSubmit` hook 在每条消息组装上下文：出厂规则 + 你的个性化规则 + 精简证据摘要。脚本只记录和压缩——**全部判断交给模型**，所以系统里没有任何魔法阈值。知识库（[commands.json](plugins/command-autopilot/knowledge/commands.json)、[playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)）存着每个命令的一句话收益和 8 个组合玩法，模型按需读取，每条消息零成本。详见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

内置 skills：`tutor`（引导）· `doctor`（自检）· `config`（静音/档位）· `evolve`（蒸馏你的证据）· `profile`（价值驾驶舱）· `whats-new`（新命令与闲置 skill，按收益讲解）。

## 环境要求

完整体验需要 Python 3.8+。没有 Python 时进入无状态模式：核心行为不变，学习暂停。

## 常见问题

**我的数据会被发到哪里吗？** 不会。零遥测。一切都存在你本机 `~/.claude/command-autopilot/` 的文件里，可打开、可审计、可删除。卸载即清空。

**它会烦我吗？** 硬性契约保证不会：每条回复至多一条建议，同一命令每会话至多一次，你反复关掉的建议会自己淡出。说一句「mute autopilot」彻底静音。

**它花多少钱？** 每条消息注入约 250–450 token 的规则（安静模式约 230，静音为 0）。这是可靠性的真实价格，档位由你控制。

**网页版 / 团队能用吗？** 能——把两小段配置提交到你仓库的 `.claude/settings.json`（[现成片段](templates/team-settings.json)），信任该工作区的所有人（包括云端会话）自动获得。

**我没装 Python 也能用吗？** 能，进入无状态模式：核心行为全部保留，只有学习层暂停，装上 Python 3.8+ 自动恢复。

**怎么卸载？** 运行 `claude plugin uninstall command-autopilot@claude-code-command-autopilot`（或者让 Claude 帮你跑），删掉 `~/.claude/command-autopilot/`，干干净净。

**这和直接在 CLAUDE.md 里写规则有什么区别？** 我们最先试的就是那条路，失败了两次：CLAUDE.md 里的规则会输给其他竞争指令，逐条消息的 hook 注入是唯一被实测证明 100% 到达模型的位置。这个发现加上「零魔法阈值」的学习设计，就是它必须做成插件而不是一段 markdown 的全部原因。细节见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 参与贡献

**五分钟完成第一个 PR**：改进 `plugins/command-autopilot/rules/*.txt` 里某条建议的措辞，或给 `plugins/command-autopilot/knowledge/commands.json` 补一条命令收益句，跑一下 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) 里对应的那步，提交。翻译 README 同样欢迎。行为写在文本文件里，不在代码里——迭代纪律见 [docs/TUNING.md](docs/TUNING.md)。

MIT 协议。
