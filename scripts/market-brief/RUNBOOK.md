# Brief NQ · ES — déroulé d'une exécution

Lancé chaque jour de bourse à 08h45 (Paris) par une tâche planifiée. Lecture seule : aucun ordre, aucun courtier.

Page : https://claude.ai/artifact/77T9cZME7Crbx6WiqmSm2g (collection `rapports`, un document par jour, id = `AAAA-MM-JJ`).

## Équipe (`.claude/agents/`)

| Agent | Rôle | Sortie |
|---|---|---|
| `marche-collecteur` | Niveaux NQ/ES (`niveaux.py`) + signaux du scanner day-trader-fr | `marche.json` |
| `veille-news` | 5 à 8 titres utiles sur QQQ/SPY (trader-news) | `news.json` |
| `contexte-crypto` | Régime crypto TEXT_TO_QUANT (gratuit) | `crypto.json` |
| `redacteur-rapport` | Assemble le rapport en français | `rapport.json` |

## Étapes

1. Si on est un samedi, un dimanche ou un jour férié de la bourse US (NYSE), arrête-toi sans rien écrire.
2. Crée un dossier de travail vide `WORK=$(mktemp -d)` et clone day-trader-fr épinglé :
   `git clone -q https://github.com/dan-ai-lab/day-trader-fr.git $WORK/day-trader-fr && git -C $WORK/day-trader-fr checkout -q 756e4f5`
   Ne mets jamais à jour ce commit sans une nouvelle relecture demandée par l'utilisateur.
3. Lance en parallèle `marche-collecteur`, `veille-news` et `contexte-crypto`, en leur donnant le chemin `WORK` et la racine du dépôt.
4. Quand les trois ont fini (même en erreur), lance `redacteur-rapport` avec `WORK`.
5. Écris `$WORK/rapport.json` dans la page avec l'outil `ArtifactData` : action `set`, url de la page, collection `rapports`, doc_id = la date du rapport.
6. Termine par une phrase de résumé (elle sert de notification push).

Si une source est en panne, le rapport part quand même avec la section marquée indisponible.
