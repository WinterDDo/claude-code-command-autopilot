# Claude Code를 위한 Skill Autopilot

**기억하는 스킬만이 아니라, 설치해 둔 스킬을 쓰세요.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | 한국어 | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

당신은 Claude Code를 확장하려고 스킬을 설치합니다. 그러고는 어떤 게 있는지, 언제 어울리는지 잊어버립니다. 그리고 더 많이 설치할수록 *상황은 더 나빠집니다.* Claude Code의 스킬 예산을 넘기면, 가장 덜 쓰는 스킬의 설명이 슬그머니 빠지기 때문에, *바로 이 작업*에 딱 맞는 스킬이 모델에게 보이지 않게 될 수 있습니다. **Skill Autopilot은 지금 당신이 하는 일에 가장 잘 맞는, 설치된 스킬을 매 턴마다 앞에 내놓습니다 — 그래서 잊히는 대신 딱 맞는 스킬이 당신 앞에 놓입니다.** 또한 크거나 위험한 작업에 어울리는 고효율 수들(병렬 에이전트, 워크플로, 자율적인 /goal, 깊은 조사)을 당신이 고를 메뉴로 펼쳐 놓고, 자잘한 것들(되돌리기, 컨텍스트 정리)은 조용히 처리합니다. 새롭고 실험적입니다 — 오픈 소스, MIT, 텔레메트리 제로, 로컬 우선.

## 가능해지는 것들

| 그 순간 | Autopilot 없이 | Autopilot 있으면 |
|---|---|---|
| 크거나, 여러 파일에 걸치거나, 반복적인 작업 | 한 단계씩 손으로 갈아 넣음 | 시작하기 전에 **더 빠른 경로의 메뉴**(병렬 에이전트, 워크플로, /background)를 트레이드오프와 함께 펼쳐 주고, 당신이 고름 |
| 끝까지 알아서 굴러가야 할 작업 | 매 턴마다 옆에서 챙겨야 함 | **/goal**을 제안해서 Claude가 스스로 끝까지 작업함 |
| 진짜 조사가 필요한 질문 | 얕은 검색 한 번 | **여러 출처를 깊이 파는 조사**를 돌려 출처가 달린 답을 건넴 |
| 설치해 놓고 잊은 스킬 | 그냥 잠들어 있음 — 예산을 넘기면 컨텍스트에서 빠지기까지 함 | **당신 작업에 맞는 스킬을 앞에 내놓아서**, 딱 맞는 스킬이 모델 앞에 놓이게 함 |
| 같은 제안을 계속 거절할 때 | 대부분의 도구는 끝없이 잔소리 | 분위기를 읽고 그 제안을 거둠 — *당신*을 학습함 |
| 기본기 — 되돌리기, 컨텍스트, 곁다리 얘기 | 명령어를 배운 적이 없음 | 조용히 처리: 손보기 전에 **/rewind**, 주제 전환 때 **/clear**, 곁다리 얘기엔 **/btw** |

**실제로는 이렇게 들립니다:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

명령어 자체가 처음이신가요? [쉬운 말로 정리한 Claude Code 명령어 치트시트](docs/claude-code-commands-cheatsheet.md)(영어)와 [실제 작업을 줄여 주는 8가지 Claude Code 워크플로](docs/claude-code-workflows.md)(영어)도 함께 관리하고 있습니다.

Claude Code는 당신이 설치한 스킬과 명령어로 굴러갑니다 — 그런데 딱 맞는 것이 딱 맞는 순간에 떠오르는 일은 드물고, 스킬 라이브러리가 크면 *상황은 더 나빠집니다*(예산을 넘기면 Claude Code가 가장 덜 쓰는 스킬의 설명을 컨텍스트에서 빼 버립니다). Skill Autopilot은 세 가지 방식으로 그 간극을 메웁니다.

