# Skill Autopilot para Claude Code

**Usa las skills que has instalado, no solo las que recuerdas.**

[English](README.md) | [中文](README.zh.md) | Español | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Instalas skills para ampliar Claude Code y luego olvidas cuáles tienes, o cuándo encajan. Y la cosa *empeora* a medida que instalas más: una vez superado el presupuesto de skills de Claude Code, este descarta en silencio las descripciones de las skills que menos usas, de modo que la skill perfecta para *esta* tarea puede quedar invisible para el modelo. **Skill Autopilot saca a la luz, en cada turno, las skills instaladas más relevantes para lo que estás haciendo, así una que encaja queda frente a ti en vez de olvidada.** También despliega los movimientos de alto impacto que encajan con una tarea grande o arriesgada (agentes en paralelo, un Workflow, un /goal autónomo, investigación profunda) como un menú del que tú eliges, y se ocupa de las cosas pequeñas (deshacer, higiene de contexto) en silencio. Nuevo y experimental: código abierto, MIT, cero telemetría, local primero.

## Qué hace posible

| El momento | Sin Autopilot | Con Autopilot |
|---|---|---|
| Un trabajo grande, de varios archivos o repetitivo | Lo haces a mano paso a paso | Despliega un **menú de caminos más rápidos** (agentes en paralelo, un Workflow, /background) antes de empezar, con las ventajas y desventajas; tú eliges |
| Una tarea que debería llegar sola hasta el final | La supervisas turno a turno | Te ofrece **/goal** para que Claude trabaje hasta el final por su cuenta |
| Una pregunta que necesita investigación de verdad | Una búsqueda superficial | Ejecuta una **investigación profunda con varias fuentes** y te entrega una respuesta con citas |
| Skills que instalaste pero olvidaste | Se quedan sin usar, o se descartan del contexto cuando superas el presupuesto | **Saca a la luz las relevantes para tu tarea**, así una skill que encaja queda frente al modelo |
| Sigues rechazando una sugerencia | La mayoría de las herramientas insisten para siempre | Lee el ambiente y la deja de lado: aprende de *ti* |
| Lo básico: deshacer, contexto, comentarios al margen | Nunca aprendiste los comandos | Lo resuelve en silencio: **/rewind** antes de cualquier reparación, **/clear** al cambiar de tema, **/btw** para comentarios al margen |

**Cómo suena en la práctica:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

¿Nuevo en los comandos en sí? También mantenemos [la chuleta en lenguaje sencillo de los comandos de Claude Code](docs/claude-code-commands-cheatsheet.md) (en inglés) y [8 flujos de trabajo de Claude Code que ahorran trabajo de verdad](docs/claude-code-workflows.md) (en inglés).

Claude Code funciona con las skills y los comandos que has instalado, pero el adecuado rara vez aparece en el momento justo, y una biblioteca grande de skills lo *empeora* (al superar el presupuesto, Claude Code descarta del contexto las descripciones de las skills menos usadas). Skill Autopilot cierra esa brecha con tres movimientos:

1. **Saca a la luz las skills que encajan, justo cuando encajan.** En cada turno ordena tus skills instaladas frente a lo que de verdad estás pidiendo y pone las más relevantes frente al modelo (por su nombre; el modelo lee la descripción completa bajo demanda), incluidas las que Claude Code descartó del contexto por superar el presupuesto. Y cuando varios movimientos de alto impacto encajan con una tarea grande o arriesgada (agentes en paralelo, un Workflow, un /goal autónomo, investigación profunda), los despliega como un menú y tú eliges.
2. **El resto lo hace él mismo, en lugar de recomendar.** Lo que Claude puede hacer por su cuenta, simplemente lo hace: los cambios grandes entran en modo plan antes de tocar cualquier archivo, las preferencias se guardan en memoria, una skill instalada que encaja se usa. Lo básico de seguridad (/rewind, /clear, /btw) se te entrega en el momento exacto, nunca como un sermón.
3. **Aprende a quitarse de tu camino.** Cada sugerencia que omites es evidencia local: lo que sigues rechazando se silencia, así nunca se vuelve insistente. (La personalización más profunda, inclinarse hacia los movimientos que *tú* específicamente prefieres, está en la hoja de ruta; el logro de hoy es precisión y silencio, no fingir que ya te conoce.)

Nunca recorre una lista fija de consejos. Razona sobre cada turno, señala algo como mucho una vez cuando de verdad ayuda, y el resto del tiempo guarda silencio. La meta es que dejes de notarlo.

