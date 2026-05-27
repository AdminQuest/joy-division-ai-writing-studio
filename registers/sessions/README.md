# Registre des sessions et répétitions — Joy Division / Warsaw

## Fonction du registre

Ce registre centralise l'ensemble des sessions studio, répétitions,
Peel sessions, enregistrements radio et TV de Joy Division
(et Warsaw / Stiff Kittens) dans leur chronologie documentée.

Il sert à :
- stabiliser les dates et lieux d'enregistrement ;
- distinguer les sessions officiellement publiées des inédits et bootlegs ;
- relier sessions, titres enregistrés, producteurs et atomes documentaires ;
- préparer les exports CSV/JSON et alimenter le moteur RAG ;
- identifier les lacunes dans le registre chronologique maître.

Le registre ne doit pas devenir une discographie analytique ou un journal
de studio narratif. Il reste factuel, traçable, relationnel.

---

## Source canonique primaire

| Champ | Valeur |
|-------|--------|
| ID source | `REGISTRY-SESSIONS` |
| URL | https://joydiv.org/sessrehears.htm |
| Auteur | Tony Nuttall |
| Statut | `reference_externe` |
| Fiabilité | `haute` |
| Consultation | en attente (accès réseau limité dans l'environnement) |

---

## Structure normalisée d'une entrée

```yaml
id: JD-SESSION-YYYYMMDD-001
date: YYYY-MM-DD
date_display: "jour mois année"
type: studio        # studio / repetition / peel / radio / tv / demo / soundcheck
lieu: "Studio ou salle"
ville: "Ville"
titres_enregistres: []
statut: officiel    # officiel / inedit / bootleg / perdu / partiel
sources: [REGISTRY-SESSIONS]
atomes_lies: []
chronologie_id: ""  # CHR-XXXX-XXX si entrée dans master_chronology
notes: ""
```

### Conventions d'identifiant

- Format : `JD-SESSION-YYYYMMDD-NNN`
- NNN = index sur 3 chiffres si plusieurs sessions le même jour (001, 002…)
- Date de jour inconnue : `YYYYMM00` (ex. `JD-SESSION-197706000-001`)
- Date de mois inconnu : `YYYY0000` (ex. `JD-SESSION-197700000-001`)

### Valeurs contrôlées

**type**
| Valeur | Usage |
|--------|-------|
| `studio` | Session d'enregistrement en studio (demo, album, single) |
| `repetition` | Répétition sans intention discographique |
| `peel` | BBC Peel Session (Maida Vale ou similaire) |
| `radio` | Autre émission radio (Granada, BBC autre que Peel…) |
| `tv` | Émission ou captation télévisée |
| `demo` | Démo autonome, home-recording ou location informelle |
| `soundcheck` | Balance avant concert, enregistrée par accident ou bootleg |

**statut**
| Valeur | Usage |
|--------|-------|
| `officiel` | Publié sur album, single, compilation ou archive BBC officielle |
| `inedit` | Jamais publié, mais existence documentée |
| `bootleg` | Circulant uniquement en version non officielle |
| `perdu` | Existence documentée, aucun enregistrement connu subsistant |
| `partiel` | Partiellement publié, partiellement perdu ou inédit |

---

## Fichiers du registre

| Fichier | Contenu |
|---------|---------|
| `00_canonical_sessions.md` | Registre canonique complet — source joydiv.org |
| `lacunes_chronologie.md` | Sessions sans entrée dans master_chronology.md |

Les fichiers de registre source-spécifiques suivent la convention :
`sessions_<source_id>_<descripteur>.md`
(ex. `sessions_s41_hook_peel.md` pour les sessions citées par Hook)

---

## Schéma

Voir [`schemas/session_v1.yaml`](../../schemas/session_v1.yaml) pour
la documentation complète des champs, valeurs contrôlées et règles éditoriales.

---

## Relations avec les autres registres

- **Chronologie** : `registers/chronology/master_chronology.md` contient
  les entrées `type: enregistrement` pour les sessions documentées par
  les sources déjà indexées (notamment CHR-1978-001 — Sessions RCA/Arrow).
  Croiser via le champ `chronologie_id`.
- **Atomes** : les sources S41 (Hook), S83 (Hannett, architecture sonore),
  S45 (Curtis/Deborah), S35 (Morris), S84 (Cope) contiennent les mentions
  de sessions les plus nombreuses.
- **Concerts** : certains soundchecks documentés dans le registre concerts
  peuvent correspondre à une entrée session de type `soundcheck`.

---

## Statut

> ⏳ **En attente de données** — Le fichier `00_canonical_sessions.md` sera
> créé lors de la prochaine session avec accès réseau à `joydiv.org`
> (domaine à ajouter à l'allowlist de l'environnement).
>
> Voir `lacunes_chronologie.md` pour le suivi des manques détectés
> dans `master_chronology.md`.
