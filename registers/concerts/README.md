# Registre des concerts — Joy Division / Warsaw

## Fonction du registre

Ce registre centralise l'ensemble des concerts et gigs de Joy Division
(et Warsaw / Stiff Kittens) dans leur chronologie documentée, ainsi que
les concerts annulés et les captations TV en public.

Il sert à :
- stabiliser les dates et lieux de concerts ;
- distinguer concerts confirmés, annulés, douteux et passages TV ;
- relier concerts, atomes documentaires, chronologie maître et chansons ;
- préparer les exports CSV/JSON (`exports/generated/concerts.{json,csv}`)
  et alimenter le moteur RAG ;
- identifier les lacunes dans le registre chronologique maître.

---

## Source canonique primaire

| Champ | Valeur |
|-------|--------|
| ID source | `REGISTRY-CONCERTS` |
| URL | https://joydiv.org/concerts.htm |
| Auteur | Tony Nuttall |
| Statut | `reference_externe` |
| Fiabilité | `haute` |
| Date consultation | 27 mai 2026 |

---

## Structure normalisée d'une entrée

```yaml
- id: JD-CONCERT-YYYYMMDD-NNN
  date: YYYY-MM-DD
  statut: confirme        # confirme | annule | reporte | douteux | tv
  lieu: "Nom de la salle"
  ville: "Ville"
  pays: "UK"              # UK | FRANCE | BELGIQUE | PAYS-BAS | ALLEMAGNE | USA | CANADA | IRLANDE
  ere: "Joy Division"     # Warsaw | Stiff Kittens | Joy Division
  source: joydiv.org
  url_detail: "https://joydiv.org/cDDMMYY.htm"  # optionnel
  atomes_lies: []
  chronologie_id: ""      # CHR-XXXX-XXX si lié à master_chronology
  notes: ""
  # optionnels :
  nom_tournee: "Buzzcocks tour"
  setlist: []
```

### Conventions d'identifiant

- Format : `JD-CONCERT-YYYYMMDD-NNN`
- NNN = index (001, 002…) si plusieurs concerts le même jour
- Pour les concerts annulés, utiliser le suffixe `-A01` (au lieu de `-001`)
  afin de les distinguer d'un éventuel concert confirmé le même jour
- Date du jour inconnue : `YYYYMM00` dans l'id et `YYYY-MM-00` dans `date`

---

## Fichiers du registre

| Fichier | Contenu |
|---------|---------|
| `00_canonical_concerts.md` | Registre canonique complet (joydiv.org) |
| `lacunes_chronologie.md` | À créer : concerts sans entrée dans master_chronology.md |

Les fichiers de registre source-spécifiques suivent la convention :
`concerts_<source_id>_<descripteur>.md`
(ex. `concerts_s41_hook_selected.md` pour les concerts cités par Hook)

---

## Schéma

Voir [`schemas/concert_v1.yaml`](../../schemas/concert_v1.yaml) pour la
documentation complète des champs, valeurs contrôlées et règles éditoriales.

---

## Relations avec les autres registres

- **Chronologie** : `registers/chronology/master_chronology.md` contient
  les entrées `type: concert` pour les concerts déjà indexés (notamment
  CHR-1980-001 — Bury 8 avril 1980). Croiser via `chronologie_id`.
- **Atomes** : S41 (Hook), S45 (Curtis), S35 (Morris), S29 (Goddard),
  S84 (Cope) contiennent les mentions de concerts les plus nombreuses
  — à enrichir progressivement dans `atomes_lies`.
- **Chansons** : les setlists utilisent de préférence les identifiants
  canoniques du REGISTRY (`data/registre.json`, id `REGISTRY`).
