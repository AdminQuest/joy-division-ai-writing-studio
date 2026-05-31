# Convention — catégories du registre chronologique (`categorie`)

> Étape 6 (refonte chronologie). Champ **`categorie`** porté par chaque entrée du
> registre chronologique. Vocabulaire **fermé** à cinq valeurs (la 5ᵉ,
> `concert_migre`, ajoutée à l'étape 7b-2). Additif,
> conforme au gel : la catégorie oriente le traitement (canonicalisation,
> migration, relocalisation) sans renommer ni supprimer aucune entrée.

## Vocabulaire contrôlé

| Valeur | Définition | Traitement |
|---|---|---|
| `jalon` | Événement marquant de l'histoire du groupe : formation, line-up, enregistrements, sorties, télévision/sessions fondatrices, santé, décès, concerts **premier / dernier / de transition signifiante**. | Reçoit (si réconcilié) une identité canonique `EVENT-<SLUG>` ; cœur de la chronologie. |
| `concert_a_migrer` | Concert **ordinaire** du groupe (gig de tournée sans portée de jalon), ou gig dont la seule singularité est une remarque accolée. | Conservé, ID legacy gardé, **non** promu en `EVENT-`. Migrera vers le registre `CONCERT-` (étape 7b), où la date redevient un attribut. |
| `concert_migre` | Concert ordinaire **déjà réconcilié** vers le registre concerts (étape 7b-2) : l'entrée porte un `same_as` vers son identité `CONCERT-<SLUG>`. | Conservé pour traçabilité, **hors chronologie active**. Le `same_as` (vers un `CONCERT-`, jamais un `EVENT-`) **est** la migration. Invariant : `concert_migre` ⇒ `same_as` vers un `CONCERT-` (validate_chronology INV5). |
| `reception_posthume` | Réception, lecture critique, archive ou résonance **postérieure** à l'ère 1976-1980 (ou portée par une source interprétative : S29, S34). | Conservé, étiqueté. Relocalisation différée (étape 11, concepts / réception). |
| `contexte` | Repère **contextuel** urbain, social ou historique qui n'est ni un événement du groupe, ni un concert, ni de la réception posthume (registres S02, S05, S06, S12, S20 : ville en contraction, ordre public, logement, etc.). | Conservé, étiqueté. **Exclu** de la canonicalisation `EVENT-`. Relocalisation différée (étape 11, registre concepts / contexte). |

## Tags de migration (métadonnées, étape 7b)

- **`a_resoudre: true`** — porté par un `concert_a_migrer` résiduel : vrai gig JD
  dont la date est trop imprécise (mois/année) ou ambiguë (plusieurs `CONCERT-`
  candidats) pour une réconciliation confiante. Reste `concert_a_migrer` jusqu'à
  résolution manuelle. Invariant : ne se pose que sur `concert_a_migrer`.
- **`liaison_multi_concert: true`** — porté par un `jalon` qui résume **plusieurs**
  concerts (résidence multi-soirs, ou plusieurs gigs dans une seule entrée) : la
  liaison vers les `CONCERT-` correspondants est différée à l'étape 12
  (cross-registres). Pas de `same_as` unique (ce serait une fusion abusive).

## Règles d'application

1. **Exclusivité** : une entrée porte exactement une `categorie`.
2. **Frontière jalon / concert** : un concert n'est `jalon` que s'il marque une
   transition de signification réelle (premier concert, dernier concert,
   premier sous un nom, première télévision…). La simple proximité ordinale
   (« avant-dernier », « troisième ») **ne suffit pas** → `concert_a_migrer`.
3. **Entrées bundlées** (un gig **et** un fait distinct porteur de sens — crise,
   accident, session, début de management) : classées selon le fait dominant et
   **signalées pour scission** au moment de la création du registre `CONCERT-`
   (étape 10). La scission n'est pas faite en étape 6.
4. **Coïncidence de date ≠ identité** : deux entrées à la même date ne sont
   réconciliées (`same_as`) que si elles désignent le **même** événement.
5. `contexte` et `reception_posthume` ne reçoivent **jamais** d'`EVENT-`.

## Filiation

Cette convention prolonge la spécification cross-registres
(`docs/specs/cross_registres.md`) et la doctrine de slugification
(`docs/NAMING_CONVENTIONS.md` §10). Le diagnostic et l'historique des
reclassements sont consignés dans
`docs/audits/audit_unitaire_chronologie_12b-3.md` (annexe).
