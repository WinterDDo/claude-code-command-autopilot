# Command Autopilot para Claude Code

**Use todo o Claude Code, não apenas os poucos comandos que você conhece.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | Português | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

O Claude Code consegue disparar agentes em paralelo, perseguir uma meta sozinho, rodar fluxos de trabalho de vários passos, pesquisar pela web inteira, mas, na hora, até quem é experiente acaba fazendo tudo no braço. O Command Autopilot observa o que você está realmente fazendo e, no momento certo, **apresenta as poucas jogadas de maior alavancagem que se encaixam, como um menu para você escolher.** As coisas pequenas (desfazer, higiene de contexto) ele simplesmente cuida. Não é só para iniciantes que nunca ouviram falar dos comandos; até quem é avançado esquece a melhor jogada sob pressão, e é justamente essa décima vez que importa. Código aberto, MIT, zero telemetria.

## O que ele torna possível

| O momento | Sem o Autopilot | Com o Autopilot |
|---|---|---|
| Um trabalho grande, com vários arquivos, ou repetitivo | Você faz tudo no braço, um passo de cada vez | Ele apresenta um **menu de caminhos mais rápidos** (agentes em paralelo, um Workflow, /background) antes de começar, com os trade-offs, e você escolhe |
| Uma tarefa que deveria simplesmente ir até o fim | Você fica supervisionando turno a turno | Ele oferece **/goal** para o Claude trabalhar até o fim por conta própria |
| Uma pergunta que precisa de pesquisa de verdade | Uma busca rasa | Ele roda **pesquisa profunda em várias fontes** e te entrega uma resposta com citações |
| Skills que você instalou mas esqueceu | Ficam paradas, sem uso | Ele **as usa** e diz qual acabou de ajudar: "usei sua skill de pdf: li o arquivo direto" |
| Você vive descartando uma sugestão | A maioria das ferramentas insiste para sempre | Ele percebe o clima e abandona aquela sugestão: ele aprende *você* |
| O básico: desfazer, contexto, comentários à parte | Você nunca aprendeu os comandos | Cuidado em silêncio: **/rewind** antes de qualquer conserto, **/clear** nas trocas de assunto, **/btw** para comentários à parte |

**Como isso soa na prática:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

Novo nos comandos em si? Também mantemos [a cola dos comandos do Claude Code em linguagem simples](docs/claude-code-commands-cheatsheet.md) e [8 fluxos de trabalho do Claude Code que poupam trabalho de verdade](docs/claude-code-workflows.md) (ambos em inglês).

O Claude Code tem uns 100 comandos de barra embutidos, mais todas as skills que você instalou, e os mais poderosos (orquestração, paralelismo, autonomia) são justamente os que ninguém descobre. O Command Autopilot fecha essa lacuna com três movimentos:

1. **No momento certo, ele apresenta suas opções como um menu.** Antes de uma tarefa grande, repetitiva, longa ou arriscada, ele apresenta as 2 a 4 jogadas de maior alavancagem que realmente se encaixam (agentes em paralelo, um Workflow, um /goal autônomo, pesquisa profunda, /background), cada uma com seu trade-off, e você escolhe. Não é uma única sugestão do tipo pega ou larga: é o menu, para você escolher. (Para quem é experiente também: o valor está na jogada em que você não pensou *agora*, não em uma que você nunca ouviu falar.)
2. **Ele faz o resto sozinho, em vez de recomendar.** O que o Claude consegue fazer por conta própria, ele simplesmente faz: mudanças grandes entram no modo de planejamento antes de qualquer arquivo ser tocado, preferências são gravadas na memória, suas skills instaladas são usadas (e ele diz qual ajudou). O básico de segurança (/rewind, /clear, /btw) é entregue no momento exato, nunca como um sermão.
3. **Ele aprende a sair do seu caminho.** Cada sugestão que você ignora é evidência local: o que você vive descartando fica em silêncio, então nunca vira insistência. (Uma personalização mais profunda, inclinando-se para as jogadas que *você* especificamente prefere, está no roadmap; a vitória de hoje é precisão e silêncio, não fingir que já te conhece.)

Ele nunca percorre uma lista fixa de dicas. Ele raciocina sobre cada turno, aponta algo no máximo uma vez quando isso genuinamente ajuda, e fora isso fica quieto. A meta é você parar de notar que ele existe.