1. **들어맞는 스킬을, 들어맞는 바로 그 순간에 앞에 내놓습니다.** 매 턴, 설치된 스킬을 당신이 실제로 요청한 내용에 견주어 순위를 매기고 가장 관련 있는 것들을 모델 앞에 놓습니다(이름으로 — 모델은 필요할 때 전체 설명을 읽습니다) — 예산을 넘겨 Claude Code가 컨텍스트에서 뺀 스킬까지 포함해서요. 그리고 크거나 위험한 작업에 여러 고효율 수들(병렬 에이전트, 워크플로, 자율적인 /goal, 깊은 조사)이 들어맞을 때는, 그것들을 메뉴로 펼쳐 놓고 당신이 고릅니다.
2. **나머지는 추천하는 대신 직접 합니다.** Claude가 스스로 할 수 있는 일은 그냥 합니다. 큰 변경은 파일을 건드리기 전에 플랜 모드로 들어가고, 취향은 메모리에 기록되고, 들어맞는 설치된 스킬은 실제로 사용됩니다. 안전 기본기(/rewind, /clear, /btw)는 훈수처럼 늘어놓는 게 아니라 바로 그 순간에 건넵니다.
3. **방해되지 않는 법을 학습합니다.** 당신이 건너뛴 제안 하나하나가 로컬 증거입니다. 계속 거절하는 것은 조용해지므로, 결코 잔소리가 되지 않습니다. (더 깊은 개인화 — *당신*이 특별히 선호하는 수에 맞춰 기우는 것 — 은 로드맵에 있습니다. 오늘의 성과는 정밀함과 침묵이지, 이미 당신을 안다고 시늉하는 게 아닙니다.)

고정된 팁 체크리스트를 훑는 일은 결코 없습니다. 매 턴을 새로 추론하고, 진짜로 도움이 될 때만 많아야 한 번 짚어 주고, 그 외에는 조용히 있습니다. 목표는 당신이 이 도구의 존재를 더는 의식하지 않게 되는 것입니다.

**그냥 둘러보는 중인가요?** [portable/PROMPT.md](portable/PROMPT.md)를 claude.ai나 아무 어시스턴트에나 붙여넣으세요. 핵심 동작 그대로, 설치 없이, 60초면 끝입니다.

## 설치

**가장 쉬운 방법은 Claude에게 설치를 맡기는 것입니다.** 아래 블록을 통째로 복사해서 아무 Claude Code 대화에나 붙여넣고 엔터를 누르세요.

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

설치는 Claude가 직접 실행하고, CLI가 PATH에 없는 경우 같은 예외 상황도 알아서 처리합니다. 터미널 지식이 없어도 됩니다.

<details>
<summary>수동 설치 방법</summary>

**터미널에서:**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

`claude`를 찾을 수 없다면 `~/.local/bin/claude`를 대신 쓰거나, 이 저장소를 클론한 뒤 `./install.sh`를 실행하세요.

**Claude Code CLI 세션 안에서** (`/plugin` 명령어는 데스크톱 앱에서는 쓸 수 없습니다):

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

그다음 Claude Code를 재시작하고(완전히 종료하세요. 훅은 시작할 때 로드됩니다) Claude에게 **"autopilot이 작동하는지 확인해 줘"**라고 물어보세요. 내장된 doctor가 모든 것이 끝에서 끝까지 잘 작동하는지 확인해 줍니다. 그다음 2분 투어도 해 보세요. "autopilot 투어 해 줘"라고 하면 됩니다.

