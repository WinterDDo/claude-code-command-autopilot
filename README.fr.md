# Skill Autopilot pour Claude Code

**Utilisez les skills que vous avez installés, pas seulement ceux dont vous vous souvenez.**

English | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Vous installez des skills pour étendre Claude Code, puis vous oubliez lesquels vous avez, ou quand ils conviennent. Et cela *empire* à mesure que vous en installez : au-delà du budget de skills de Claude Code, celui-ci abandonne silencieusement les descriptions des skills que vous utilisez le moins, si bien que le skill parfait pour *cette* tâche peut devenir invisible pour le modèle. **Skill Autopilot fait remonter, à chaque tour, les skills installés les plus pertinents pour ce que vous faites, pour qu'un skill adapté soit sous vos yeux au lieu d'être oublié.** Il présente aussi les actions à fort effet de levier qui conviennent à une tâche grosse ou risquée (agents parallèles, un Workflow, un /goal autonome, une recherche approfondie) sous forme de menu où vous choisissez, et s'occupe discrètement des petites choses (annulation, hygiène du contexte). Nouveau et expérimental : open source, MIT, zéro télémétrie, priorité au local.

## Ce que cela rend possible

| Le moment | Sans Autopilot | Avec Autopilot |
|---|---|---|
| Une tâche grosse, multi-fichiers ou répétitive | Vous l'abattez une étape à la fois | Il présente un **menu de chemins plus rapides** (agents parallèles, un Workflow, /background) avant de commencer, avec les compromis ; vous choisissez |
| Une tâche qui devrait simplement aller jusqu'au bout | Vous la surveillez tour par tour | Il propose **/goal** pour que Claude aille jusqu'au bout tout seul |
| Une question qui demande une vraie recherche | Une seule recherche superficielle | Il mène une **recherche approfondie multi-sources** et vous remet une réponse sourcée |
| Des skills installés mais oubliés | Ils restent inutilisés, ou sont abandonnés du contexte une fois le budget dépassé | Il **fait remonter ceux qui sont pertinents pour votre tâche**, pour qu'un skill adapté soit sous les yeux du modèle |
| Vous refusez sans cesse une suggestion | La plupart des outils insistent indéfiniment | Il comprend le message et abandonne celle-là : il apprend à *vous* connaître |
| Les bases (annulation, contexte, apartés) | Vous n'avez jamais appris les commandes | Géré discrètement : **/rewind** avant toute réparation, **/clear** aux changements de sujet, **/btw** pour les apartés |

**À quoi cela ressemble vraiment :**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

