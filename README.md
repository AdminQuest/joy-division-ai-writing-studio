# Joy Division — AI Writing Studio

Environnement HTML local pour générer des prompts structurés destinés au pilotage de l’écriture du livre *Joy Division, le son de l’éternel*.

## Version

Version 1 : statique, locale, sans dépendance externe.

## Utilisation

1. Ouvrir `index.html` dans un navigateur.
2. Choisir un chapitre.
3. Choisir un atelier de prompt.
4. Coller le texte, les notes ou la demande.
5. Cliquer sur `Générer`.
6. Copier le prompt dans l’IA utilisée.

## Structure

```text
index.html
css/style.css
js/app.js
js/prompt-builder.js
data/chapitres.json
data/ateliers.json
docs/methode.md
docs/conventions_redactionnelles.md
outputs/prompts_generes/.gitkeep
outputs/exports/.gitkeep
```

## Ateliers disponibles

- Relecture de cohérence
- Vérification des sources
- Réécriture style livre
- Anti-doublons
- Notes vers texte
- Document maître
- Mise à jour du registre
- Notes de bas de page

## Principe

Le système impose un cadre constant : chapitre cible, fonction, hors champ, risques de doublon, sources prioritaires, conventions rédactionnelles.

Il ne remplace pas les documents maîtres, le registre ou le tableau de cohérence. Il sert à les rendre opératoires dans les échanges avec l’IA.
