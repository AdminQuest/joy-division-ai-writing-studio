# Registre des sessions studio — Joy Division / Warsaw

## Fonction du registre

Ce registre centralise les 17 sessions canoniques d'enregistrement de
Joy Division (et Warsaw) : sessions studio, démos, Peel sessions, sessions
radio, et la session Still de 1981 (post-mortem).

Il sert à :
- stabiliser les dates, studios et producteurs ;
- documenter la généalogie des prises (Transmission 1 vs 2, LWTUA 1 vs 2) ;
- relier sessions, titres enregistrés, premières sorties officielles ;
- préparer les exports CSV/JSON (`exports/generated/sessions.{json,csv}`)
  et alimenter le moteur RAG ;
- identifier les lacunes dans le registre chronologique maître.

---

## Source canonique primaire

| Champ | Valeur |
|-------|--------|
| ID source | `REGISTRY-SESSIONS` |
| URL | https://joydiv.org/sessions.htm |
| Auteur | Tony Nuttall |
| Statut | `reference_externe` |
| Fiabilité | `haute` |
| Date consultation | 27 mai 2026 |

---

## Structure normalisée d'une entrée

```yaml
- id: JD-SESSION-YYYYMMDD-NNN
  numero: 1                # rang dans la chronologie canonique (1 à 17)
  label: "Warsaw demo"
  date: YYYY-MM-DD
  studio: "Pennine Sound Studios"
  ville: "Oldham"
  producteur: "Inconnu"    # ou "Martin Hannett", etc.
  ere: "Warsaw"            # Warsaw | Joy Division
  titres: []               # titres enregistrés
  premiere_sortie_officielle:
    titre: ""
    format: "album"        # album | single | EP | compilation | BBC release | inédit
    label: ""
    annee: ""
  source: joydiv.org
  atomes_lies: []
  chronologie_id: ""       # CHR-XXXX-XXX si lié à master_chronology
  # optionnels :
  ingenieur_son: "Jon Caffery"
  statut_session: officiel
  notes: ""
```

### Conventions d'identifiant

- Format : `JD-SESSION-YYYYMMDD-NNN`
- Pour les sessions au mois seulement : `YYYYMM00` (ex. `JD-SESSION-19771200-001`)
- Pour les sessions à date entièrement inconnue : `YYYY0000`

---

## Fichiers du registre

| Fichier | Contenu |
|---------|---------|
| `00_canonical_sessions.md` | Registre canonique complet (joydiv.org) — 17 sessions |
| `lacunes_chronologie.md` | À créer : sessions sans entrée dans master_chronology.md |

Les fichiers de registre source-spécifiques suivent la convention :
`sessions_<source_id>_<descripteur>.md`
(ex. `sessions_s41_hook_peel.md` pour les sessions citées par Hook)

---

## Schéma

Voir [`schemas/session_v1.yaml`](../../schemas/session_v1.yaml) pour la
documentation complète des champs et règles.

---

## Relations avec les autres registres

- **Chronologie** : `registers/chronology/master_chronology.md` contient
  l'entrée CHR-1978-001 pour les sessions RCA/Arrow (= session 3 du
  registre canonique). À enrichir progressivement.
- **Atomes** : S41 (Hook), S83 (Hannett — architecture sonore), S45 (Curtis),
  S35 (Morris), S84 (Cope) contiennent les mentions de sessions les plus
  riches.
- **Chansons** : les titres enregistrés utilisent de préférence les
  identifiants canoniques du REGISTRY (`data/registre.json`).