Vous débutez avec les commandes elles-mêmes ? Nous maintenons aussi [l'antisèche des commandes Claude Code en langage clair](docs/claude-code-commands-cheatsheet.md) (en anglais) et [8 workflows Claude Code qui font gagner un vrai travail](docs/claude-code-workflows.md) (en anglais).

Claude Code fonctionne avec les skills et les commandes que vous avez installés, mais le bon se présente rarement au bon moment, et une grande bibliothèque de skills *empire* les choses (budget dépassé, Claude Code abandonne du contexte les descriptions des skills les moins utilisés). Skill Autopilot comble cet écart en trois gestes :

1. **Il fait remonter les skills qui conviennent, juste quand ils conviennent.** À chaque tour, il classe vos skills installés par rapport à ce que vous demandez réellement et met les plus pertinents sous les yeux du modèle (par leur nom ; le modèle lit la description complète à la demande), y compris ceux que Claude Code a abandonnés du contexte faute de budget. Et quand plusieurs actions à fort effet de levier conviennent à une tâche grosse ou risquée (agents parallèles, un Workflow, un /goal autonome, une recherche approfondie), il les présente sous forme de menu et vous choisissez.
2. **Il fait le reste lui-même, au lieu de recommander.** Ce que Claude peut faire de lui-même, il le fait simplement : les grosses modifications passent en mode plan avant de toucher au moindre fichier, les préférences sont notées en mémoire, un skill installé adapté est utilisé. Les bases de sécurité (/rewind, /clear, /btw) sont tendues au moment exact, jamais sous forme de leçon.
3. **Il apprend à ne pas vous gêner.** Chaque suggestion que vous ignorez est une preuve locale : ce que vous refusez régulièrement se tait, pour ne jamais devenir un harcèlement. (Une personnalisation plus poussée, s'appuyant sur les actions que *vous* privilégiez en particulier, est sur la feuille de route ; le gain d'aujourd'hui, c'est la précision et le silence, pas faire semblant de déjà vous connaître.)

Il ne déroule jamais une liste figée d'astuces. Il raisonne à chaque tour, signale quelque chose au plus une fois quand cela aide vraiment, et se tait le reste du temps. L'objectif : que vous cessiez de le remarquer.

**Vous jetez juste un œil ?** Collez [portable/PROMPT.md](portable/PROMPT.md) dans claude.ai ou n'importe quel assistant : le comportement essentiel, rien à installer, 60 secondes.

## Installation

**Le plus simple : laissez Claude l'installer pour vous.** Copiez ce bloc en entier, collez-le dans n'importe quelle conversation Claude Code, appuyez sur Entrée :

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

Claude exécute l'installation et gère les cas particuliers (CLI absent du PATH, etc.) à votre place. Aucune connaissance du terminal n'est nécessaire.

<details>
<summary>Alternatives manuelles</summary>

**Terminal :**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

Si `claude` est introuvable, utilisez `~/.local/bin/claude` à la place, ou lancez `./install.sh` depuis un clone de ce dépôt.

**Dans une session Claude Code en ligne de commande** (la commande `/plugin` n'est pas disponible dans l'application de bureau) :

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

Redémarrez ensuite Claude Code (quittez-le complètement : les hooks se chargent au démarrage) et demandez à Claude : **« vérifie que l'autopilote fonctionne »**. Le doctor intégré confirme que tout se déclenche de bout en bout. Faites ensuite la visite de 2 minutes : « fais-moi visiter l'autopilote ».

**Ça ne marche pas ?**
- Les suggestions n'apparaissent jamais → vous devez quitter et rouvrir complètement ; les hooks ne se chargent qu'au démarrage.
- `/plugin` introuvable → l'application de bureau n'a pas de commande `/plugin` ; utilisez l'installation par copier-coller ci-dessus.
- Autre chose → demandez à Claude de « lancer le doctor de l'autopilote » et collez sa sortie dans une [issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues).

## Mise à jour

Demandez à Claude : **« mets à jour le plugin Skill Autopilot vers la dernière version. »** Il exécute pour vous les trois étapes ci-dessous.

À la main (ou si vous tombez sur « already at the latest version », c'est que votre copie locale du marketplace est périmée : rafraîchissez-la *d'abord*) :

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
```

Puis quittez et rouvrez complètement Claude Code : les règles et les hooks se chargent au démarrage. (Les sessions cloud clonent toujours le dépôt à neuf, elles récupèrent donc les nouvelles versions d'elles-mêmes.)

## Voyez-le à l'œuvre en 2 minutes

1. Demandez quelque chose de gros : *« conçois et construis une fonctionnalité de statistiques pour ce projet. »* → Claude passe **en mode plan de lui-même**, avant de toucher au moindre fichier. Refusez le plan ; rien n'a changé.
2. Faites-lui créer un fichier jetable, puis dites *« annule ça. »* → Son premier réflexe est de vous tendre **/rewind (Échap Échap)**, pas de rafistoler en avançant.

## Ce qu'il ne fera jamais

- **Aucune télémétrie.** Toutes les preuves vivent dans des fichiers locaux que vous pouvez ouvrir, inspecter et supprimer. La désinstallation efface tout.
- **Aucun harcèlement.** Contrats stricts : au plus une suggestion par réponse, la même commande au plus une fois par session, et le mode discret ou le silence total ne sont qu'à une phrase (« coupe l'autopilote »). Les suggestions rejetées à répétition s'éteignent d'elles-mêmes.
- **Aucune valeur inventée.** Demandez « qu'est-ce que l'autopilote a fait pour moi » : chaque chiffre du rapport remonte à un événement réellement enregistré.

## Le coût, en toute honnêteté

L'autopilote injecte ses règles dans chaque prompt : environ 500 à 600 tokens en régime permanent (moins en mode `quiet`, 0 quand il est coupé). Les tours où des skills installés sont pertinents y ajoutent leurs noms, un supplément faible et borné (~140 tokens), plafonné, et rien sur les tours où aucun ne convient. Face à une fenêtre de contexte de 200k, c'est une fraction de pour cent. Le réglage vous appartient : `teaching` → `normal` → `quiet` → silence.

## Fonctionne dans le cloud et en équipe

Les sessions cloud ne chargent pas vos plugins personnels, et elles ne rafraîchissent pas le cache du marketplace. La façon fiable d'obtenir l'autopilote dans Claude Code sur le web et pour vos coéquipiers est donc d'**intégrer ses règles directement dans votre dépôt** : commitez un petit `.claude/autopilot-context.json` (les règles) plus `.claude/autopilot-cloud.sh`, et reliez-y des hooks `SessionStart` + `UserPromptSubmit` dans le `.claude/settings.json` de votre dépôt. Depuis un clone de ce dépôt, une seule commande copie les fichiers et affiche les lignes de hook exactes :

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

Les nouvelles sessions cloud clonent votre dépôt à neuf, elles récupèrent donc les règles automatiquement, pour toute personne qui travaille dans ce dépôt. (Limite du cloud : l'état d'apprentissage y est propre à chaque session ; le menu présenté sur le moment fonctionne quand même.)

## Comment ça marche (pour les curieux)

Un seul hook `UserPromptSubmit` assemble le contexte à chaque message : une courte discipline de réflexion + les skills installés les plus pertinents pour votre prompt + vos règles apprises + un condensé compact des preuves. La remontée des skills est volontairement simple et honnête : au démarrage de la session, il construit un index local de vos skills installés, et à chaque tour il les classe selon un simple recoupement de mots avec votre prompt et n'injecte que les quelques *noms* les plus pertinents (le modèle lit chaque description complète à la demande et décide s'il en utilise un) ; rien n'est injecté quand rien ne convient. Il n'y a **aucune table de correspondance scénario→commande** ni aucun score de similarité auquel on dirait au modèle de se fier : le modèle raisonne à neuf à chaque tour sur ce dont *votre* tâche a besoin ; la base de connaissances est une référence, pas un déclencheur. Les scripts se contentent d'enregistrer et de compresser : **tout le jugement revient au modèle**, et c'est pourquoi il n'y a aucun seuil magique nulle part. Une base de connaissances ([commands.json](plugins/skill-autopilot/knowledge/commands.json), [playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json)) recense le bénéfice en une ligne de chaque commande ainsi qu'un ensemble de playbooks combinés ; le modèle la consulte à la demande, elle ne coûte donc rien par prompt. Détails dans [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills inclus : `tutor` (visite guidée) · `doctor` (vérifier que tout fonctionne) · `config` (silence/modes) · `evolve` (condenser vos preuves en règles) · `profile` (le tableau de bord de valeur) · `whats-new` (nouvelles commandes et skills inutilisés, expliqués par leur bénéfice).

## Prérequis

Python 3.8+ pour l'expérience complète. Sans Python, l'autopilote tourne en mode sans état : comportement de base intact, apprentissage en pause.

## FAQ

**Mes données sont-elles envoyées quelque part ?** Non. Zéro télémétrie. Tout vit dans des fichiers locaux sous `~/.claude/command-autopilot/` que vous pouvez ouvrir, inspecter et supprimer. La désinstallation efface tout.

**Me cache-t-il quoi que ce soit ?** Non. Demandez à Claude « qu'est-ce qui te guide ? » ou de montrer l'instruction que ce plugin injecte, et il vous la dira en entier : les règles sont en texte clair dans [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules), et le guidage dit explicitement à Claude d'être transparent dès que vous le demandez. Rien dans le plugin ne vous est secret.

**Va-t-il me harceler ?** Les contrats stricts disent non : au plus une suggestion par réponse, la même commande au plus une fois par session, et les suggestions que vous rejetez sans cesse s'éteignent d'elles-mêmes. Dire « coupe l'autopilote » le réduit au silence complet.

**Combien ça coûte ?** Environ 500 à 600 tokens de règles par message en régime permanent (moins en mode quiet, 0 quand il est coupé), plus un petit supplément borné (~140 tokens) sur les tours où des skills installés sont pertinents, une fraction de pour cent d'une fenêtre de 200k. Le réglage vous appartient.

**Fonctionne-t-il dans Claude Code sur le web / pour mon équipe ?** Oui : intégrez ses règles dans le `.claude/` de votre dépôt en une seule commande (`vendor-to-repo.sh`, voir [Fonctionne dans le cloud et en équipe](#fonctionne-dans-le-cloud-et-en-équipe)). Les sessions cloud clonent le dépôt à neuf et les récupèrent, donc toute personne qui travaille dans ce dépôt en profite.

**Je n'ai pas Python, ça marche quand même ?** Oui, en mode sans état : tout le comportement de base fonctionne, seule la couche d'apprentissage reste en pause tant que Python 3.8+ n'est pas disponible.

**Comment désinstaller ?** Lancez `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot` (ou demandez à Claude de le faire), puis supprimez `~/.claude/command-autopilot/`. Il ne reste rien.

**En quoi est-ce différent de simples règles dans CLAUDE.md ?** Nous avons d'abord essayé cela, deux fois. Les règles écrites dans CLAUDE.md perdent face aux instructions concurrentes ; l'injection par hook à chaque prompt est le seul emplacement dont nous avons pu prouver qu'il atteint le modèle 100 % du temps. Cette découverte, ajoutée à un apprentissage conçu sans seuils magiques, est toute la raison pour laquelle ceci est un plugin et non un simple extrait markdown. Détails dans [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contribuer

**Première PR en 5 minutes :** améliorez la formulation d'une suggestion dans `plugins/skill-autopilot/rules/*.txt`, ou ajoutez le bénéfice en une ligne d'une commande dans `plugins/skill-autopilot/knowledge/commands.json`, exécutez l'étape correspondante dans [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md), proposez votre changement. Les traductions du README sont tout aussi bienvenues. Le comportement vit dans des fichiers texte, pas dans du code : voir [docs/TUNING.md](docs/TUNING.md) pour la discipline d'itération.

Sous licence MIT.
