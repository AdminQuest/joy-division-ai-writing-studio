# Controle M1 - DM vers registres

## Objet

Rapport genere par `python3 tools/check_dm_registers_consistency.py`.

Ce controle est strictement en lecture sur les documents maitres, registres, exports et manifeste. Il produit des constats et ne corrige aucun ecart.

## Périmètre

Perimetre MVP couvert : personnes, chansons, chronologie, citations, concerts et sessions.

Le controle verifie les identifiants de registres explicitement visibles dans `chapters/*/document_maitre.md`, leur presence dans les exports P0 disponibles, et les principales volumetries exposees par `exports/generated/master_docs_index.json`.

Hors perimetre MVP : registres P1, relations transversales completes, sources, exports hors registres P0, tracabilite passage par passage, correction des registres ou des documents maitres.

## Résumé global

| Indicateur | Valeur |
|------------|---------|
| Documents declares dans le manifeste | 14 |
| Documents maîtres sur disque | 14 |
| Documents cohérents | 1 |
| Documents partiellement cohérents | 13 |
| Documents non cohérents | 0 |
| Écarts détectés | 81 |
| Identifiants introuvables | 1 |
| Registres absents | 0 |
| Compteurs incohérents | 0 |
| Familles non couvertes | 51 |
| Relations non résolues | 0 |
| Libellés divergents | 29 |
| Manifestes incohérents | 0 |
| people visibles / retrouvés | 477 / 477 |
| songs visibles / retrouvés | 235 / 236 |
| chronology visibles / retrouvés | 413 / 413 |
| quotes visibles / retrouvés | 511 / 511 |
| concerts visibles / retrouvés | 0 / 0 |
| sessions visibles / retrouvés | 0 / 0 |

## Audit par document maître

| DM | Statut | Registres P0 retrouvés | Écarts MVP | Familles hors MVP |
|----|--------|------------------------|------------|-------------------|
| `chapters/01/document_maitre.md` | partiellement cohérent | people: 24/24, songs: 1/2, chronology: 15/15, quotes: 38/38, concerts: 0/0, sessions: 0/0 | identifiant introuvable: 1, libellé divergent: 2 | concepts: 12, motifs: 3, myths: 3, relations: 10 |
| `chapters/02/document_maitre.md` | partiellement cohérent | people: 34/34, songs: 10/10, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 2 | concepts: 5, motifs: 2, myths: 6, relations: 2 |
| `chapters/03/document_maitre.md` | partiellement cohérent | people: 33/33, songs: 26/26, chronology: 25/25, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 3 | concepts: 12, myths: 6, relations: 4 |
| `chapters/04/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 34/34, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 1 | concepts: 5, myths: 5, relations: 2 |
| `chapters/05/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 7/7, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 5 | concepts: 4, motifs: 4, myths: 7, relations: 1 |
| `chapters/06/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 28/28, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 2 | concepts: 5, motifs: 1, myths: 4 |
| `chapters/07/document_maitre.md` | partiellement cohérent | people: 23/23, songs: 17/17, chronology: 17/17, quotes: 20/20, concerts: 0/0, sessions: 0/0 | libellé divergent: 2 | concepts: 6, motifs: 1, myths: 8, relations: 5 |
| `chapters/08/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 11/11, chronology: 36/36, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 2 | concepts: 22, motifs: 2, myths: 5, relations: 1 |
| `chapters/09/document_maitre.md` | partiellement cohérent | people: 14/14, songs: 3/3, chronology: 3/3, quotes: 13/13, concerts: 0/0, sessions: 0/0 | libellé divergent: 2 | concepts: 6, motifs: 1, myths: 2, relations: 1 |
| `chapters/10/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 11/11, chronology: 29/29, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 1 | concepts: 16, motifs: 7, myths: 4, relations: 2 |
| `chapters/11/document_maitre.md` | partiellement cohérent | people: 29/29, songs: 29/29, chronology: 17/17, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 1 | concepts: 3, motifs: 2, myths: 4, relations: 13 |
| `chapters/12/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 17/17, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 1 | concepts: 11, motifs: 1, myths: 5 |
| `chapters/13/document_maitre.md` | cohérent | people: 40/40, songs: 13/13, chronology: 31/31, quotes: 40/40, concerts: 0/0, sessions: 0/0 | Aucun écart MVP | concepts: 11, myths: 7, organizations: 1, relations: 6 |
| `chapters/14/document_maitre.md` | partiellement cohérent | people: 40/40, songs: 28/28, chronology: 40/40, quotes: 40/40, concerts: 0/0, sessions: 0/0 | libellé divergent: 5 | concepts: 7, myths: 6, relations: 12 |

