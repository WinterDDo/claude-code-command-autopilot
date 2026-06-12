# Command Autopilot pour Claude Code

**Utilisez Claude Code à 100 % sans mémoriser une seule commande.**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | Français | [Deutsch](README.de.md)

Conçu pour celles et ceux qui utilisent Claude Code sans jamais avoir touché aux commandes `/`. Si vous avez déjà perdu du travail sans savoir que vous pouviez l'annuler, ou regardé Claude se lancer tête baissée dans une grosse modification que vous auriez aimé voir planifiée d'abord, ce projet est fait pour vous.

## Ce qui change concrètement après l'installation

| Le moment | Sans Autopilot | Avec Autopilot |
|---|---|---|
| Claude casse quelque chose | Vous ignorez que l'annulation existe ; Claude continue à « réparer » | Il vous tend d'abord **/rewind** : deux fois Échap, et vous revoilà avant les dégâts |
| Vous demandez quelque chose de gros | Claude se met à modifier immédiatement | Il **planifie d'abord, automatiquement** : rien ne change tant que vous n'avez pas validé |
| Vous changez de sujet en pleine session | L'ancien contexte vous ralentit et vous coûte de l'argent | Un choix cliquable apparaît : continuer / repartir à neuf / ouvrir une session dédiée, chacun avec sa raison |
| Les skills que vous avez installés dorment | Vous aviez oublié que vous les aviez | Il les utilise et vous le dit : « votre skill pdf a servi : fichier lu directement » |
| Vous ignorez sans cesse une suggestion | La plupart des outils insistent indéfiniment | Il comprend le message et se tait : il apprend à *vous* connaître |

Claude Code propose une centaine de commandes slash intégrées, plus tous les skills que vous avez installés. Les débutants n'en connaissent presque aucune : ils perdent donc du travail qu'une seule touche aurait pu restaurer, gaspillent du contexte qu'ils auraient pu nettoyer, et regardent Claude foncer dans de grosses modifications qui méritaient d'abord un plan.

Command Autopilot règle cela en trois gestes :

1. **Il agit au lieu de recommander.** Ce que Claude peut faire lui-même, il le fait, tout simplement : les grosses modifications passent automatiquement en mode plan avant de toucher au moindre fichier, vos préférences sont notées en mémoire, vos skills installés sont utilisés (et il vous dit, en une ligne, lequel vient de vous aider).
2. **Il vous tend la commande avant le moment décisif, jamais après.** Les commandes que vous seul pouvez utiliser (/rewind, /clear...) arrivent sous forme de choix cliquables, pile au croisement qu'elles résolvent, chacune avec son bénéfice en une ligne, pour que vous sachiez pourquoi vous appuyez.
3. **Il évolue avec vous.** Chaque suggestion acceptée ou ignorée est une preuve, conservée en local. L'autopilote lit l'ambiance : ce que vous rejetez régulièrement se tait, ce qui vous aide arrive plus tôt, et environ toutes les 10 sessions il condense votre usage en règles personnalisées, visibles, appuyées sur des preuves, et supprimables.

Il enseigne exactement **quatre habitudes** (/clear, /btw, /rewind, le mode plan), chacune quelques fois tout au plus, puis se fait oublier. L'objectif : que vous cessiez de le remarquer.

## Installation

**Le plus simple : laissez Claude l'installer pour vous.** Copiez ce bloc en entier, collez-le dans n'importe quelle conversation Claude Code, appuyez sur Entrée :

```
Installe le plugin Command Autopilot pour moi :
1. Localise mon CLI claude : essaie `command -v claude` ; s'il n'est pas dans le PATH, essaie `~/.local/bin/claude`
   (l'emplacement habituel sur macOS/Linux). Si besoin, utilise le chemin complet dans les étapes suivantes.
2. Exécute : claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. Exécute : claude plugin install command-autopilot@claude-code-command-autopilot
4. Montre-moi les deux confirmations de réussite, puis rappelle-moi de quitter complètement Claude Code et de le rouvrir.
```

Claude exécute l'installation et gère les cas particuliers (CLI absent du PATH, etc.) à votre place. Aucune connaissance du terminal n'est nécessaire.

<details>
<summary>Alternatives manuelles</summary>

**Terminal :**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

Si `claude` est introuvable, utilisez `~/.local/bin/claude` à la place, ou lancez `./install.sh` depuis un clone de ce dépôt.

**Dans une session Claude Code en ligne de commande** (la commande `/plugin` n'est pas disponible dans l'application de bureau) :

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

Redémarrez ensuite Claude Code (quittez-le complètement : les hooks se chargent au démarrage) et essayez la visite guidée de 2 minutes : demandez à Claude « fais-moi visiter l'autopilote ».

## Voyez-le à l'œuvre en 2 minutes

1. Demandez quelque chose de gros : *« conçois et construis une fonctionnalité de statistiques pour ce projet. »* → Claude passe **en mode plan de lui-même**, avant de toucher au moindre fichier. Refusez le plan ; rien n'a changé.
2. Faites-lui créer un fichier jetable, puis dites *« annule ça. »* → Son premier réflexe est de vous tendre **/rewind (Échap Échap)**, pas de rafistoler en avançant.

## Ce qu'il ne fera jamais