**¿Solo echando un vistazo?** Pega [portable/PROMPT.md](portable/PROMPT.md) en claude.ai o en cualquier asistente: el comportamiento central, sin instalar nada, en 60 segundos.

## Instalación

**Lo más fácil: deja que Claude lo instale por ti.** Copia este bloque completo, pégalo en cualquier conversación de Claude Code y pulsa Enter:

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude ejecuta la instalación y se encarga de los casos raros (el CLI fuera del PATH, etc.) por ti. No hace falta saber de terminal.

<details>
<summary>Alternativas manuales</summary>

**Terminal:**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

Si no se encuentra `claude`, usa `~/.local/bin/claude` en su lugar, o ejecuta `./install.sh` desde un clon de este repositorio.

**Dentro de una sesión del CLI de Claude Code** (el comando `/plugin` no está disponible en la app de escritorio):

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

Después reinicia Claude Code (ciérralo por completo: los hooks se cargan al arrancar) y pídele a Claude: **"comprueba que el autopilot está funcionando"**; el doctor integrado confirma que todo se dispara de principio a fin. Luego haz el tour de 2 minutos: "dame el tour del autopilot".

**¿No funciona?**
- Las sugerencias nunca aparecen → tienes que cerrar y reabrir por completo; los hooks solo se cargan al arrancar.
- `/plugin` no encontrado → la app de escritorio no tiene el comando `/plugin`; usa la instalación de copiar y pegar de arriba.
- Cualquier otra cosa → pídele a Claude que "ejecute el autopilot doctor" y pega su salida en un [issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues).

## Actualizar

Pídele a Claude: **"actualiza el plugin Skill Autopilot a la última versión."** Ejecuta por ti los tres pasos de abajo.

