# Claude Code를 위한 Command Autopilot

**명령어를 하나도 외우지 않고 Claude Code를 100% 활용하세요.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | 한국어 | [Français](README.fr.md) | [Deutsch](README.de.md)

Claude Code는 쓰고 있지만 `/` 명령어는 한 번도 써 본 적 없는 분들을 위해 만들었습니다. 되돌릴 수 있는 줄도 모르고 작업을 날려 본 적이 있거나, 계획부터 세웠으면 했던 큰 변경에 Claude가 곧장 달려드는 걸 지켜본 적이 있다면, 바로 당신을 위한 도구입니다.

## 설치하면 실제로 달라지는 것

| 이런 순간 | Autopilot 없이 | Autopilot 있으면 |
|---|---|---|
| Claude가 뭔가를 망가뜨렸을 때 | 되돌리기가 있는 줄도 모른 채, Claude는 계속 "고치기"만 함 | 먼저 **/rewind**를 건네줍니다. Esc 두 번이면 망가지기 전으로 돌아갑니다 |
| 큰 작업을 부탁했을 때 | Claude가 곧바로 파일을 고치기 시작 | **자동으로 계획부터** 세웁니다. 승인하기 전까지 아무것도 바뀌지 않습니다 |
| 세션 도중에 주제를 바꿨을 때 | 오래된 컨텍스트가 속도를 늦추고 돈을 낭비 | 클릭할 수 있는 선택지가 뜹니다. 계속하기 / 새로 시작 / 따로 분리, 각각 이유와 함께 |
| 설치한 스킬이 잠자고 있을 때 | 갖고 있다는 것조차 잊어버림 | 알아서 쓰고 알려줍니다. "pdf 스킬로 파일을 바로 읽었어요" |
| 같은 제안을 계속 무시할 때 | 대부분의 도구는 끝없이 잔소리 | 눈치를 채고 조용해집니다. *당신*을 학습하니까요 |

Claude Code에는 약 100개의 슬래시 명령어가 내장돼 있고, 직접 설치한 스킬도 있습니다. 하지만 초보자는 그 대부분을 모릅니다. 그래서 키 한 번이면 되돌릴 수 있었던 작업을 잃고, 비울 수 있었던 컨텍스트를 낭비하고, 계획부터 세웠어야 할 큰 수정에 Claude가 돌진하는 걸 지켜보게 됩니다.

Command Autopilot은 이 문제를 세 가지 방식으로 해결합니다.

1. **추천하는 대신, 직접 합니다.** Claude가 스스로 할 수 있는 일은 그냥 합니다. 큰 변경은 파일을 건드리기 전에 자동으로 플랜 모드에 들어가고, 당신의 취향은 메모리에 기록되고, 설치해 둔 스킬은 실제로 사용됩니다. 어떤 스킬이 도움이 됐는지는 한 줄로 알려줍니다.
2. **명령어는 그 순간이 오기 전에 건넵니다. 지나간 뒤가 아니라.** 당신만 누를 수 있는 명령어(/rewind, /clear 등)는 그것이 필요한 바로 그 갈림길에서 클릭 가능한 선택지로 도착합니다. 한 줄짜리 이점 설명이 붙어 있어서, 왜 누르는지 알 수 있습니다.
3. **당신과 함께 진화합니다.** 제안을 받아들였는지 무시했는지가 전부 로컬에 증거로 남습니다. Autopilot은 눈치를 봅니다. 계속 무시당한 제안은 조용해지고, 도움이 된 제안은 더 일찍 나오고, 대략 10세션마다 사용 기록을 정제해 당신만의 규칙으로 만듭니다. 눈으로 확인할 수 있고, 증거가 붙어 있고, 지울 수도 있습니다.

가르치는 건 딱 **네 가지 습관**(/clear, /btw, /rewind, 플랜 모드)뿐입니다. 각각 많아야 몇 번 알려주고 나면 조용해집니다. 목표는 이 플러그인의 존재를 잊게 만드는 것입니다.

## 설치

**가장 쉬운 방법은 Claude에게 설치를 맡기는 것입니다.** 아래 블록을 통째로 복사해서 아무 Claude Code 대화에나 붙여넣고 엔터를 누르세요.

