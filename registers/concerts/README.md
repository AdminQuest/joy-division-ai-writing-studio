# Registre des concerts — Joy Division / Warsaw

## Fonction du registre

Ce registre centralise l'ensemble des concerts et gigs de Joy Division
(et Warsaw / Stiff Kittens) dans leur chronologie documentée.

Il sert à :
- stabiliser les dates et lieux de concerts ;
- constituer une base factuelle pour les analyses live (présence scénique,
  diffusion géographique, évolution du répertoire) ;
- relier concerts, atomes documentaires, chronologie maître et chansons ;
- préparer les exports CSV/JSON et alimenter le moteur RAG ;
- identifier les lacunes dans le registre chronologique maître.

Le registre ne doit pas devenir une encyclopédie de setlists ou un journal
de tournée narratif. Il reste factuel, traçable, relationnel.

---

## Source canonique primaire

| Champ | Valeur |
|-------|--------|
| ID source | `REGISTRY-CONCERTS` |
| URL | https://joydiv.org/concerts.htm |
| Auteur | Tony Nuttall |
| Statut | `reference_externe` |
| Fiabilité | `haute` |
| Consultation | en attente (accès réseau limité dans l'environnement) |

---

## Structure normalisée d'une entrée

```yaml
id: JD-CONCERT-YYYYMMDD-001
date: YYYY-MM-DD
date_display: "jour mois année"
lieu: "Nom de la salle"
ville: "Ville"
pays: "Pays"
alias_groupe: "Joy Division"  # obligatoire avant janv. 1978
setlist: []
sources: [REGISTRY-CONCERTS]
atomes_lies: []
chronologie_id: ""            # CHR-XXXX-XXX si entrée dans master_chronology
notes: ""
```

### Conventions d'identifiant

- Format : `JD-CONCERT-YYYYMMDD-NNN`
- NNN = index sur 3 chiffres si plusieurs concerts le même jour (001, 002…)
- Date de jour inconnue : `YYYYMM00` (ex. `JD-CONCERT-197706000-001`)
- Date de mois inconnu : `YYYY0000` (ex. `JD-CONCERT-197700000-001`)

### Valeurs contrôlées

**alias_groupe**
- `Joy Division` — à partir de janvier 1978
- `Warsaw` — de mai 1977 à décembre 1977
- `Stiff Kittens` — 29 mai 1977 (premier concert officiel, affiche)

---

## Fichiers du registre

| Fichier | Contenu |
|---------|---------|
| `00_canonical_concerts.md` | Registre canonique complet — source joydiv.org |
| `lacunes_chronologie.md` | Concerts sans entrée dans master_chronology.md |

Les fichiers de registre source-spécifiques suivent la convention :
`concerts_<source_id>_<descripteur>.md`
(ex. `concerts_s41_hook_selected.md` pour les concerts cités par Hook)

---

## Schéma

Voir [`schemas/concert_v1.yaml`](../../schemas/concert_v1.yaml) pour
la documentation complète des champs, valeurs contrôlées et règles éditoriales.

---

## Relations avec les autres registres

- **Chronologie** : `registers/chronology/master_chronology.md` contient
  les entrées `type: concert` pour les concerts documentés par les sources
  déjà indexées. Croiser via le champ `chronologie_id`.
- **Atomes** : les sources S41 (Hook), S45 (Curtis/Deborah), S35 (Morris),
  S29 (Goddard), S84 (Cope) contiennent les mentions de concerts les plus
  nombreuses.
- **Chansons** : les setlists utilisent de préférence les identifiants
  canoniques du REGISTRY (`data/registre.json`, id `REGISTRY`).

---

## Statut

> ⏳ **En attente de données** — Le fichier `00_canonical_concerts.md` sera
> créé lors de la prochaine session avec accès réseau à `joydiv.org`
> (domaine à ajouter à l'allowlist de l'environnement).
>
> Voir `lacunes_chronologie.md` pour le suivi des manques détectés
> dans `master_chronology.md`.