Hacerlo a mano (o si te sale "ya estás en la última versión", eso significa que tu copia local del marketplace está desactualizada, así que refréscala *primero*):

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
```

Después cierra y reabre Claude Code por completo: las reglas y los hooks se cargan al arrancar. (Las sesiones en la nube siempre clonan el repositorio de nuevo, así que recogen las versiones nuevas por su cuenta.)

## Velo funcionar en 2 minutos

1. Pide algo grande: *"diseña y construye una función de estadísticas para este proyecto"*. → Claude entra en **modo plan por sí solo**, antes de tocar ningún archivo. Rechaza el plan; nada cambió.
2. Haz que cree un archivo desechable y luego di *"deshaz eso"*. → Su primera reacción es ofrecerte **/rewind (Esc Esc)**, no parchear hacia adelante.

## Lo que nunca hará

- **Nada de telemetría.** Toda la evidencia vive en archivos locales que puedes abrir, revisar y borrar. Desinstalar lo elimina todo.
- **Nada de insistencia.** Contratos firmes: como mucho una sugerencia por respuesta, el mismo comando como mucho una vez por sesión, y el modo silencioso o el silencio total están a una frase de distancia ("silencia el autopilot"). Las sugerencias que descartas repetidamente se apagan solas.
- **Nada de valor inventado.** Pregunta "¿qué ha hecho el autopilot por mí?" y cada número del informe se remonta a un evento real registrado.

## El costo, sin rodeos

El autopilot inyecta sus reglas en cada prompt: entre 500 y 600 tokens aproximadamente en régimen estable (menos en `quiet`, 0 cuando está silenciado). En los turnos donde las skills instaladas son relevantes, añade sus nombres: un pequeño extra acotado (~140 tokens), con tope, y nada en los turnos donde ninguna encaja. Frente a una ventana de contexto de 200k, eso es una fracción de un porcentaje. Tú controlas el dial: `teaching` → `normal` → `quiet` → silencio total.

## Funciona en la nube y para equipos

Las sesiones en la nube no cargan tus plugins personales, y tampoco refrescan la caché del marketplace; así que la forma fiable de tener el autopilot en Claude Code en la web y para tus compañeros de equipo es **incorporar sus reglas a tu repositorio**: haz commit de un pequeño `.claude/autopilot-context.json` (las reglas) más `.claude/autopilot-cloud.sh`, y conéctale los hooks `SessionStart` + `UserPromptSubmit` en el `.claude/settings.json` de tu repositorio. Desde un clon de este repositorio, un solo comando copia los archivos e imprime las líneas exactas de los hooks:

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

Las nuevas sesiones en la nube clonan tu repositorio de cero, así que recogen las reglas automáticamente, para todos los que trabajen en ese repositorio. (Salvedad de la nube: ahí el estado de aprendizaje es por sesión; el menú en el momento sigue funcionando.)

## Cómo funciona (para curiosos)

Un único hook de `UserPromptSubmit` arma el contexto en cada mensaje: una disciplina de pensamiento breve + las skills instaladas más relevantes para tu prompt + tus reglas aprendidas + un resumen compacto de evidencia. El aflorar de skills es deliberadamente tonto y honesto: al inicio de la sesión construye un índice local de tus skills instaladas, y en cada turno las ordena por una coincidencia barata de palabras con tu prompt e inyecta solo los pocos *nombres* más relevantes (el modelo lee cada descripción completa bajo demanda y decide si usa alguna); no se inyecta nada cuando nada encaja. **No hay tabla de búsqueda escenario→comando** ni un calculador de similitud al que se le diga al modelo que confíe: el modelo razona de nuevo en cada turno sobre lo que necesita *tu* tarea; la base de conocimiento es referencia, no disparadores. Los scripts solo registran y comprimen: **todo el juicio pertenece al modelo**, por eso no hay umbrales mágicos en ninguna parte. Una base de conocimiento ([commands.json](plugins/skill-autopilot/knowledge/commands.json), [playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json)) contiene el beneficio en una línea de cada comando y un conjunto de jugadas combinadas; el modelo la lee bajo demanda, así que no cuesta nada por prompt. Más detalles en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills incluidas: `tutor` (tour guiado) · `doctor` (verifica que funciona) · `config` (silencio/modos) · `evolve` (destila tu evidencia en reglas) · `profile` (el panel de valor) · `whats-new` (comandos nuevos y skills sin usar, explicados por su beneficio).

## Requisitos

Python 3.8+ para la experiencia completa. Sin Python, el autopilot funciona en modo sin estado: el comportamiento central queda intacto, el aprendizaje se pausa.

## Preguntas frecuentes

**¿Mis datos se envían a algún lado?** No. Cero telemetría. Todo vive en archivos locales en `~/.claude/command-autopilot/` que puedes abrir, revisar y borrar. Al desinstalar, se elimina todo.

**¿Me oculta algo?** No. Pídele a Claude "¿qué te está guiando?" o que muestre la instrucción que este plugin inyecta, y te lo dirá por completo: las reglas son texto plano en [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules), y la guía le indica explícitamente a Claude que sea transparente siempre que preguntes. Nada del plugin es secreto para ti.

**¿Me va a estar molestando?** Los contratos firmes dicen que no: como mucho una sugerencia por respuesta, el mismo comando como mucho una vez por sesión, y las sugerencias que sigues descartando se apagan solas. Decir "silencia el autopilot" lo calla por completo.

**¿Cuánto cuesta?** Entre 500 y 600 tokens de reglas por mensaje en régimen estable (menos en quiet, 0 cuando está silenciado), más un pequeño extra acotado (~140 tokens) en los turnos donde las skills instaladas son relevantes: una fracción de un porcentaje de una ventana de 200k. Tú controlas el dial.

**¿Funciona en Claude Code en la web / para mi equipo?** Sí: incorpora sus reglas al `.claude/` de tu repositorio con un solo comando (`vendor-to-repo.sh`, ver [Funciona en la nube y para equipos](#funciona-en-la-nube-y-para-equipos)). Las sesiones en la nube clonan el repositorio de cero y las recogen, así que todos los que trabajen en ese repositorio lo tienen.

**No tengo Python, ¿funciona igual?** Sí, en modo sin estado: todo el comportamiento central funciona, solo la capa de aprendizaje se pausa hasta que haya Python 3.8+ disponible.

**¿Cómo lo desinstalo?** Ejecuta `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot` (o pídeselo a Claude) y borra `~/.claude/command-autopilot/`. No queda nada.

**¿En qué se diferencia de simplemente escribir reglas en CLAUDE.md?** Lo intentamos primero, dos veces. Las reglas en CLAUDE.md pierden frente a instrucciones que compiten; la inyección por hook en cada prompt es la única ubicación que pudimos comprobar que llega al modelo el 100% de las veces. Ese hallazgo, junto con el diseño de aprendizaje sin umbrales mágicos, es toda la razón por la que esto es un plugin y no un fragmento de markdown. Detalles en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contribuir

**Tu primer PR en 5 minutos:** mejora la redacción de una sugerencia en `plugins/skill-autopilot/rules/*.txt`, o añade el beneficio en una línea de un comando a `plugins/skill-autopilot/knowledge/commands.json`, ejecuta el paso correspondiente en [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) y envíalo. Las traducciones del README son igual de bienvenidas. El comportamiento vive en archivos de texto, no en código: lee [docs/TUNING.md](docs/TUNING.md) para la disciplina de iteración.

Licencia MIT.
