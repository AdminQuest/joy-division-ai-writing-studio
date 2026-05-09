# Couche documentaire — sources atomisées

Ce dossier constitue la base documentaire primaire du projet.

Chaque sous-dossier correspond à une source bibliographique, archivistique, journalistique ou universitaire.

## Objectifs

Le système vise à :

- atomiser les sources ;
- distinguer faits, citations et interprétations ;
- sécuriser les usages rédactionnels ;
- préparer automatiquement les exports ;
- limiter les erreurs de citation et les redondances.

## Structure recommandée

```text
sources/
  hook/
    source.md
    ocr.txt
    scans/
```

## Principe méthodologique

Chaque unité atomique doit :

1. porter une seule idée exploitable ;
2. être reliée à un ou plusieurs chapitres ;
3. disposer d’un statut de vérification ;
4. distinguer clairement :
   - citation exacte ;
   - paraphrase ;
   - interprétation ;
   - hypothèse.

## Logique générale

Les fiches Markdown deviennent progressivement la source maîtresse.

Les exports Excel et JSON sont ensuite générés automatiquement pour :

- le registre des références ;
- le fichier citations ;
- le tableau de cohérence thématique ;
- les ateliers de prompts.