**작동하지 않나요?**
- 제안이 전혀 안 뜸 → 완전히 종료했다가 다시 열어야 합니다. 훅은 시작할 때만 로드됩니다.
- `/plugin`을 찾을 수 없음 → 데스크톱 앱에는 `/plugin` 명령어가 없습니다. 위의 복사-붙여넣기 설치를 쓰세요.
- 그 외 → Claude에게 "run the autopilot doctor"라고 하고, 그 출력을 [이슈](https://github.com/WinterDDo/claude-code-skill-autopilot/issues)에 붙여넣으세요.

## 업데이트

Claude에게 **"Skill Autopilot 플러그인을 최신 버전으로 업데이트해 줘"**라고 하세요. 아래 세 단계를 대신 실행해 줍니다.

직접 할 때(또는 "already at the latest version"이 뜨면 — 로컬 마켓플레이스 복사본이 오래됐다는 뜻이니, *먼저* 새로 고치세요):

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
```

그다음 Claude Code를 완전히 종료했다가 다시 여세요. 규칙과 훅은 시작할 때 로드됩니다. (클라우드 세션은 항상 저장소를 새로 클론하므로, 새 버전을 스스로 가져옵니다.)

## 2분 만에 확인하기

1. 큰 작업을 부탁해 보세요. *"design and build a statistics feature for this project."* 그러면 Claude는 어떤 파일을 건드리기도 전에 **스스로 플랜 모드에 들어갑니다.** 계획을 거절하면, 아무것도 바뀌지 않았습니다.
2. 버려도 되는 파일을 하나 만들게 한 다음, *"undo that."*이라고 말해 보세요. 첫 반응은 덧대서 고치는 게 아니라, **/rewind(Esc 두 번)**를 건네는 것입니다.

## 절대 하지 않는 것

- **텔레메트리 없음.** 모든 증거는 직접 열어 보고, 점검하고, 지울 수 있는 로컬 파일에 있습니다. 제거하면 전부 사라집니다.
- **잔소리 없음.** 단단한 약속: 응답 하나에 제안은 최대 한 개, 같은 명령어는 세션당 최대 한 번, "quiet"이나 완전 음소거는 한마디면 됩니다("mute autopilot"). 반복해서 거절한 제안은 알아서 사라집니다.
- **부풀린 성과 없음.** "what has the autopilot done for me"라고 물어보세요. 리포트의 모든 숫자는 실제로 기록된 이벤트로 거슬러 올라갑니다.

## 솔직한 비용

Autopilot은 모든 프롬프트에 규칙을 주입합니다. 정상 상태에서 대략 500~600 토큰입니다(`quiet`에서는 더 적고, 음소거 시 0). 설치된 스킬이 관련 있는 턴에서는 그 스킬의 이름이 더해집니다 — 작고 제한된 추가분(~140 토큰)이며, 상한이 있고, 들어맞는 게 없는 턴에서는 아무것도 더해지지 않습니다. 200k 컨텍스트 창에 견주면 1퍼센트의 몇 분의 일 수준입니다. 조절은 당신 몫입니다: `teaching` → `normal` → `quiet` → 음소거.

## 클라우드와 팀에서도 작동

클라우드 세션은 당신의 개인 플러그인을 불러오지 않고, 마켓플레이스 캐시도 새로 고치지 않습니다. 그래서 웹 버전 Claude Code와 동료들에게 Autopilot을 확실히 적용하는 방법은 **규칙을 당신의 저장소에 벤더링하는 것**입니다. 작은 `.claude/autopilot-context.json`(규칙)과 `.claude/autopilot-cloud.sh`를 커밋하고, 저장소의 `.claude/settings.json`에서 `SessionStart` + `UserPromptSubmit` 훅을 거기에 연결하세요. 이 저장소를 클론한 곳에서 명령어 한 번이면 파일을 복사하고 정확한 훅 줄을 출력해 줍니다.

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

새 클라우드 세션은 당신의 저장소를 새로 클론하므로, 그 저장소에서 일하는 모두를 위해 규칙을 자동으로 가져옵니다. (클라우드 주의사항: 거기서는 학습 상태가 세션마다 따로입니다. 다만 그 순간의 메뉴는 여전히 작동합니다.)

## 작동 원리 (궁금한 분들을 위해)

`UserPromptSubmit` 훅 하나가 메시지마다 컨텍스트를 조립합니다. 짧은 사고 규율 + 당신의 프롬프트에 가장 관련 있는 설치된 스킬 + 당신이 학습시킨 규칙 + 압축된 증거 요약입니다. 스킬을 앞에 내놓는 방식은 일부러 단순하고 정직합니다. 세션 시작 때 설치된 스킬의 로컬 색인을 만들고, 매 턴 당신의 프롬프트와의 값싼 단어 겹침으로 순위를 매겨 가장 관련 있는 몇 개의 *이름*만 주입합니다(모델은 필요할 때 각 스킬의 전체 설명을 읽고 쓸지를 스스로 정합니다) — 들어맞는 게 없으면 아무것도 주입하지 않습니다. **시나리오→명령어 조회 테이블 같은 건 없고**, 모델더러 믿으라고 하는 유사도 점수기 같은 것도 없습니다 — 모델이 매 턴 *당신의* 작업에 무엇이 필요한지 새로 추론합니다. 지식 베이스는 트리거가 아니라 참고 자료입니다. 스크립트는 기록하고 압축하는 일만 합니다 — **판단은 전부 모델의 몫**이라서, 마법의 임계값 같은 건 어디에도 없습니다. 지식 베이스([commands.json](plugins/skill-autopilot/knowledge/commands.json), [playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json))에는 모든 명령어의 한 줄 이점과 조합 플레이북 모음이 담겨 있고, 모델이 필요할 때만 읽기 때문에 프롬프트당 비용은 없습니다. 자세한 내용은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에 있습니다.

포함된 스킬: `tutor`(가이드 투어) · `doctor`(정상 작동 점검) · `config`(음소거와 모드) · `evolve`(증거를 규칙으로 정제) · `profile`(가치 대시보드) · `whats-new`(새 명령어와 안 쓰는 스킬을 이점 중심으로 소개).

## 요구 사항

전체 기능을 쓰려면 Python 3.8 이상이 필요합니다. Python이 없어도 무상태 모드로 작동합니다. 핵심 동작은 그대로, 학습만 잠시 멈춥니다.

## 자주 묻는 질문

**내 데이터가 어딘가로 전송되나요?** 아니요. 텔레메트리는 전혀 없습니다. 모든 것은 `~/.claude/command-autopilot/`의 로컬 파일에 있고, 직접 열어 보고, 점검하고, 지울 수 있습니다. 제거하면 전부 사라집니다.

**저한테 뭔가 숨기나요?** 아니요. Claude에게 "what's guiding you?"라고 묻거나 이 플러그인이 주입하는 지시를 보여 달라고 하면, 전부 알려 줍니다. 규칙은 [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules)에 평문으로 들어 있고, 안내문은 당신이 물어볼 때마다 투명하게 밝히라고 Claude에게 명시적으로 지시합니다. 이 플러그인에 당신에게서 숨기는 것은 아무것도 없습니다.

**잔소리하지 않나요?** 단단한 약속이 막아 줍니다. 응답 하나에 제안은 최대 한 개, 같은 명령어는 세션당 최대 한 번, 계속 거절한 제안은 알아서 사라집니다. "mute autopilot"이라고 하면 완전히 조용해집니다.

**비용이 얼마나 드나요?** 정상 상태에서 메시지마다 대략 500~600 토큰의 규칙을 주입합니다(quiet에서는 더 적고, 음소거 시 0). 여기에 설치된 스킬이 관련 있는 턴에서 작고 제한된 추가분(~140 토큰)이 더해집니다 — 200k 창의 1퍼센트의 몇 분의 일 수준입니다. 조절은 당신이 합니다.

**웹 버전 Claude Code나 팀에서도 되나요?** 네. 명령어 한 번으로 규칙을 저장소의 `.claude/`에 벤더링하세요(`vendor-to-repo.sh`, [클라우드와 팀에서도 작동](#클라우드와-팀에서도-작동) 참고). 클라우드 세션은 저장소를 새로 클론해 규칙을 가져오므로, 그 저장소에서 일하는 모두가 적용받습니다.

**Python이 없는데 작동하나요?** 네, 무상태 모드로 작동합니다. 핵심 동작은 전부 쓸 수 있고, Python 3.8 이상이 생길 때까지 학습 레이어만 멈춥니다.

**어떻게 제거하나요?** `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot`을 실행하고(Claude에게 시켜도 됩니다) `~/.claude/command-autopilot/`을 삭제하세요. 아무것도 남지 않습니다.

**CLAUDE.md에 규칙을 적는 것과 뭐가 다른가요?** 저희도 그걸 먼저 시도했습니다. 두 번이나요. 하지만 CLAUDE.md의 규칙은 경쟁하는 다른 지시들에 밀립니다. 프롬프트마다 훅으로 주입하는 방식이, 모델에 100% 도달한다고 입증할 수 있었던 유일한 위치였습니다. 이 발견과 마법의 임계값 없는 학습 설계가, 이것이 마크다운 조각이 아니라 플러그인인 이유의 전부입니다. 자세한 내용은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에 있습니다.

## 기여하기

**5분 만에 첫 PR:** `plugins/skill-autopilot/rules/*.txt`에서 제안 하나의 문구를 다듬거나, `plugins/skill-autopilot/knowledge/commands.json`에 명령어의 한 줄 이점을 추가하고, [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md)의 해당 단계를 실행한 뒤 제출하세요. README 번역도 똑같이 환영합니다. 동작은 코드가 아니라 텍스트 파일에 들어 있습니다. 반복 개선의 규율은 [docs/TUNING.md](docs/TUNING.md)를 참고하세요.

라이선스는 MIT입니다.
