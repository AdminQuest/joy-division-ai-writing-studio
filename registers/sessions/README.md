# Registre des sessions / répétitions — Joy Division / Warsaw

## Fonction du registre

Ce registre centralise les sessions et répétitions documentées de Joy Division
(et Warsaw) : répétitions, démos, sessions studio, sessions radio, sessions
télévisées et lieux de travail musical.

Il sert à :
- stabiliser les dates, studios et producteurs ;
- documenter les lieux de travail sonore et de répétition ;
- documenter la généalogie des prises (Transmission 1 vs 2, LWTUA 1 vs 2) ;
- relier sessions, titres travaillés, premières sorties officielles, personnes
  et lieux ;
- préparer les exports CSV/JSON (`exports/generated/sessions.{json,csv}`)
  et alimenter le moteur RAG ;
- identifier les lacunes dans le registre chronologique maître.

---

## Source canonique primaire

| Champ | Valeur |
|-------|--------|
| ID source | `REGISTRY-SESSIONS` |
| URL | https://joydiv.org/sessions.htm ; https://joydiv.org/rehearsals.htm ; https://joydiv.org/jdtv.htm |
| Auteur | Tony Nuttall |
| Statut | `reference_externe` |
| Fiabilité | `haute` |
| Date consultation | 4 juin 2026 |

---

## Structure normalisée d'une entrée

```yaml
- id: JD-SESSION-YYYYMMDD-NNN
  numero: 1                # rang dans la chronologie canonique
  label: "Warsaw demo"
  date: YYYY-MM-DD
  type_session: demo       # rehearsal | demo | studio | radio | television
  studio: "Pennine Sound Studios"
  lieu: "Pennine Sound Studios"
  place_id: "PLACE-PENNINE-STUDIOS-OLDHAM"
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
  sources: []
  urls: []
  statut_documentaire: etabli # etabli | probable | conteste
  atomes_lies: []
  chronologie_id: ""       # CHR-XXXX-XXX si lié à master_chronology
  relations: {}
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
| `joy_division_sessions_register_v1.md` | Registre actif C3A-9 — 26 sessions / répétitions |
| `00_canonical_sessions.md` | Note legacy ; ne contient plus de records pour éviter les doublons |
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

- **Chronologie** : plusieurs événements canoniques existent déjà pour RCA,
  Granada, Peel, Piccadilly, T.J. Davidson's, Unknown Pleasures, Transmission,
  Closer et Love Will Tear Us Apart.
- **Atomes** : S41 (Hook), S83 (Hannett — architecture sonore), S45 (Curtis),
  S35 (Morris), S84 (Cope) contiennent les mentions de sessions les plus
  riches.
- **Chansons** : les titres enregistrés utilisent de préférence les
  identifiants canoniques du REGISTRY (`data/registre.json`).
