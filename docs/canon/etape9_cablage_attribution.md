# Étape 9 (suite) — Câblage des attributions de citations vers `PERSON-`

*Rattache les attributions des 962 citations aux identifiants canoniques `PERSON-`
(mergés en #47), crée additivement les `PERSON-` auteurs-sources manquants, et
route les attributions non-personnes vers l'étape 10. Tous les chiffres sont
recalculés depuis les artefacts générés (`registers/relations/attribution_edges.json`,
`exports/generated/people.json`). Aucun n'est patché à la main.*

## 0. Politiques appliquées

- **Gel additif.** Les 166 `PERSON-` de #47 ne sont NI renommés NI fusionnés.
  On AJOUTE seulement de nouveaux `PERSON-` auteurs-sources. Les id `PERS-*`
  restent intacts.
- **Conformité XR** (`docs/specs/cross_registres.md`). Les arêtes sont portées
  par l'entité **contingente** (la citation) vers le nœud `PERSON-`
  (règle de direction §3.3), au format `liens: [{predicat, cible}]` (§3.1). Deux
  prédicats sont **ajoutés additivement** au vocabulaire contrôlé (§4.3, consignés
  dans la spec avec fiches) : `a_pour_auteur_source` et `rapportee_par` ; le
  locuteur emploie le prédicat noyau `attribuee_a`.
- **SSOT.** Générateur unique et déterministe `tools/build_attribution_edges.py`
  (idempotent ; n'indexe que la couche canonique #47 pour la résolution, jamais
  ses propres `PERSON-` auteurs-sources).
- **Exécuter le clair, flagger l'ambigu.** Toute attribution non résolue et non
  clairement rattachable est marquée `a_resoudre` ; aucune fusion forcée.

## 1. Livrables

| Livrable | Chemin |
|----------|--------|
| Arêtes d'attribution typées (XR) | `registers/relations/attribution_edges.json` |
| Copie fetchée par le graphe | `exports/generated/attribution_edges.json` |
| Bloc délimité des `PERSON-` auteurs-sources créés | `registers/people/00_authors_canonical.md` |
| Hand-off `ORG-` mis à jour (non-personnes) | `registers/people/pending_org.json` |
| Générateur SSOT déterministe | `tools/build_attribution_edges.py` |
| Validateur gate-able + sentinelle | `tools/validate_attribution.py` |
| Extension du vocabulaire XR + fiches prédicats | `docs/specs/cross_registres.md` (§4.1, §4.2, §4.3) |
| Extension additive du schéma (`origine`) | `schemas/person_canonical.schema.json` |

## 2. Synthèse chiffrée

| Indicateur | Valeur |
|------------|:------:|
| Citations traitées | **962** |
| Citations couvertes (arête résolue **ou** flag explicite) | **962 / 962 = 100 %** |
| Arêtes `attribuee_a` (locuteur, 0..1) | **910** |
| dont narration d'auteur (locuteur anonyme → auteur) | 599 |
| dont locuteur nommé résolu | 311 |
| Arêtes `a_pour_auteur_source` (0..n) | **1 241** |
| Arêtes `rapportee_par` (0..n) | **31** |
| `PERSON-` auteurs-sources créés (additif) | **38** |
| Non-personnes routées → `ORG-` | **4** |
| Citations portant `a_resoudre` | 58 |
| Citations portant `attribution_non_personne` | 12 |

### Identité de comptage (vérifiée)

- **Locuteurs (962)** : 607 « anonyme » + 355 nommés.
  - 607 anonymes = **599** narration reliée à un `PERSON-` auteur + **8** dont
    l'`auteur_source` est une non-personne (institution/groupe → flag, non câblé).
    **0 orphelin** (invariant ATTR-b).
  - 355 nommés = **311** résolus (`attribuee_a`) + **44** `a_resoudre` (figures
    citées non canonicalisées).
  - Total `attribuee_a` = 599 + 311 = **910**.

## 3. Câblage des attributions résolues (XR)

Chaque citation porte une liste d'arêtes `liens` (format §3.1) :

- `locuteur` nommé → `attribuee_a` (cardinalité 0..1) vers le `PERSON-` du locuteur ;
- **narration d'auteur** (cas 5a de l'audit, locuteur « anonyme » + `auteur_source`
  présent) → `attribuee_a` vers le `PERSON-` du premier `auteur_source` ;
- `auteur_source` → `a_pour_auteur_source` (0..n ; co-auteurs éclatés) ;
- `rapporteur` → `rapportee_par` (0..n).