**Só dando uma olhada?** Cole [portable/PROMPT.md](portable/PROMPT.md) no claude.ai ou em qualquer assistente: o comportamento central, nada instalado, 60 segundos.

## Instalação

**O jeito mais fácil: deixe o Claude instalar para você.** Copie este bloco inteiro, cole em qualquer conversa do Claude Code e aperte Enter:

```
Install the Command Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Run: claude plugin install command-autopilot@claude-code-command-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

O Claude executa a instalação e cuida dos casos complicados (CLI fora do PATH etc.) por você. Não precisa entender de terminal.

<details>
<summary>Alternativas manuais</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

Se o `claude` não for encontrado, use `~/.local/bin/claude` no lugar, ou rode `./install.sh` a partir de um clone deste repositório.

**Dentro de uma sessão do CLI do Claude Code** (o comando `/plugin` não está disponível no app de desktop):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

Depois reinicie o Claude Code (feche por completo: os hooks carregam na inicialização) e peça ao Claude: **"check that the autopilot is working"** (o doctor embutido confirma que tudo está disparando de ponta a ponta). Em seguida, faça o tour de 2 minutos: "give me the autopilot tour".

**Não está funcionando?**
- As sugestões nunca aparecem → você precisa fechar por completo e abrir de novo; os hooks só carregam na inicialização.
- `/plugin` não encontrado → o app de desktop não tem o comando `/plugin`; use a instalação por copiar e colar acima.
- Qualquer outra coisa → peça ao Claude para "run the autopilot doctor" e cole a saída em uma [issue](https://github.com/WinterDDo/claude-code-command-autopilot/issues).

## Atualização

Peça ao Claude: **"update the command-autopilot plugin to the latest version."** Ele roda os três passos abaixo para você.

Fazendo na mão (ou se você bater em "already at the latest version" — isso significa que sua cópia local do marketplace está desatualizada, então atualize-a *primeiro*):

```sh
claude plugin marketplace update claude-code-command-autopilot   # refresh the catalog from GitHub
claude plugin update command-autopilot@claude-code-command-autopilot
```

Depois feche por completo e abra de novo o Claude Code: regras e hooks carregam na inicialização. (As sessões na nuvem sempre clonam o repositório do zero, então pegam as novas versões por conta própria.)

## Veja funcionando em 2 minutos

1. Peça algo grande: *"design and build a statistics feature for this project."* → O Claude entra **no modo de planejamento sozinho**, antes de tocar em qualquer arquivo. Rejeite o plano; nada mudou.
2. Peça para ele criar um arquivo descartável e depois diga *"undo that."* → A primeira reação dele é te entregar o **/rewind (Esc Esc)**, não sair remendando para a frente.

## O que ele nunca vai fazer

- **Nada de telemetria.** Toda a evidência fica em arquivos locais que você pode abrir, auditar e apagar. Desinstalar remove tudo.
- **Nada de insistência.** Contratos rígidos: no máximo uma sugestão por resposta, o mesmo comando no máximo uma vez por sessão, e o modo quieto ou o silêncio total estão a uma frase de distância ("mute autopilot"). Sugestões que você descarta repetidamente somem sozinhas.
- **Nada de valor inventado.** Pergunte "what has the autopilot done for me" e cada número do relatório remete a um evento real registrado.

## O custo, sem rodeios

O autopilot injeta as regras dele em cada prompt: algo entre 300 e 500 tokens dependendo do modo (quiet ≈ 300, mudo = 0). Esse é o preço do único posicionamento que comprovadamente funciona. O botão fica na sua mão: `teaching` → `normal` → `quiet` → mudo.

## Funciona na nuvem e para equipes

As sessões na nuvem não carregam seus plugins pessoais, e não atualizam o cache do marketplace, então o jeito confiável de ter o autopilot no Claude Code na web e para os colegas de equipe é **incorporar as regras dele ao seu repositório**: faça commit de um pequeno `.claude/autopilot-context.json` (as regras) mais o `.claude/autopilot-cloud.sh`, e conecte os hooks `SessionStart` + `UserPromptSubmit` a ele no `.claude/settings.json` do seu repositório. A partir de um clone deste repositório, um comando copia os arquivos e imprime as linhas de hook exatas:

```sh
plugins/command-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

