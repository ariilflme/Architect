# Brief NQ · ES — déroulé d'une exécution

Lancé chaque jour de bourse à 08h45 (Paris) par une tâche planifiée. Lecture seule : aucun ordre, aucun courtier.

Page : https://claude.ai/artifact/77T9cZME7Crbx6WiqmSm2g (collection `rapports`, un document par jour, id = `AAAA-MM-JJ`).

## Équipe (`.claude/agents/`)

| Agent | Rôle | Sortie |
|---|---|---|
| `marche-collecteur` | Niveaux et signaux NQ/ES (`niveaux.py`) | `marche.json` |
| `veille-news` | 5 à 8 titres utiles sur QQQ/SPY (`actus.py`) | `news.json` |
| `contexte-crypto` | Régime crypto TEXT_TO_QUANT (gratuit, si le connecteur est là) | `crypto.json` |
| `redacteur-rapport` | Assemble le rapport en français | `rapport.json` |

## Étapes

1. Si on est un samedi, un dimanche ou un jour férié de la bourse US (NYSE), arrête-toi sans rien écrire.
2. Crée un dossier de travail vide : `WORK=$(mktemp -d)`. Aucun code extérieur n'est téléchargé : les deux scripts du dossier `scripts/market-brief/` utilisent seulement la bibliothèque standard de Python.
3. Lance en parallèle `marche-collecteur`, `veille-news` et `contexte-crypto`, en leur donnant le chemin `WORK` et la racine du dépôt.
4. Quand les trois ont fini (même en erreur), lance `redacteur-rapport` avec `WORK`.
5. Écris `$WORK/rapport.json` dans la page avec l'outil `ArtifactData` : action `set`, url de la page, collection `rapports`, doc_id = la date du rapport (`file_path` = `$WORK/rapport.json`). Si le document du jour existe déjà (relance), lis-le avec `get` et passe sa `version` en `if_version`.
6. Termine par une phrase de résumé (elle sert de notification push).

Si une source est en panne, le rapport part quand même avec la section marquée indisponible.
