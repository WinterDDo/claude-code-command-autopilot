# Command Autopilot para Claude Code

**Usa el 100% de Claude Code sin memorizar ni un solo comando.**

[English](README.md) | [中文](README.zh.md) | Español | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

Hecho para quienes usan Claude Code pero nunca han tocado los comandos `/`. Si alguna vez perdiste trabajo que no sabías que podías deshacer, o viste a Claude lanzarse a un cambio enorme que ojalá hubiera planificado primero, esto es para ti.

## Qué cambia realmente después de instalarlo

| El momento | Sin Autopilot | Con Autopilot |
|---|---|---|
| Claude rompe algo | No sabes que existe el deshacer; Claude sigue "arreglando" | Te ofrece **/rewind** primero: pulsa Esc dos veces y vuelves a antes del daño |
| Pides algo grande | Claude empieza a editar de inmediato | **Planifica primero, automáticamente**: nada cambia hasta que tú apruebes |
| Cambias de tema a mitad de sesión | El contexto viejo te frena y quema dinero | Aparece una opción clicable: continuar / empezar de cero / separar en otra sesión, cada una con su razón |
| Las skills que instalaste se quedan sin usar | Olvidaste que las tenías | Las usa y te lo cuenta: "usé tu skill de pdf: leí el archivo directamente" |
| Sigues descartando una sugerencia | La mayoría de las herramientas insisten para siempre | Lee el ambiente y guarda silencio: aprende de *ti* |

Claude Code tiene unos 100 comandos de barra integrados, más todas las skills que hayas instalado. Los principiantes no conocen casi ninguno, así que pierden trabajo que podían haber recuperado con una tecla, queman contexto que podían haber limpiado y ven a Claude lanzarse a ediciones grandes que merecían un plan primero.

Command Autopilot lo resuelve con tres movimientos:

1. **Hace, en lugar de recomendar.** Lo que Claude puede hacer por sí mismo, simplemente lo hace: los cambios grandes entran automáticamente en modo plan antes de tocar cualquier archivo, tus preferencias se guardan en memoria y tus skills instaladas se usan (y te dice, en una línea, qué skill acaba de ayudarte).
2. **Te entrega el comando antes del momento, nunca después.** Los comandos que solo tú puedes pulsar (/rewind, /clear...) llegan como opciones clicables justo en la encrucijada que resuelven, cada uno con su beneficio en una línea, para que sepas por qué lo estás pulsando.
3. **Evoluciona contigo.** Cada sugerencia que aceptas o ignoras es evidencia local. El autopilot lee el ambiente: lo que sigues descartando se silencia, lo que te ayuda se ofrece antes, y más o menos cada 10 sesiones destila tu uso en reglas personalizadas: visibles, respaldadas por evidencia y borrables.

Enseña exactamente **cuatro hábitos** (/clear, /btw, /rewind, modo plan), cada uno como mucho unas pocas veces, y luego guarda silencio. La meta es que dejes de notarlo.

## Instalación

**Lo más fácil: deja que Claude lo instale por ti.** Copia este bloque completo, pégalo en cualquier conversación de Claude Code y pulsa Enter:

```
Instálame el plugin Command Autopilot:
1. Localiza mi CLI de claude: prueba `command -v claude`; si no está en el PATH, prueba `~/.local/bin/claude`
   (la ubicación habitual en macOS/Linux). Usa la ruta completa en los pasos siguientes si hace falta.
2. Ejecuta: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Ejecuta: claude plugin install command-autopilot@claude-code-command-autopilot
4. Muéstrame las dos confirmaciones de éxito y luego recuérdame cerrar Claude Code por completo y volver a abrirlo.
```

Claude ejecuta la instalación y se encarga de los casos raros (el CLI fuera del PATH, etc.) por ti. No hace falta saber de terminal.

<details>
<summary>Alternativas manuales</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

Si no se encuentra `claude`, usa `~/.local/bin/claude` en su lugar, o ejecuta `./install.sh` desde un clon de este repositorio.

**Dentro de una sesión del CLI de Claude Code** (el comando `/plugin` no está disponible en la app de escritorio):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

Después reinicia Claude Code (ciérralo por completo: los hooks se cargan al arrancar) y prueba el tour de 2 minutos: pídele a Claude "dame el tour del autopilot".

## Velo funcionar en 2 minutos

1. Pide algo grande: *"diseña y construye una función de estadísticas para este proyecto"*. → Claude entra en **modo plan por sí solo**, antes de tocar ningún archivo. Rechaza el plan; nada cambió.
2. Haz que cree un archivo desechable y luego di *"deshaz eso"*. → Su primera reacción es ofrecerte **/rewind (Esc Esc)**, no parchear hacia adelante.

## Lo que nunca hará