```
Command Autopilot 플러그인을 설치해 줘:
1. 내 claude CLI 위치를 찾아 줘. 먼저 `command -v claude`를 시도하고, PATH에 없으면
   `~/.local/bin/claude`(macOS/Linux의 일반적인 위치)를 확인해 줘. 필요하면 다음 단계에서 전체 경로를 사용해.
2. 실행: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. 실행: claude plugin install command-autopilot@claude-code-command-autopilot
4. 두 개의 성공 메시지를 보여 주고, 마지막으로 Claude Code를 완전히 종료했다가 다시 열라고 알려 줘.
```

설치는 Claude가 직접 실행하고, CLI가 PATH에 없는 경우 같은 예외 상황도 알아서 처리합니다. 터미널 지식이 없어도 됩니다.

<details>
<summary>수동 설치 방법</summary>

**터미널에서:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

`claude`를 찾을 수 없다면 `~/.local/bin/claude`를 대신 쓰거나, 이 저장소를 클론한 뒤 `./install.sh`를 실행하세요.

**Claude Code CLI 세션 안에서** (`/plugin` 명령어는 데스크톱 앱에서는 쓸 수 없습니다):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

그다음 Claude Code를 재시작하세요(완전히 종료해야 합니다. 훅은 시작할 때 로드됩니다). 2분 투어도 해 보세요. Claude에게 "autopilot 투어 해 줘"라고 말하면 됩니다.

## 2분 만에 확인하기

1. 큰 작업을 부탁해 보세요. *"이 프로젝트에 통계 기능을 설계하고 만들어 줘."* 그러면 Claude는 파일을 건드리기 전에 **스스로 플랜 모드에 들어갑니다**. 계획을 거절하면, 아무것도 바뀌지 않은 그대로입니다.
2. 버려도 되는 파일을 하나 만들게 한 다음, *"방금 한 거 취소해 줘"*라고 말해 보세요. 첫 반응은 덧대서 고치는 게 아니라, **/rewind(Esc 두 번)**를 건네는 것입니다.

## 절대 하지 않는 것

- **텔레메트리 없음.** 모든 기록은 로컬 파일에 있어서 직접 열어 보고, 점검하고, 지울 수 있습니다. 플러그인을 제거하면 전부 사라집니다.
- **잔소리 없음.** 단단한 약속이 있습니다. 응답 하나에 제안은 최대 한 개, 같은 명령어는 세션당 최대 한 번. "autopilot 음소거해 줘" 한마디면 조용한 모드나 완전 음소거로 바뀝니다. 계속 무시당한 제안은 알아서 사라집니다.
- **부풀린 성과 없음.** "autopilot이 지금까지 뭘 해 줬어?"라고 물어보세요. 리포트의 모든 숫자는 실제로 기록된 이벤트로 거슬러 올라갑니다.

## 솔직한 비용

Autopilot은 모든 프롬프트에 규칙을 주입합니다. 모드에 따라 대략 250~450 토큰입니다(quiet ≈ 230, 음소거 = 0). 확실하게 작동한다고 입증된 유일한 위치에 두기 위한 대가입니다. 조절은 당신 몫입니다: `teaching` → `normal` → `quiet` → 음소거.

## 클라우드와 팀에서도 작동

클라우드 세션은 개인 설정을 불러오지 않습니다. 그래서 웹 버전 Claude Code와 팀 동료들에게도 적용하려면, 저장소의 `.claude/settings.json`에 아래 내용을 커밋하세요(전체 스니펫은 [templates/team-settings.json](templates/team-settings.json)에 있습니다).

```json
{
  "extraKnownMarketplaces": {
    "claude-code-command-autopilot": {
      "source": { "source": "github", "repo": "WinterDDo/claude-code-command-autopilot" }
    }
  },
  "enabledPlugins": { "command-autopilot@claude-code-command-autopilot": true }
}
```

워크스페이스를 신뢰한 모든 사람에게 Autopilot이 적용됩니다. 로컬에서도, 클라우드 세션에서도요. (클라우드 주의사항: 설정 확인 창이 뜨지 않아 기본값이 적용되고, 학습 상태는 클라우드 세션마다 초기화됩니다.)