## Écarts détectés

- **libellé divergent** — famille `people` — `chapters/01/document_maitre.md` : PERS-S85-001: libelle visible `ACTEURS` ; libelle exporte `Colin Malcolm`.
- **libellé divergent** — famille `people` — `chapters/01/document_maitre.md` : PERS-S85-006: libelle visible `ACTEURS` ; libelle exporte `Lou Stoppard / Adam Murray`.
- **identifiant introuvable** — famille `songs` — `chapters/01/document_maitre.md` : SONG-S45-SHADOWPLAY-RCA est visible dans le DM mais absent de exports/generated/songs.json.
- **famille non couverte** — famille `concepts` — `chapters/01/document_maitre.md` : 12 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/01/document_maitre.md` : 3 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/01/document_maitre.md` : 3 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/01/document_maitre.md` : 10 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/02/document_maitre.md` : PERS-004: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **libellé divergent** — famille `people` — `chapters/02/document_maitre.md` : PERS-004-S75: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **famille non couverte** — famille `concepts` — `chapters/02/document_maitre.md` : 5 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/02/document_maitre.md` : 2 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/02/document_maitre.md` : 6 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/02/document_maitre.md` : 2 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/03/document_maitre.md` : PERS-004: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **libellé divergent** — famille `people` — `chapters/03/document_maitre.md` : PERS-004-S75: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **libellé divergent** — famille `people` — `chapters/03/document_maitre.md` : PERS-008: libelle visible `James Martin Hannett` ; libelle exporte `Martin Hannett`.
- **famille non couverte** — famille `concepts` — `chapters/03/document_maitre.md` : 12 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/03/document_maitre.md` : 6 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/03/document_maitre.md` : 4 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/04/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **famille non couverte** — famille `concepts` — `chapters/04/document_maitre.md` : 5 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/04/document_maitre.md` : 5 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/04/document_maitre.md` : 2 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/05/document_maitre.md` : PERS-004: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **libellé divergent** — famille `people` — `chapters/05/document_maitre.md` : PERS-006: libelle visible `Robert Leo Gretton` ; libelle exporte `Rob Gretton`.
- **libellé divergent** — famille `people` — `chapters/05/document_maitre.md` : PERS-007: libelle visible `Anthony Howard Wilson` ; libelle exporte `Tony Wilson`.
- **libellé divergent** — famille `people` — `chapters/05/document_maitre.md` : PERS-008: libelle visible `James Martin Hannett` ; libelle exporte `Martin Hannett`.
- **libellé divergent** — famille `people` — `chapters/05/document_maitre.md` : PERS-009: libelle visible `Peter Andrew Saville` ; libelle exporte `Peter Saville`.
- **famille non couverte** — famille `concepts` — `chapters/05/document_maitre.md` : 4 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/05/document_maitre.md` : 4 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/05/document_maitre.md` : 7 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/05/document_maitre.md` : 1 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/06/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **libellé divergent** — famille `people` — `chapters/06/document_maitre.md` : PERS-008: libelle visible `James Martin Hannett` ; libelle exporte `Martin Hannett`.
- **famille non couverte** — famille `concepts` — `chapters/06/document_maitre.md` : 5 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/06/document_maitre.md` : 1 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/06/document_maitre.md` : 4 identifiant(s) visibles pour la famille `myths` hors MVP.
- **libellé divergent** — famille `people` — `chapters/07/document_maitre.md` : PERS-004: libelle visible `Stephen Paul David Morris` ; libelle exporte `Stephen Morris`.
- **libellé divergent** — famille `people` — `chapters/07/document_maitre.md` : PERS-008: libelle visible `James Martin Hannett` ; libelle exporte `Martin Hannett`.
- **famille non couverte** — famille `concepts` — `chapters/07/document_maitre.md` : 6 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/07/document_maitre.md` : 1 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/07/document_maitre.md` : 8 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/07/document_maitre.md` : 5 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/08/document_maitre.md` : PERS-S85-003: libelle visible `ACTEURS` ; libelle exporte `Tom Hingley`.
- **libellé divergent** — famille `people` — `chapters/08/document_maitre.md` : PERS-S85-004: libelle visible `ACTEURS` ; libelle exporte `David Haslam`.
- **famille non couverte** — famille `concepts` — `chapters/08/document_maitre.md` : 22 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/08/document_maitre.md` : 2 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/08/document_maitre.md` : 5 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/08/document_maitre.md` : 1 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/09/document_maitre.md` : PERS-006: libelle visible `Robert Leo Gretton` ; libelle exporte `Rob Gretton`.
- **libellé divergent** — famille `people` — `chapters/09/document_maitre.md` : PERS-007: libelle visible `Anthony Howard Wilson` ; libelle exporte `Tony Wilson`.
- **famille non couverte** — famille `concepts` — `chapters/09/document_maitre.md` : 6 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/09/document_maitre.md` : 1 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/09/document_maitre.md` : 2 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/09/document_maitre.md` : 1 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/10/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **famille non couverte** — famille `concepts` — `chapters/10/document_maitre.md` : 16 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/10/document_maitre.md` : 7 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/10/document_maitre.md` : 4 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/10/document_maitre.md` : 2 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/11/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **famille non couverte** — famille `concepts` — `chapters/11/document_maitre.md` : 3 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/11/document_maitre.md` : 2 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/11/document_maitre.md` : 4 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/11/document_maitre.md` : 13 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/12/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **famille non couverte** — famille `concepts` — `chapters/12/document_maitre.md` : 11 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `motifs` — `chapters/12/document_maitre.md` : 1 identifiant(s) visibles pour la famille `motifs` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/12/document_maitre.md` : 5 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `concepts` — `chapters/13/document_maitre.md` : 11 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/13/document_maitre.md` : 7 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `organizations` — `chapters/13/document_maitre.md` : 1 identifiant(s) visibles pour la famille `organizations` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/13/document_maitre.md` : 6 identifiant(s) visibles pour la famille `relations` hors MVP.
- **libellé divergent** — famille `people` — `chapters/14/document_maitre.md` : PERS-001: libelle visible `Ian Kevin Curtis` ; libelle exporte `Ian Curtis`.
- **libellé divergent** — famille `people` — `chapters/14/document_maitre.md` : PERS-006: libelle visible `Robert Leo Gretton` ; libelle exporte `Rob Gretton`.
- **libellé divergent** — famille `people` — `chapters/14/document_maitre.md` : PERS-007: libelle visible `Anthony Howard Wilson` ; libelle exporte `Tony Wilson`.
- **libellé divergent** — famille `people` — `chapters/14/document_maitre.md` : PERS-008: libelle visible `James Martin Hannett` ; libelle exporte `Martin Hannett`.
- **libellé divergent** — famille `people` — `chapters/14/document_maitre.md` : PERS-009: libelle visible `Peter Andrew Saville` ; libelle exporte `Peter Saville`.
- **famille non couverte** — famille `concepts` — `chapters/14/document_maitre.md` : 7 identifiant(s) visibles pour la famille `concepts` hors MVP.
- **famille non couverte** — famille `myths` — `chapters/14/document_maitre.md` : 6 identifiant(s) visibles pour la famille `myths` hors MVP.
- **famille non couverte** — famille `relations` — `chapters/14/document_maitre.md` : 12 identifiant(s) visibles pour la famille `relations` hors MVP.

