# Joy Division — AI Writing Studio

Environnement HTML local de pilotage rédactionnel pour la production du livre *Joy Division, le son de l’éternel*.

---

## 1. Principe général

L’outil transforme l’interaction avec l’IA en processus structuré.

Chaque prompt est construit à partir de :
- la structure du chapitre
- les contraintes de périmètre
- les risques de doublon
- le registre des sources
- un atelier de travail spécifique

L’objectif n’est pas de générer du texte libre, mais de **contraindre la production intellectuelle**.

---

## 2. Utilisation

1. Ouvrir `index.html`
2. Sélectionner :
   - un chapitre
   - un atelier
   - un mode de sortie
3. Coller le texte ou les notes
4. Générer le prompt
5. Copier dans l’IA

---

## 3. Registre des sources (Excel → JSON)

Le registre est maintenu dans Excel, puis converti.

### Conversion

```bash
pip install openpyxl
python tools/convert_registre_xlsx.py mon_registre.xlsx
```

Le fichier suivant est généré :

```text
data/registre.json
```

Ce fichier est automatiquement utilisé par l’outil pour :
- afficher le statut des sources
- distinguer les sources sécurisées et fragiles
- enrichir les prompts

---

## 4. Ateliers de pilotage rédactionnel

L’outil repose sur 8 fonctions distinctes :

- Relecture de cohérence
- Vérification des sources
- Réécriture style livre
- Anti-doublons
- Transformation notes → texte
- Construction document maître
- Mise à jour du registre
- Notes de bas de page

Chaque atelier impose :
- un objectif
- des contrôles
- un format de sortie

---

## 5. Modes de sortie

- Diagnostic bref
- Tableau de contrôle
- Rédaction exploitable
- Format registre
- Rédaction chapitre complet

---

## 6. Audit de chapitre

Le système permet désormais un **audit complet du chapitre**.

Objectifs :
- vérifier la cohérence globale
- détecter les glissements hors périmètre
- identifier les redondances
- repérer les zones non sourcées
- signaler les sources fragiles utilisées

L’audit produit :
1. Diagnostic global
2. Points faibles
3. Incohérences
4. Zones à renforcer
5. Recommandations structurées

Ce mode constitue un **contrôle qualité éditorial automatisé**.

---

## 7. Architecture

```text
index.html
css/style.css
js/app.js
js/prompt-builder.js
data/chapitres.json
data/ateliers.json
data/registre.json
tools/convert_registre_xlsx.py
```

---

## 8. Positionnement

Ce projet n’est pas un générateur de texte.

C’est un système permettant :
- de structurer l’écriture
- de sécuriser les sources
- de contrôler la cohérence
- de limiter les erreurs

L’IA est utilisée comme opérateur contraint, et non comme auteur autonome.