Claude Code를 아예 안 쓰신다면? [portable/PROMPT.md](portable/PROMPT.md)가 핵심 규칙을 claude.ai, Cursor 등 어떤 어시스턴트로든 옮겨 줍니다. 붙여넣기만 하면 끝입니다.

## 작동 원리 (궁금한 분들을 위해)

`UserPromptSubmit` 훅 하나가 메시지마다 컨텍스트를 조립합니다. 내용물은 기본 규칙 + 당신이 학습시킨 규칙 + 압축된 증거 요약입니다. 스크립트는 기록하고 압축하는 일만 합니다. **판단은 전부 모델의 몫**이라서, 마법의 임계값 같은 건 어디에도 없습니다. 지식 베이스([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json))에는 모든 명령어의 한 줄 이점과 8개의 조합 플레이북이 담겨 있고, 모델이 필요할 때만 읽기 때문에 프롬프트당 비용은 없습니다. 자세한 내용은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에 있습니다.

포함된 스킬: `tutor`(가이드 투어) · `doctor`(정상 작동 점검) · `config`(음소거와 모드) · `evolve`(증거를 규칙으로 정제) · `profile`(가치 대시보드) · `whats-new`(새 명령어와 안 쓰는 스킬을 이점 중심으로 소개).

## 요구 사항

전체 기능을 쓰려면 Python 3.8 이상이 필요합니다. Python이 없어도 무상태 모드로 작동합니다. 핵심 동작은 그대로, 학습만 잠시 멈춥니다.

## 자주 묻는 질문

**내 데이터가 어딘가로 전송되나요?** 아니요. 텔레메트리는 전혀 없습니다. 모든 것은 `~/.claude/command-autopilot/`의 로컬 파일에 있고, 직접 열어 보고, 점검하고, 지울 수 있습니다. 플러그인을 제거하면 전부 사라집니다.

**잔소리하지 않나요?** 단단한 약속이 막아 줍니다. 응답 하나에 제안은 최대 한 개, 같은 명령어는 세션당 최대 한 번, 계속 무시당한 제안은 알아서 사라집니다. "autopilot 음소거해 줘"라고 하면 완전히 조용해집니다.

**비용이 얼마나 드나요?** 모드에 따라 메시지마다 대략 250~450 토큰의 규칙을 주입합니다(quiet ≈ 230, 음소거 = 0). 확실함을 위한 솔직한 대가이고, 조절은 당신이 합니다.

**웹 버전 Claude Code나 팀에서도 되나요?** 네. 저장소의 `.claude/settings.json`에 작은 블록 두 개를 커밋하면([스니펫은 여기](templates/team-settings.json)) 워크스페이스를 신뢰한 모두에게 적용됩니다. 클라우드 세션도 포함해서요.

**Python이 없는데 작동하나요?** 네, 무상태 모드로 작동합니다. 핵심 동작은 전부 쓸 수 있고, Python 3.8 이상이 생길 때까지 학습 레이어만 멈춥니다.

**어떻게 제거하나요?** `claude plugin uninstall command-autopilot@claude-code-command-autopilot`을 실행하고(Claude에게 시켜도 됩니다) `~/.claude/command-autopilot/`을 삭제하세요. 아무것도 남지 않습니다.

**CLAUDE.md에 규칙을 적는 것과 뭐가 다른가요?** 저희도 그걸 먼저 시도했습니다. 두 번이나요. 하지만 CLAUDE.md의 규칙은 경쟁하는 다른 지시들에 밀립니다. 프롬프트마다 훅으로 주입하는 방식이, 모델에 100% 도달한다고 입증할 수 있었던 유일한 위치였습니다. 이 발견과 마법의 임계값 없는 학습 설계가, 이것이 마크다운 조각이 아니라 플러그인인 이유의 전부입니다. 자세한 내용은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에 있습니다.

## 기여하기

동작은 코드가 아니라 텍스트 파일에 들어 있습니다. 개선의 대부분은 `rules/*.txt`의 문구 수정이나 `knowledge/*.json` 항목 추가입니다. 개선 절차는 [docs/TUNING.md](docs/TUNING.md)를 읽고, 동작 변경을 제안하기 전에 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md)를 실행하세요. 습관 카드와 README 번역은 첫 PR로 가장 만만한 주제입니다.

라이선스는 MIT입니다.
