# Schémas documentaires

Ce dossier définit les formats canoniques du système documentaire.

Objectif :
- empêcher la dérive des fichiers Markdown ;
- stabiliser les clés YAML ;
- faciliter les futurs parseurs ;
- préparer les exports CSV/JSON ;
- sécuriser le futur moteur RAG.

## Principe

Les fichiers `*.schema.yaml` ne sont pas encore des schémas JSON stricts.
Ils constituent une norme documentaire interne lisible par l’humain et par l’IA.

Ils définissent :
- les champs obligatoires ;
- les champs recommandés ;
- les valeurs contrôlées ;
- les règles d’usage ;
- les risques à éviter.

## Schémas disponibles

| Fichier | Objet |
|---|---|
| `atom.schema.yaml` | Unité atomique documentaire |
| `quote.schema.yaml` | Citation exacte normalisée |
| `chronology.schema.yaml` | Événement chronologique |
| `song.schema.yaml` | Entrée du registre chansons |
| `person.schema.yaml` | Entrée du registre personnes |

## Règle fondamentale

Tout nouveau fichier d’atomisation ou de registre doit respecter ces schémas.

En cas de doute, ne pas inventer de champ : utiliser `notes` ou `methodological_warnings`.