Novas sessões na nuvem clonam seu repositório do zero, então pegam as regras automaticamente, para todo mundo que trabalha naquele repositório. (Ressalva da nuvem: lá o estado de aprendizado é por sessão; o menu na hora continua funcionando.)

## Como funciona (para os curiosos)

Um único hook de `UserPromptSubmit` monta o contexto a cada mensagem: uma disciplina curta de raciocínio + suas regras aprendidas + um resumo compacto de evidências. **Não há tabela de consulta cenário→comando** — o modelo raciocina do zero a cada turno sobre o que a *sua* tarefa precisa; a base de conhecimento é referência, não gatilho. Os scripts só registram e comprimem — **todo o julgamento pertence ao modelo**, e é por isso que não existe nenhum limite mágico em lugar nenhum. Uma base de conhecimento ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) guarda o benefício em uma linha de cada comando e um conjunto de jogadas combinadas; o modelo lê sob demanda, então não custa nada por prompt. Detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills incluídas: `tutor` (tour guiado) · `doctor` (verifica se está funcionando) · `config` (mudo/modos) · `evolve` (destila suas evidências em regras) · `profile` (o painel de valor) · `whats-new` (comandos novos e skills paradas, explicados pelo benefício).

## Requisitos

Python 3.8+ para a experiência completa. Sem Python, o autopilot roda em modo sem estado: o comportamento central fica intacto, o aprendizado pausa.

## Perguntas frequentes

**Meus dados são enviados para algum lugar?** Não. Zero telemetria. Tudo fica em arquivos locais em `~/.claude/command-autopilot/` que você pode abrir, auditar e apagar. Ao desinstalar, tudo some.

**Ele esconde algo de mim?** Não. Pergunte ao Claude "what's guiding you?" ou peça para ele mostrar a instrução que este plugin injeta, e ele vai te contar por completo — as regras são texto puro em [`plugins/command-autopilot/rules/`](plugins/command-autopilot/rules), e a orientação manda o Claude explicitamente ser transparente sempre que você perguntar. Nada sobre o plugin é segredo para você.

**Ele vai ficar me enchendo?** Os contratos rígidos dizem que não: no máximo uma sugestão por resposta, o mesmo comando no máximo uma vez por sessão, e sugestões que você vive descartando somem sozinhas. Dizer "mute autopilot" cala ele por completo.

**Quanto custa?** Ele injeta algo entre 300 e 500 tokens de regras por mensagem dependendo do modo (quiet ≈ 300, mudo = 0). É o preço honesto da confiabilidade; o botão fica na sua mão.

**Funciona no Claude Code na web / para a minha equipe?** Sim: incorpore as regras dele ao `.claude/` do seu repositório com um comando (`vendor-to-repo.sh`, veja [Funciona na nuvem e para equipes](#funciona-na-nuvem-e-para-equipes)). As sessões na nuvem clonam o repositório do zero e pegam as regras, então todo mundo que trabalha naquele repositório recebe.

**Não tenho Python, ainda funciona?** Sim, em modo sem estado: todo o comportamento central funciona, só a camada de aprendizado pausa até o Python 3.8+ estar disponível.

**Como desinstalo?** Rode `claude plugin uninstall command-autopilot@claude-code-command-autopilot` (ou peça para o Claude) e apague `~/.claude/command-autopilot/`. Não sobra nada.

**Qual a diferença para simplesmente escrever regras no CLAUDE.md?** Nós tentamos isso primeiro, duas vezes. Regras no CLAUDE.md perdem para instruções concorrentes; a injeção via hook a cada prompt é o único posicionamento que conseguimos provar que chega ao modelo 100% das vezes. Essa descoberta, junto com o design de aprendizado sem limites mágicos, é o motivo inteiro de isto ser um plugin e não um trecho de markdown. Detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Como contribuir

**Primeiro PR em 5 minutos:** melhore a redação de uma sugestão em `plugins/command-autopilot/rules/*.txt`, ou adicione o benefício em uma linha de um comando em `plugins/command-autopilot/knowledge/commands.json`, rode o passo correspondente em [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md), e envie. Traduções do README são igualmente bem-vindas. O comportamento vive em arquivos de texto, não em código: veja [docs/TUNING.md](docs/TUNING.md) para a disciplina de iteração.

Licença MIT.