Les chaînes multi-auteurs sont éclatées sur `;` (séparateur fiable de co-auteurs)
puis, prudemment, sur `,` **uniquement** quand chaque fragment a ≥ 2 mots — pour
ne pas casser « Nom, Prénom » (ex. « Adorno, Theodor W. »). Les vues plates
(`attribuee_a`, `auteur_source`, `rapporteur`) sont dérivées des `liens` pour la
lecture ; les `liens` font foi.

## 4. `PERSON-` auteurs-sources créés (création additive — bloc délimité)

**38 créés**, `categorie=auteur_secondaire`, `origine=auteur_source`,
`same_as=[]` (identité née de l'attribution, sans backing `PERS-*` — autorisée
par le schéma et le validateur). Chaque création est **confirmée** comme auteur
d'une source du corpus via `data/registre.json` (vérité-terrain), ce qui écarte
les doublons d'un `PERSON-` existant sous variante. Liste :

`PERSON-aileen-dillane`, `PERSON-alastair-greig`, `PERSON-alfredo-suatoni`,
`PERSON-caterina-tomeo`, `PERSON-catherine-strong`, `PERSON-claude-flowers`,
`PERSON-dan-jacobson`, `PERSON-daniele-de-luca`, `PERSON-david-lees`,
`PERSON-david-meagher`, `PERSON-david-wilkinson`, `PERSON-eoin-devereux`,
`PERSON-gavin-butt`, `PERSON-gay-jennifer-breyley`, `PERSON-giacomo-botta`,
`PERSON-giada-iovane`, `PERSON-giovanni-maria-riccio`, `PERSON-ian-jeffrey`,
`PERSON-j-ruben-valdes-miyares`, `PERSON-jennifer-otter-bickerdike`,
`PERSON-john-s-greenwood`, `PERSON-jon-wozencroft`, `PERSON-kieran-cashell`,
`PERSON-kodwo-eshun`, `PERSON-loic-riom`, `PERSON-marco-broll`,
`PERSON-mark-johnson`, `PERSON-martin-j-power`, `PERSON-mike-west`,
`PERSON-nicholas-wood`, `PERSON-paul-tarpey`, `PERSON-robin-parmar`,
`PERSON-sara-martinez`, `PERSON-simon-frith`, `PERSON-thomson-prentice`,
`PERSON-tiffany-naiman`, `PERSON-uwe-schutte`, `PERSON-walter-cullen`.

Tous les candidats listés au §5.1 de l'audit ont été confirmés et créés (ou déjà
résolus contre un `PERSON-` existant). Les co-auteurs des chaînes composites
(`S81` Devereux/Cullen/Meagher, `S83` Greenwood/Tarpey, `S12` Wood/Prentice…)
sont créés un par un.

## 5. Attributions non-personnes → étape 10 (NON créées en `PERSON-`)

4 entités routées vers `registers/people/pending_org.json`, citations marquées
`attribution_non_personne`, câblage reporté à l'étape 10 :

| Entité | Type | Source |
|--------|------|--------|
| HM Treasury | institution | S11 |
| Happy Mondays | groupe | S14 |
| Manchester Digital Music Archive | archive/collectif | S21 |
| The Times | institution de presse | S12 |

Aucune n'est créée en `PERSON-` (invariant ATTR-c du validateur le vérifie).

## 6. Ambigus → `a_resoudre`

**44 chaînes distinctes** non résolues et non clairement rattachables, portées
par 58 citations, listées dans `attribution_edges.json` (`a_resoudre`) : figures
citées comme locuteurs mais non canonicalisées (Roland Barthes, Walter Benjamin,
Chuck Klosterman, James Anderton, R. Murray Schafer…), patronymes tronqués
(« Naiman »), ou fragments de presse. Aucune n'est forcée. Contrôle automatique :
aucune valeur `a_resoudre` ne résout en réalité contre le registre (sinon ce
serait une lacune de logique, pas une ambiguïté de donnée).

## 7. Les 9 `attribution_a_arbitrer` (audit §6) — résolues

| Citation | Résolution | Flag |
|----------|------------|:----:|
| `S76-Q020`, `S76-Q079`, `S76-Q131`, `S76-Q163`, `S76-Q169`, `S76-Q181`, `S76-Q189`, `S76-Q190` | narration *Torn Apart* → `attribuee_a` = `PERSON-mick-middles` (1er auteur) ; `a_pour_auteur_source` = Middles + Reade | levé |
| `S76-Q116` | parole rapportée : `attribuee_a` = `PERSON-ian-curtis` ; `rapportee_par` = Dave McCullough + Middles + Reade ; `a_pour_auteur_source` = Middles + Reade | levé |