- **Aucune télémétrie.** Toutes les preuves vivent dans des fichiers locaux que vous pouvez ouvrir, inspecter et supprimer. La désinstallation efface tout.
- **Aucun harcèlement.** Contrats stricts : au plus une suggestion par réponse, la même commande au plus une fois par session, et le mode discret ou le silence total ne sont qu'à une phrase (« coupe l'autopilote »). Les suggestions rejetées à répétition s'éteignent d'elles-mêmes.
- **Aucune valeur inventée.** Demandez « qu'est-ce que l'autopilote a fait pour moi » : chaque chiffre du rapport remonte à un événement réellement enregistré.

## Le coût, en toute honnêteté

L'autopilote injecte ses règles dans chaque prompt : environ 250 à 450 tokens selon le mode (discret ≈ 230, coupé = 0). C'est le prix du seul emplacement dont l'efficacité est démontrée. Le réglage vous appartient : `teaching` → `normal` → `quiet` → silence.

## Fonctionne dans le cloud et en équipe

Les sessions cloud ne chargent pas votre configuration personnelle. Pour Claude Code sur le web et pour vos coéquipiers, ajoutez donc ceci au fichier `.claude/settings.json` de votre dépôt (extrait complet dans [templates/team-settings.json](templates/team-settings.json)) :

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

Toute personne qui fait confiance à l'espace de travail reçoit l'autopilote, en local comme dans les sessions cloud. (Limites du cloud : les invites de configuration n'y apparaissent pas, les valeurs par défaut s'appliquent donc ; l'état d'apprentissage repart de zéro à chaque session cloud.)

Pas de Claude Code du tout ? [portable/PROMPT.md](portable/PROMPT.md) transporte les règles essentielles vers claude.ai, Cursor ou n'importe quel assistant : collez, c'est parti.

## Comment ça marche (pour les curieux)

Un seul hook `UserPromptSubmit` assemble le contexte à chaque message : règles d'origine + vos règles apprises + un condensé compact des preuves. Les scripts se contentent d'enregistrer et de compresser : **tout le jugement revient au modèle**, et c'est pourquoi il n'y a aucun seuil magique nulle part. Une base de connaissances ([commands.json](plugins/command-autopilot/knowledge/commands.json), [playbooks.json](plugins/command-autopilot/knowledge/playbooks.json)) recense le bénéfice en une ligne de chaque commande ainsi que 8 playbooks combinés ; le modèle la consulte à la demande, elle ne coûte donc rien par prompt. Détails dans [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Skills inclus : `tutor` (visite guidée) · `doctor` (vérifier que tout fonctionne) · `config` (silence/modes) · `evolve` (condenser vos preuves en règles) · `profile` (le tableau de bord de valeur) · `whats-new` (nouvelles commandes et skills inutilisés, expliqués par leur bénéfice).

## Prérequis

Python 3.8+ pour l'expérience complète. Sans Python, l'autopilote tourne en mode sans état : comportement de base intact, apprentissage en pause.

## FAQ

**Mes données sont-elles envoyées quelque part ?** Non. Zéro télémétrie. Tout vit dans des fichiers locaux sous `~/.claude/command-autopilot/` que vous pouvez ouvrir, inspecter et supprimer. La désinstallation efface tout.

**Va-t-il me harceler ?** Les contrats stricts disent non : au plus une suggestion par réponse, la même commande au plus une fois par session, et les suggestions que vous rejetez sans cesse s'éteignent d'elles-mêmes. Dire « coupe l'autopilote » le réduit au silence complet.

**Combien ça coûte ?** Il injecte environ 250 à 450 tokens de règles par message selon le mode (discret ≈ 230, coupé = 0). C'est le prix honnête de la fiabilité ; le réglage vous appartient.

**Fonctionne-t-il dans Claude Code sur le web / pour mon équipe ?** Oui : ajoutez deux petits blocs au `.claude/settings.json` de votre dépôt ([extrait ici](templates/team-settings.json)) et toute personne qui fait confiance à l'espace de travail en profite, sessions cloud comprises.

**Je n'ai pas Python, ça marche quand même ?** Oui, en mode sans état : tout le comportement de base fonctionne, seule la couche d'apprentissage reste en pause tant que Python 3.8+ n'est pas disponible.

**Comment désinstaller ?** Lancez `claude plugin uninstall command-autopilot@claude-code-command-autopilot` (ou demandez à Claude de le faire), puis supprimez `~/.claude/command-autopilot/`. Il ne reste rien.

**En quoi est-ce différent de simples règles dans CLAUDE.md ?** Nous avons d'abord essayé cela, deux fois. Les règles écrites dans CLAUDE.md perdent face aux instructions concurrentes ; l'injection par hook à chaque prompt est le seul emplacement dont nous avons pu prouver qu'il atteint le modèle 100 % du temps. Cette découverte, ajoutée à un apprentissage conçu sans seuils magiques, est toute la raison pour laquelle ceci est un plugin et non un simple extrait markdown. Détails dans [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contribuer

Le comportement vit dans des fichiers texte, pas dans du code : la plupart des améliorations sont des reformulations dans `rules/*.txt` ou des entrées dans `knowledge/*.json`. Lisez [docs/TUNING.md](docs/TUNING.md) pour la discipline d'itération, et déroulez [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) avant de proposer un changement de comportement. Traduire la carte des habitudes et les READMEs est la première contribution la plus accueillante.

Sous licence MIT.
