# Rapport d’intégration — S42 — Amendola & Troianiello

```yaml
source_id: S42
date_integration: "2026-05-17"
workflow: "passe complète atomisation v2"
passage_atomise: "Article complet : « Metropoli e spazio periferico nell’underground post-punk inglese », dans Our Vision Touched the Sky, p. 41-53 de l’exemplaire PDF."
```

## 1. Atomes v2 créés

- S42-A001 — S42 comme article spatial et sociologique, non comme source primaire
- S42-A002 — « Shadowplay » comme seuil spatial
- S42-A003 — Centre / périphérie : post-punk depuis les marges industrielles
- S42-A004 — Le post-punk produit des identités sociales autant qu’il les reflète
- S42-A005 — Nostalgie, industrie du rétro et réemploi contemporain du post-punk
- S42-A006 — Punk contre post-punk : destruction, reconstruction et expérimentation
- S42-A007 — Manchester, Liverpool, Sheffield : triangulation périphérique
- S42-A008 — Focal places : clubs, disquaires, salles de répétition et réseaux
- S42-A009 — Electric Circus : matrice punk et héritage post-punk mancunien
- S42-A010 — Factory Records comme focal place esthétique et institutionnel
- S42-A011 — Manchester post-industrielle : grise périphérie, médicaments, littérature et dégoût culturel
- S42-A012 — Liverpool et Sheffield : rhizome post-punk, Eric’s, Meatwhistle et Cabaret Voltaire
- S42-A013 — De la sous-culture au mainstream : réification et circulation globale du post-punk

## 2. Relations stabilisées créées

- REL-S42-001 — Statut documentaire
- REL-S42-002 — « Shadowplay » comme opérateur spatial
- REL-S42-003 — Centre/périphérie comme dynamique de circulation
- REL-S42-004 — Anti-déterminisme
- REL-S42-005 — Nostalgie contemporaine et industrie du rétro
- REL-S42-006 — Punk / post-punk : rupture puis reconstruction
- REL-S42-007 — Triangulation Manchester / Liverpool / Sheffield
- REL-S42-008 — Focal places comme lieux-réseaux
- REL-S42-009 — Manchester post-industrielle comme atmosphère sociale
- REL-S42-010 — Sous-culture réifiée

## 3. Registres enrichis

- concepts : centre/périphérie post-punk ; focal places ; musique comme production d’identité ; sous-culture réifiée ;
- motifs : ville-seuil ; périphérie industrielle du Nord ; lieux-réseaux ; rétro post-punk ;
- mythes : déterminisme mancunien ; réduction de tout le post-punk à Joy Division ; trahison automatique par le mainstream ;
- références : S42 maintenu comme article, non comme volume complet ;
- spécialisés : citations minimales, chronologie courte, acteurs, lieux, organisations, chansons.

## 4. Mise à jour documents maîtres / RAG

La mise à jour documentaire est décrite dans :

```text
sources/amendola_troianiello_metropoli_spazio_periferico/dm_rag_update_s42_metropoli_spazio_periferico.md
```

## 5. Contrôles recommandés

```bash
grep -R "S42-A001" -n sources registers chapters exports | head -20
grep -R "REL-S42-001" -n sources registers chapters exports | head -20
grep -R "focal places" -n sources registers chapters exports | head -20
grep -R "centre/périphérie" -n sources registers chapters exports | head -20
grep -R "Electric Circus" -n sources registers chapters exports | head -20
grep -R "Meatwhistle" -n sources registers chapters exports | head -20
```
