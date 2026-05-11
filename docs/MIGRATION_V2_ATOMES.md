# Migration v2 — Atomes enrichis

## Objet

Ce document décrit la migration du repo vers le modèle d’atomisation enrichie v2.

La version v2 transforme les atomes :

```text
fragment documentaire
→ unité de raisonnement historiographique
```

Le repo cesse progressivement d’être un stockage documentaire linéaire.

Il devient :

```text
un système de connaissances éditoriales piloté par IA.
```

---

# 1. Principe fondamental

Les anciennes atomisations ne doivent pas être supprimées.

Elles constituent :

- le socle documentaire ;
- la mémoire du projet ;
- l’archive de travail ;
- la couche de factualisation initiale.

La migration consiste donc :

- à enrichir ;
- qualifier ;
- relier ;
- stabiliser.

Pas à réécrire brutalement tout le corpus.

---

# 2. Les trois couches documentaires du repo

Le repo distingue désormais trois niveaux.

## Niveau 1 — Sources

Exemples :

- Hook ;
- Deborah Curtis ;
- Reynolds ;
- Johnson ;
- archives ;
- interviews ;
- bootlegs ;
- documents académiques.

Ces fichiers restent les sources documentaires primaires.

---

## Niveau 2 — Atomes

Les atomes représentent :

- faits ;
- lectures ;
- concepts ;
- citations ;
- controverses ;
- mythes.

Ils sont désormais enrichis par :

- rôle argumentatif ;
- niveau de preuve ;
- stabilité ;
- importance ;
- risque de surinterprétation ;
- motifs ;
- concepts dérivés.

---

## Niveau 3 — Documents maîtres

Les documents maîtres changent de statut.

Ils ne doivent plus être considérés comme des sources documentaires primaires.

Ils deviennent :

- cartes argumentatives ;
- couches de synthèse ;
- pré-manuscrits ;
- systèmes de pilotage éditorial.

Ils servent à :

- identifier les manques ;
- détecter les redondances ;
- hiérarchiser les concepts ;
- orienter les enrichissements d’atomes ;
- équilibrer la narration.

---

# 3. Migration minimale obligatoire

Tous les anciens atomes doivent recevoir les nouveaux champs minimaux.

Modèle minimal :

```yaml
role_argumentatif:
  - documentation générale

niveau_preuve:
  statut: corrobore
  corroboration: moyenne
  confiance: moyenne

stabilite:
  statut: assez_stable
  risque_revision: moyen

importance:
  niveau: moyenne

risque_surinterpretation:
  niveau: moyen

liens_interchapitres:
  - Chapitre 1

liens_citations: []

motifs: []

concepts_derives: []
```

Cette étape vise uniquement :

- la compatibilité parseur ;
- la cohérence structurelle ;
- la normalisation documentaire.

Elle ne constitue pas encore un enrichissement intellectuel complet.

---

# 4. Priorisation de l’enrichissement

Le repo ne doit pas être enrichi uniformément.

Principe :

```text
20 % des atomes structurent 80 % du livre.
```

Les enrichissements détaillés doivent viser en priorité :

- Manchester post-industrielle ;
- Factory Records ;
- Martin Hannett ;
- Unknown Pleasures ;
- Ian Curtis ;
- la spatialisation sonore ;
- les sessions RCA ;
- les mythologies postérieures ;
- les concepts centraux.

---

# 5. Distinction critique des types documentaires

Le repo doit désormais distinguer explicitement :

| Type | Nature |
|---|---|
| fait | information établie |
| lecture | interprétation analytique |
| concept | outil théorique |
| citation_clef | citation structurante |
| mythe | reconstruction symbolique |
| controverse | désaccord documentaire |

Cette séparation devient fondamentale pour éviter :

- la confusion mémoire/fait ;
- la téléologie ;
- la mythologisation de Joy Division ;
- les glissements interprétatifs.

---

# 6. Doctrine sur les documents maîtres

Les documents maîtres ne doivent plus être atomisés comme des livres-source.

Ils doivent servir à :

- identifier les atomes réellement utilisés ;
- cartographier les chaînes argumentatives ;
- détecter les tunnels théoriques ;
- mesurer la densité conceptuelle ;
- repérer les répétitions ;
- surveiller les risques de surinterprétation.

Les documents maîtres deviennent donc :

```text
des couches de supervision éditoriale.
```

---

# 7. Chantiers futurs

## Court terme

- migration minimale des anciens atomes ;
- génération des diagnostics v2 ;
- qualification progressive des atomes centraux.

## Moyen terme

- graphes documentaires ;
- propagation conceptuelle ;
- cartographie des motifs ;
- détection automatique des redondances.

## Long terme

- RAG sémantique ;
- scoring historiographique ;
- moteur de cohérence narrative ;
- pilotage éditorial assisté par IA.