## Limites observées

- Le controle ne couvre que les familles P0 : personnes, chansons, chronologie, citations, concerts et sessions.
- Les familles P1 visibles, comme concepts, motifs, mythes, lieux, organisations et relations, sont signalees comme hors MVP et ne sont pas resolues.
- Les relations transversales ne sont pas controlees dans cette version.
- La comparaison de libelles reste volontairement prudente et ne s'applique que lorsque le libelle visible et le libelle exporte sont objectivement disponibles.
- Le controle ne verifie pas la tracabilite passage par passage.
- Une volumetrie coherente ne prouve pas la coherence fine de tous les passages redactionnels.

## Faux positifs possibles

- Un libelle abrege ou typographiquement adapte dans un document maitre peut differer du libelle exporte sans signaler une erreur documentaire.
- Une famille hors MVP peut etre volontairement visible dans un document maitre sans etre controlee par cette premiere version.
- Un identifiant absent d'un export P0 peut relever d'un registre specialise non encore consolide plutot que d'une erreur du document maitre.
- Les compteurs peuvent rester coherents alors que certains objets visibles sont des selections redactionnelles.

## Conclusion

Le controle DM -> registres est partiellement concluant dans le perimetre MVP : des ecarts doivent etre relus avant toute correction separee.

Ce rapport ne vaut pas validation des registres P1, des sources, des exports complets ou de la coherence passage par passage.
