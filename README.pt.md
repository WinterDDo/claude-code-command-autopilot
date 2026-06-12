# Command Autopilot para Claude Code

**Use 100% do Claude Code sem decorar nenhum comando.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | Português | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

Feito para quem usa o Claude Code mas nunca tocou nos comandos `/`. Se você já perdeu trabalho sem saber que dava para desfazer, ou viu o Claude sair fazendo uma mudança enorme que merecia um plano antes, isto é para você.

## O que muda de verdade depois de instalar

| O momento | Sem o Autopilot | Com o Autopilot |
|---|---|---|
| O Claude quebra alguma coisa | Você não sabe que existe desfazer; o Claude continua "consertando" | Ele te entrega o **/rewind** primeiro: aperte Esc duas vezes e volte para antes do estrago |
| Você pede algo grande | O Claude começa a editar na hora | Ele **planeja primeiro, automaticamente**: nada muda até você aprovar |
| Você troca de assunto no meio da sessão | O contexto antigo te atrasa e queima dinheiro | Aparece uma escolha clicável: continuar / começar do zero / separar em outra sessão, cada uma com o motivo |
| As skills que você instalou ficam paradas | Você esqueceu que as tinha | Ele as usa e avisa: "usei sua skill de pdf: li o arquivo direto" |
| Você vive descartando uma sugestão | A maioria das ferramentas insiste para sempre | Ele percebe o clima e fica quieto: ele aprende *você* |

O Claude Code tem uns 100 comandos de barra embutidos, mais todas as skills que você instalou. Iniciantes não conhecem quase nenhum, então perdem trabalho que dava para recuperar com uma tecla, queimam contexto que dava para limpar e veem o Claude partir para edições grandes que mereciam um plano antes.

O Command Autopilot resolve isso com três movimentos:

1. **Ele faz, em vez de recomendar.** O que o Claude consegue fazer sozinho, ele simplesmente faz: mudanças grandes entram automaticamente no modo de planejamento antes de qualquer arquivo ser tocado, suas preferências são gravadas na memória e suas skills instaladas são usadas (e ele conta, em uma linha, qual skill acabou de te ajudar).
2. **Ele te entrega o comando antes da hora, nunca depois.** Comandos que só você pode apertar (/rewind, /clear...) chegam como escolhas clicáveis exatamente na bifurcação que eles resolvem, cada um com o benefício em uma linha, para você saber por que está apertando.
3. **Ele evolui com você.** Cada sugestão que você aceita ou ignora vira evidência local. O autopilot percebe o clima: o que você vive descartando fica em silêncio, o que te ajuda passa a ser oferecido mais cedo, e a cada 10 sessões, mais ou menos, ele destila seu uso em regras personalizadas: visíveis, baseadas em evidência e apagáveis.

Ele ensina exatamente **quatro hábitos** (/clear, /btw, /rewind, modo de planejamento), cada um no máximo algumas vezes, e depois fica quieto. A meta é você parar de notar que ele existe.

## Instalação

**O jeito mais fácil: deixe o Claude instalar para você.** Copie este bloco inteiro, cole em qualquer conversa do Claude Code e aperte Enter:

```
Instale o plugin Command Autopilot para mim:
1. Localize meu CLI do claude: tente `command -v claude`; se não estiver no PATH, tente `~/.local/bin/claude`
   (o local mais comum no macOS/Linux). Use o caminho completo nos próximos passos se precisar.
2. Execute: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Execute: claude plugin install command-autopilot@claude-code-command-autopilot
4. Me mostre as duas confirmações de sucesso e depois me lembre de fechar o Claude Code por completo e abrir de novo.
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

Depois reinicie o Claude Code (feche por completo: os hooks carregam na inicialização) e experimente o tour de 2 minutos: peça ao Claude "me dê o tour do autopilot".

## Veja funcionando em 2 minutos

1. Peça algo grande: *"projete e construa uma funcionalidade de estatísticas para este projeto"*. → O Claude entra **no modo de planejamento sozinho**, antes de tocar em qualquer arquivo. Rejeite o plano; nada mudou.
2. Peça para ele criar um arquivo descartável e depois diga *"desfaça isso"*. → A primeira reação dele é te entregar o **/rewind (Esc Esc)**, não sair remendando para a frente.

## O que ele nunca vai fazer

- **Nada de telemetria.** Toda a evidência fica em arquivos locais que você pode abrir, auditar e apagar. Desinstalar remove tudo.
- **Nada de insistência.** Contratos rígidos: no máximo uma sugestão por resposta, o mesmo comando no máximo uma vez por sessão, e o modo quieto ou o silêncio total estão a uma frase de distância ("silencie o autopilot"). Sugestões que você descarta repetidamente somem sozinhas.
- **Nada de valor inventado.** Pergunte "o que o autopilot já fez por mim" e cada número do relatório remete a um evento real registrado.

## O custo, sem rodeios

O autopilot injeta as regras dele em cada prompt: algo entre 250 e 450 tokens dependendo do modo (quiet ≈ 230, mudo = 0). Esse é o preço do único posicionamento que comprovadamente funciona. O botão fica na sua mão: `teaching` → `normal` → `quiet` → mudo.

## Funciona na nuvem e para equipes

Sessões na nuvem não carregam sua configuração pessoal, então para o Claude Code na web e para colegas de equipe, adicione isto ao `.claude/settings.json` do seu repositório (trecho completo em [templates/team-settings.json](templates/team-settings.json)):

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

Todo mundo que confiar no workspace recebe o autopilot, tanto localmente quanto em sessões na nuvem. (Ressalvas da nuvem: os avisos de configuração não disparam lá, então valem os padrões; o estado de aprendizado zera a cada sessão na nuvem.)

Não usa o Claude Code? O [portable/PROMPT.md](portable/PROMPT.md) leva as regras centrais para o claude.ai, o Cursor ou qualquer assistente: é colar e usar.

## Como funciona (para os curiosos)

Um hook de `UserPromptSubmit` monta o contexto a cada mensagem: regras de fábrica + suas regras aprendidas + um resumo compacto de evidências. Os scripts só registram e comprimem; **todo o julgamento pertence ao modelo**, e é por isso que não existe nenhum limite mágico em lugar nenhum. Uma base de conhecimento ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) guarda o benefício em uma linha de cada comando e 8 jogadas combinadas; o modelo lê sob demanda, então não custa nada por prompt. Detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills incluídas: `tutor` (tour guiado) · `doctor` (verifica se está funcionando) · `config` (mudo/modos) · `evolve` (destila suas evidências em regras) · `profile` (o painel de valor) · `whats-new` (comandos novos e skills paradas, explicados pelo benefício).

## Requisitos

Python 3.8+ para a experiência completa. Sem Python, o autopilot roda em modo sem estado: o comportamento central fica intacto, o aprendizado pausa.

## Perguntas frequentes

**Meus dados são enviados para algum lugar?** Não. Zero telemetria. Tudo fica em arquivos locais em `~/.claude/command-autopilot/` que você pode abrir, auditar e apagar. Ao desinstalar, tudo some.

**Ele vai ficar me enchendo?** Os contratos rígidos dizem que não: no máximo uma sugestão por resposta, o mesmo comando no máximo uma vez por sessão, e sugestões que você vive descartando somem sozinhas. Dizer "silencie o autopilot" cala ele por completo.

**Quanto custa?** Ele injeta algo entre 250 e 450 tokens de regras por mensagem dependendo do modo (quiet ≈ 230, mudo = 0). É o preço honesto da confiabilidade; o botão fica na sua mão.

**Funciona no Claude Code na web / para a minha equipe?** Sim: adicione dois blocos pequenos ao `.claude/settings.json` do seu repositório ([trecho aqui](templates/team-settings.json)) e todo mundo que confiar no workspace recebe, incluindo sessões na nuvem.

**Não tenho Python, ainda funciona?** Sim, em modo sem estado: todo o comportamento central funciona, só a camada de aprendizado pausa até o Python 3.8+ estar disponível.

**Como desinstalo?** Rode `claude plugin uninstall command-autopilot@claude-code-command-autopilot` (ou peça para o Claude) e apague `~/.claude/command-autopilot/`. Não sobra nada.

**Qual a diferença para simplesmente escrever regras no CLAUDE.md?** Nós tentamos isso primeiro, duas vezes. Regras no CLAUDE.md perdem para instruções concorrentes; a injeção via hook a cada prompt é o único posicionamento que conseguimos provar que chega ao modelo 100% das vezes. Essa descoberta, junto com o design de aprendizado sem limites mágicos, é o motivo inteiro de isto ser um plugin e não um trecho de markdown. Detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Como contribuir

O comportamento vive em arquivos de texto, não em código: a maioria das melhorias são ajustes de redação em `rules/*.txt` ou entradas em `knowledge/*.json`. Leia [docs/TUNING.md](docs/TUNING.md) para a disciplina de iteração e rode [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) antes de propor mudanças de comportamento. Traduções do cartão de hábitos e dos READMEs são o primeiro PR mais amigável.

Licença MIT.