- **Nada de telemetría.** Toda la evidencia vive en archivos locales que puedes abrir, revisar y borrar. Desinstalar lo elimina todo.
- **Nada de insistencia.** Contratos firmes: como mucho una sugerencia por respuesta, el mismo comando como mucho una vez por sesión, y el modo silencioso o el silencio total están a una frase de distancia ("silencia el autopilot"). Las sugerencias que descartas repetidamente se apagan solas.
- **Nada de valor inventado.** Pregunta "¿qué ha hecho el autopilot por mí?" y cada número del informe se remonta a un evento real registrado.

## El costo, sin rodeos

El autopilot inyecta sus reglas en cada prompt: entre 250 y 450 tokens aproximadamente según el modo (quiet ≈ 230, silenciado = 0). Ese es el precio de la única ubicación que demostradamente funciona. Tú controlas el dial: `teaching` → `normal` → `quiet` → silencio total.

## Funciona en la nube y para equipos

Las sesiones en la nube no cargan tu configuración personal, así que para Claude Code en la web y para tus compañeros de equipo, añade esto al `.claude/settings.json` de tu repositorio (fragmento completo en [templates/team-settings.json](templates/team-settings.json)):

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

Todos los que confíen en el espacio de trabajo reciben el autopilot, tanto en local como en sesiones en la nube. (Salvedades de la nube: los avisos de configuración no se activan ahí, así que se aplican los valores por defecto; el estado de aprendizaje se reinicia en cada sesión en la nube.)

¿No tienes Claude Code? [portable/PROMPT.md](portable/PROMPT.md) lleva las reglas centrales a claude.ai, Cursor o cualquier asistente: pega y listo.

## Cómo funciona (para curiosos)

Un hook de `UserPromptSubmit` arma el contexto en cada mensaje: reglas de fábrica + tus reglas aprendidas + un resumen compacto de evidencia. Los scripts solo registran y comprimen; **todo el juicio pertenece al modelo**, y por eso no hay umbrales mágicos en ninguna parte. Una base de conocimiento ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) contiene el beneficio en una línea de cada comando y 8 jugadas combinadas; el modelo la lee bajo demanda, así que no cuesta nada por prompt. Más detalles en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills incluidas: `tutor` (tour guiado) · `doctor` (verifica que funciona) · `config` (silencio/modos) · `evolve` (destila tu evidencia en reglas) · `profile` (el panel de valor) · `whats-new` (comandos nuevos y skills sin usar, explicados por su beneficio).

## Requisitos

Python 3.8+ para la experiencia completa. Sin Python, el autopilot funciona en modo sin estado: el comportamiento central queda intacto, el aprendizaje se pausa.

## Preguntas frecuentes

**¿Mis datos se envían a algún lado?** No. Cero telemetría. Todo vive en archivos locales en `~/.claude/command-autopilot/` que puedes abrir, revisar y borrar. Al desinstalar, se elimina todo.

**¿Me va a estar molestando?** Los contratos firmes dicen que no: como mucho una sugerencia por respuesta, el mismo comando como mucho una vez por sesión, y las sugerencias que sigues descartando se apagan solas. Decir "silencia el autopilot" lo calla por completo.

**¿Cuánto cuesta?** Inyecta entre 250 y 450 tokens de reglas por mensaje según el modo (quiet ≈ 230, silenciado = 0). Es el precio honesto de la fiabilidad; tú controlas el dial.

**¿Funciona en Claude Code en la web / para mi equipo?** Sí: añade dos bloques pequeños al `.claude/settings.json` de tu repositorio ([fragmento aquí](templates/team-settings.json)) y todos los que confíen en el espacio de trabajo lo reciben, sesiones en la nube incluidas.

**No tengo Python, ¿funciona igual?** Sí, en modo sin estado: todo el comportamiento central funciona, solo la capa de aprendizaje se pausa hasta que haya Python 3.8+ disponible.

**¿Cómo lo desinstalo?** Ejecuta `claude plugin uninstall command-autopilot@claude-code-command-autopilot` (o pídeselo a Claude) y borra `~/.claude/command-autopilot/`. No queda nada.

**¿En qué se diferencia de simplemente escribir reglas en CLAUDE.md?** Lo intentamos primero, dos veces. Las reglas en CLAUDE.md pierden frente a instrucciones que compiten; la inyección por hook en cada prompt es la única ubicación que pudimos comprobar que llega al modelo el 100% de las veces. Ese hallazgo, junto con el diseño de aprendizaje sin umbrales mágicos, es toda la razón por la que esto es un plugin y no un fragmento de markdown. Detalles en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contribuir

El comportamiento vive en archivos de texto, no en código: la mayoría de las mejoras son cambios de redacción en `rules/*.txt` o entradas en `knowledge/*.json`. Lee [docs/TUNING.md](docs/TUNING.md) para la disciplina de iteración y ejecuta [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) antes de proponer cambios de comportamiento. Las traducciones de la tarjeta de hábitos y de los README son el primer PR más amigable.

Licencia MIT.