`S76-Q116` portait un `rapporteur` ambigu (« entretien McCullough ») ; l'audit
tranche pour **Dave McCullough** (interview), transmis par Middles & Reade —
résolution arbitrée explicite et tracée dans le générateur (`ARBITRAGE_RAPPORTEUR`),
limitée à cette citation, jamais une heuristique large.

## 8. Validation et anti-drift

```bash
python3 tools/build_attribution_edges.py        # génère arêtes + auteurs + pending_org
python3 tools/build_registers.py --strict       # errors=0 ; 204 PERSON- (166 + 38)
python3 tools/validate_attribution.py           # ATTR-a..d + XR-1/XR-3 ; exit 0
python3 tools/validate_attribution.py --check-drift  # double build_registers + SSOT-a/b/c ; exit 0
python3 tools/validate_people.py                # registre canonique #47 ; exit 0
python3 tools/check_generated_sync.py           # sentinelle globale ; en phase
```

Invariants du validateur : **ATTR-a** couverture (arête résolue ou flag explicite
pour chaque citation) · **ATTR-b** zéro narration d'auteur non reliée (0 orphelin)
· **ATTR-c** aucune non-personne câblée en `PERSON-` · **ATTR-d** `PERSON-`
`origine=auteur_source` autorisé sans `same_as` · **XR-1** toute cible résout vers
un `PERSON-` existant · **XR-3** tout prédicat ∈ vocabulaire contrôlé.

## 9. Réponse à la revue Codex

La revue signalait que `00_authors_canonical.md` était régénéré à vide au second
passage `build_registers`, laissant **408 arêtes `[XR-1]` pendantes** dans l'état
committé. Correction à la racine, en quatre points :

1. **Register des auteurs = fonction pure de `quotes.json` (SSOT).** La
   résolution des noms n'indexe plus `exports/generated/people.json` (qui, après
   un build, contient déjà les `PERSON-` auteurs-sources créés ici — d'où la
   diffusion auto-référentielle qui vidait le register). `load_canonical_index`
   lit désormais **uniquement** la couche canonique #47 figée
   (`registers/people/00_canonical_people.md`, 166 `PERSON-`). L'ensemble des 38
   auteurs créés est donc rendu **intégralement et à l'identique** à chaque
   exécution. *Avant* : 2ᵉ passage → 0 auteur. *Après* : rerun → fichier
   byte-identique, 38 auteurs présents (idempotence stricte vérifiée).

2. **Couche de résolution non circulaire.** Le validateur reconstruit l'univers
   `PERSON-` depuis les **deux registers SSOT** — #47 `∪` register des auteurs
   (`00_authors_canonical.md`), lus directement depuis les `.md` — et ne lit
   jamais un `people.json` potentiellement périmé ou auto-référentiel.

3. **Arêtes re-résolues.** Après correction, `validate_attribution.py` retombe à
   **0 cible non résolue** (les 408 ont disparu) ; couverture 962/962.

4. **Sentinelle durcie (garde anti-récidive).** `validate_attribution.py
   --check-drift` exécute désormais `build_registers` **deux fois** (avec
   `build_attribution_edges` entre), puis vérifie : **(a)** `00_authors_canonical.md`
   byte-identique entre les deux régénérations (aucun « Total créés : 0 »
   parasite, aucun auteur supprimé) ; **(b)** les 38 `PERSON- origine=auteur_source`
   toujours présents après le 2ᵉ build (register **et** `people.json`) ; **(c)**
   `validate_attribution` = 0 cible non résolue après le 2ᵉ build. Ce double
   passage est précisément ce qui manquait. **Test de non-régression** : réinjecté
   le bug d'origine (résolution contre `people.json`), la sentinelle **échoue**
   (`exit 1`, `SSOT-a` + 408 `XR-1`) ; restaurée, elle repasse à `exit 0`.

Le générateur reste **idempotent** quel que soit l'état de `people.json`, la
résolution n'indexant que la couche #47 figée.

## 9 bis. Hors périmètre (étapes ultérieures)

- Registres `ORG-` / concept (étape 10) : seulement flaggés ici (pending_org).
- Prédicat `porte_sur` (sujet de citation), `associe_a`, maillage profond (ét. 11).

## 10. Lien de la PR

Pull request : **[https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/48](https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/48)** (branche `claude/etape9-cablage-attribution` → `main`). Revue `@codex review` déclenchée à l'ouverture. **Ne pas merger** (le merge reste gaté).
