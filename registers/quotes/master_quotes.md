# Registre consolidé des citations

Ce registre consolide les citations issues des anciens fichiers de travail et des atomisations. Aucune citation n’est canonique par sa seule origine. Les statuts restent opératoires :

```text
candidate               citation utile mais non encore promue pour insertion définitive
verified_candidate      citation historiquement contrôlée mais à replacer dans son contexte avant emploi
reference_or_concept    titre, notion, paraphrase ou concept ; ne pas traiter comme citation directe
rejected                citation écartée, remplacée ou non fiable
```

---

# 1. Import des citations historiques

```yaml
id: HIST-C1-IMPORT-001
lot: citations_historiques_chapitre_1
source_file: 00_Citations.xlsx
source_origin:
  - registre historique
  - fichier de travail utilisateur
sheet: Chapitre 1 - Citations
range: A1:L71
rows_imported: 70
chapitres:
  - Chapitre 1
statut_consolidation: imported_batch
arbitrage: >
  Les 70 lignes du fichier historique 00_Citations.xlsx sont importées comme lot de consolidation.
  Elles ne sont pas automatiquement supérieures aux citations atomisées. Les entrées marquées
  comme concepts, titres, paraphrases ou formulations analytiques doivent rester hors citation
  directe. Les identifiants historiques S20, S35 et S37 sont à lire comme legacy_id pointant
  respectivement vers S72, S41 et S45.
```

## 1.1. Index des entrées historiques importées

| ID consolidé | Source historique | Type | Entrée | Statut |
|---|---|---|---|---|
| HIST-C1-001 | S10 | verbatim | « L'endroit où je vivais, où j'avais mes souvenirs les plus heureux... eh bien, cet endroit n'existait plus. » | verified_candidate |
| HIST-C1-002 | à attribuer | paraphrase issue d’un témoignage | « plateau de tournage abandonné » | candidate |
| HIST-C1-003 | à attribuer | paraphrase issue d’un témoignage | « bombardé de bombes à neutrons » | candidate |
| HIST-C1-004 | S10 | verbatim | « fumer 70 cigarettes par jour » | verified_candidate |
| HIST-C1-005 | S11 | terme analytique | « remède Thatcher » | reference_or_concept |
| HIST-C1-006 | S12 | surnom médiatique | « Flic de Dieu » | reference_or_concept |
| HIST-C1-007 | S14 | titre de chanson | « God's Cop » | reference_or_concept |
| HIST-C1-008 | S16 | titre de chanson | « Boredom » | reference_or_concept |
| HIST-C1-009 | S17 | titre de chanson | « Rowche Rumble » | reference_or_concept |
| HIST-C1-010 | S10 | verbatim | « L'expérience que j'ai eue de la classe ouvrière, c'était sa disparition » | verified_candidate |
| HIST-C1-011 | S18 | paraphrase attribuée | « la réponse d'une génération délaissée et désabusée » | candidate |
| HIST-C1-012 | S19 | concept | « reconversion du capital » | reference_or_concept |
| HIST-C1-013 | à attribuer | mot d’argot cité | « khazi » | candidate |
| HIST-C1-014 | à attribuer | formule attribuée ou paraphrase | « Le Factory ne s'intéresse pas au style de vie, il s'intéresse à la qualité de... » | candidate |
| HIST-C1-015 | S28 | titre d’œuvre | « So It Goes » | reference_or_concept |
| HIST-C1-016 | à attribuer | formulation d’auteur / paraphrase | « son Manchester » | reference_or_concept |
| HIST-C1-017 | à attribuer | intitulé de rubrique | « Pam ponders » | candidate |
| HIST-C1-018 | S21 | citation courte à attribuer | « minimalisme branché » | candidate |
| HIST-C1-019 | S25 | terme de qualification | « honnête » | candidate |
| HIST-C1-020 | S21 | terme critique | « bourgeois » | verified_candidate |
| HIST-C1-021 | S21 | catégorie discursive | « nouvelle pop » | verified_candidate |
| HIST-C1-022 | à attribuer | concept théorique importé | « hantologique » | reference_or_concept |
| HIST-C1-023 | S31 | qualification analytique | « gélide » | candidate |
| HIST-C1-024 | S31 | concept | « glaciale » | reference_or_concept |
| HIST-C1-025 | à attribuer | concept | « incorporation » | reference_or_concept |
| HIST-C1-026 | S25 | notion analytique | « l'écosystème mancunien » | reference_or_concept |
| HIST-C1-027 | à attribuer | titre de chanson | « Isolation » | reference_or_concept |
| HIST-C1-028 | à attribuer | titre de chanson | « Twenty Four Hours » | reference_or_concept |
| HIST-C1-029 | à attribuer | formulation analytique | « entreprise commune » | reference_or_concept |
| HIST-C1-030 | à attribuer | verbatim | « l'historicisme imaginatif » | candidate |
| HIST-C1-031 | S72 legacy S20 | paraphrase | « Joy Division a créé quelque chose qui, tout en étant profondément ancré dans ... » | candidate |
| HIST-C1-032 | à attribuer | verbatim | « double temporalité » | candidate |
| HIST-C1-033 | à attribuer | verbatim | « Il est ironique que je reçoive une reconnaissance officielle d'une ville fran... » | candidate |
| HIST-C1-034 | à attribuer | titre de chanson | « Love Will Tear Us Apart » | reference_or_concept |
| HIST-C1-035 | S25 | référence factuelle | « Pulsebeat of Manchester » | reference_or_concept |
| HIST-C1-036 | S39 | concept | « modernité liquide » | reference_or_concept |
| HIST-C1-037 | à attribuer | concept | « hantologie » | reference_or_concept |
| HIST-C1-038 | à attribuer | verbatim | « futur perdu » | candidate |
| HIST-C1-039 | S40 | verbatim | « une nostalgie du futur qui ne s'est jamais réalisé » | candidate |
| HIST-C1-040 | à attribuer | concept / traduction | « shrinking city » | reference_or_concept |
| HIST-C1-041 | S10 | paraphrase | Sumner et la disparition du lieu de ses souvenirs heureux | candidate |
| HIST-C1-042 | S10 | paraphrase | Sumner, « plus grand bidonville d'Europe » et « 70 cigarettes par jour » | candidate |
| HIST-C1-043 | S15 | paraphrase | De Luca et le concert des Sex Pistols du 4 juin 1976 | candidate |
| HIST-C1-044 | S18 | paraphrase | Fédida et l’éveil d’une scène musicale | candidate |
| HIST-C1-045 | à attribuer | paraphrase | Manchester traversée par des dynamiques contradictoires | candidate |
| HIST-C1-046 | S72 legacy S20 | paraphrase | Reynolds et le paysage urbain en déclin de Manchester | candidate |
| HIST-C1-047 | à attribuer | paraphrase | Electric Circus comme « khazi » attribué à Kevin Cummins | candidate |
| HIST-C1-048 | S26 | paraphrase | Gavin Butt et le rôle des écoles d’art | candidate |
| HIST-C1-049 | S27 | paraphrase | Nick Crossley et les réseaux sociaux de la scène | candidate |
| HIST-C1-050 | S22 | paraphrase | Wilkinson et City Fun | candidate |
| HIST-C1-051 | à attribuer | paraphrase | Cath Carroll, « Pam ponders » | candidate |
| HIST-C1-052 | S25 | paraphrase | Wilkinson, Factory et minimalisme branché / musique honnête | candidate |
| HIST-C1-053 | à attribuer | paraphrase | Wilkinson, féminisme et culture populaire | candidate |
| HIST-C1-054 | S30 | paraphrase | Simon Frith et la musique populaire comme résistance culturelle | candidate |
| HIST-C1-055 | S29 | paraphrase | Michael Goddard et transformation du paysage industriel | candidate |
| HIST-C1-056 | à attribuer | paraphrase | Goddard et approche hantologique | candidate |
| HIST-C1-057 | à attribuer | paraphrase | Connexion intime entre groupe et environnement urbain | candidate |
| HIST-C1-058 | à attribuer | paraphrase | Incertitude, anxiété et musique de Joy Division | candidate |
| HIST-C1-059 | S41 | paraphrase | Hook et le contexte local | candidate |
| HIST-C1-060 | S41 | paraphrase | Hook et les expériences locales façonnant le son | candidate |
| HIST-C1-061 | S31 | paraphrase | Allegri et l’observation / absorption de la ville | candidate |
| HIST-C1-062 | S31 | paraphrase | Allegri et l’univers sonore propre | candidate |
| HIST-C1-063 | à attribuer | paraphrase | Au-delà du mythe mancunien | candidate |
| HIST-C1-064 | S11 | paraphrase | Deborah Curtis et complexité politique de Curtis | candidate |
| HIST-C1-065 | S72 legacy S20 | paraphrase | Reynolds : local et universel | candidate |
| HIST-C1-066 | à attribuer | paraphrase | Double temporalité critique | candidate |
| HIST-C1-067 | S36 | paraphrase | Crosthwaite et innovations sonores | candidate |
| HIST-C1-068 | S41 | paraphrase | Peter Hook et reconnaissance officielle à Clermont-Ferrand | candidate |
| HIST-C1-069 | à attribuer | paraphrase | Brunow et régénération mémorielle | candidate |
| HIST-C1-070 | S40 | paraphrase | Cacciatore et nostalgie du futur | candidate |

---

# 2. Import des citations atomisées restantes

## 2.1. S41 — Hook, *Unknown Pleasures*, 2012

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S41-Q001 | « as I remember it » | candidate / original vérifié | Source primaire mémorielle ; utile en méthode. |
| S41-Q002 | « X Factor for punks » | candidate / original vérifié | Humour rétrospectif ; signaler l’anachronisme. |
| S41-Q003 | « get rid of this Nazi artwork » | candidate / original vérifié | Gretton et la pochette d’*An Ideal for Living*. |
| S41-Q004 | « stop-the-press moment » | candidate / à revérifier | « Transmission » comme moment d’évidence interne. |
| S41-Q005 | « the best recordings we had made so far » | candidate / à revérifier | « Digital » et « Glass » comme seuil technique. |
| S41-Q006 | « Burnel for the sound, Simonon for the pose » | candidate / à revérifier | Influences de Hook : son et posture. |
| S41-Q007 | « it didn't sound like us » | candidate / à revérifier | Déception initiale devant *Unknown Pleasures*. |
| S41-Q008 | « a turkey » | candidate / à vérifier | Sessions RCA / Arrow comme échec formateur. |
| S41-Q009 | « that was Joy Division becoming New Order » | candidate / à vérifier | « Ceremony » comme zone de passage. |

## 2.2. S45 — Curtis, *Touching from a Distance*, 1995

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S45-Q001 | « working nine to five » | candidate / original vérifié | Refus de la vie salariale routinière. |
| S45-Q002 | « voted Conservative » | candidate / original vérifié | Détail biographique à ne pas surpolitiser. |
| S45-Q003 | « a one-off » | candidate / original vérifié | Déni initial après le premier fit. |
| S45-Q004 | « cleaner and colder » | candidate / à revérifier | Premier effet Hannett sur *A Factory Sample*. |
| S45-Q005 | « increasingly isolated » | candidate / à vérifier | Isolement domestique croissant. |

## 2.3. S68 — Broll, *Joy Division*, 1988

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S68-Q001 | « non se ne fece quindi nulla » | candidate / à vérifier | Contrat RCA abandonné ; paraphrase préférable. |
| S68-Q002 | « non lascerà più i Joy Division » | candidate / à vérifier | Hannett comme seuil ; formule interprétative. |
| S68-Q003 | « strepitoso successo » | candidate / à vérifier | Futurama ; appréciation subjective. |

## 2.4. S69 — Greig & Strong, « But We Remember When We Were Young », 2014

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S69-Q001 | « Cet article examine à quel point nous pouvons considérer cette production comme nostalgique... » | candidate / vérifié | Fonction programmatique de l’article. |
| S69-Q002 | « la nostalgie sans mémoire » / « la nostalgie ersatz » | candidate / vérifié | Concept utile ; signaler Appadurai. |
| S69-Q003 | « nostalgie comme humeur » / « nostalgie comme mode » | candidate / vérifié | Typologie de la nostalgie ; signaler Grainge. |
| S69-Q004 | « cette autobiographie fut une expulsion du passé, un désir de s’en libérer » | candidate / vérifié | Deborah Curtis et non-nostalgie. |
| S69-Q005 | « le commerce de la mémoire » | candidate / vérifié | Citation indirectement attribuée à Saville ; vérifier Grant Gee. |
| S69-Q006 | « maintenant il pille notre patrimoine personnel » | candidate / à revérifier | Citation polémique ; vérifier l’original Guardian. |

## 2.5. S70 — Suatoni, *Dal cuore della città / From the Centre of the City*, 1990

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S70-Q001 | « appreciate the band and not simply follow them for fashion or mournful interests » | candidate / à revérifier | Critique du culte morbide. |
| S70-Q002 | « the group is only great when it lives in the music » | candidate / à revérifier | Primat de la musique sur le mythe. |
| S70-Q003 | « a sleepless night on the edge of the world, me and Joy Division » | candidate / à revérifier | Réception intime et culte de l’objet disque. |
| S70-Q004 | « into the metropolitan, into the dark, lonely alley ways of our conscience » | candidate / à revérifier | Métropole intériorisée. |
| S70-Q005 | « it is certainly wrong to see his death as the last creative gesture of Joy Division » | candidate / à revérifier | Contre la téléologie morbide. |
| S70-Q006 | « Friendship is always been the main thing, what produces music » | candidate / à revérifier | Amitié comme matrice musicale ; citation attribuée. |
| S70-Q007 | « he cleaned up the sound from old impurities » | candidate / à revérifier | Hannett architecte sonore ; simplification à encadrer. |
| S70-Q008 | « the Joy Division cult has been the creation of a myth... » | candidate / à revérifier | Attribué à Mike West ; vérifier dans S47. |
| S70-Q009 | « Ian Curtis wasn't a martyr. Not exactly. He didn't die for his art but with it. » | candidate / à revérifier | Formule sensible ; sobriété nécessaire. |
| S70-Q010 | « Joy Division's music was above everything else, simply, communication » | candidate / à revérifier | Communication affective. |
| S70-Q011 | « Our lyrics may mean something completely different to every single individual » | candidate / à revérifier | Attribué à Hook ; retrouver l’entretien. |

## 2.6. S71 — Flowers, *Dreams Never End*, 1995/2012

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S71-Q001 | « I laid on my bed with the window cracked open... » | candidate / vérifié | Réception américaine intime. |
| S71-Q002 | « ...two songs into it, I thought I was gonna puke » | candidate / vérifié | Effet physique de *Closer*. |
| S71-Q003 | « Warsaw was just different » | candidate / vérifié | Gretton et l’altérité de Warsaw. |
| S71-Q004 | « The name Factory came about not as a tribute to Andy Warhol’s Factory... » | candidate / vérifié | Origine du nom Factory. |
| S71-Q005 | « Like Joy Division, Tony Wilson cared more about art than money or business » | candidate / vérifié | Formule synthétique à nuancer. |
| S71-Q006 | « With Martin Hannett focusing their message... » | candidate / vérifié | Hannett et concentration sonore. |
| S71-Q007 | « For Ian’s sake, flashing lights were strictly prohibited » | candidate / vérifié | Maladie et scène. |
| S71-Q008 | « why don’t we do the first album here (on Factory), with you? » | candidate / vérifié | Choix Factory. |
| S71-Q009 | « I’ve got the spirit, but lose the feeling » | candidate / vérifié | Parole de chanson ; citation très limitée. |
| S71-Q010 | « They insisted that people should decide for themselves what the songs meant » | candidate / vérifié | Sens ouvert des paroles. |
| S71-Q011 | « They chose the darkness » | candidate / vérifié | Formule critique, non preuve. |
| S71-Q012 | « The paradox of Joy Division was that their songs got better... » | candidate / vérifié | Risque de romantisation. |
| S71-Q013 | « I’ve been waiting for a guide... » | candidate / vérifié | Analyse d’« Atrocity Exhibition ». |
| S71-Q014 | « Their innocence died with him » | candidate / vérifié | Passage à New Order. |
| S71-Q015 | « suddenly Barney finds his voice » | candidate / vérifié | « Temptation » et voix de Sumner. |
| S71-Q016 | « The business side of running the Hacienda became an absolute nightmare » | candidate / vérifié | Hacienda et économie. |
| S71-Q017 | « Peter Hook’s bass riffs in ‘Blue Monday’... » | candidate / vérifié | Continuité New Order / dance music. |
| S71-Q018 | « the video was a bit reverential, really, and a bit corny » | candidate / vérifié | Gretton sur « Atmosphere ». |
| S71-Q019 | « I wanted to sell a dead rock star... » | candidate / vérifié | Wilson ; citation explosive à contextualiser. |
| S71-Q020 | « The first LP we’ve recorded that is as good as Joy Division » | candidate / vérifié | *Technique* mesuré à Joy Division. |

## 2.7. S72 — Reynolds, *Rip It Up and Start Again*, 2005/2006

| ID | Citation originale | Statut | Usage / arbitrage |
|---|---|---|---|
| S72-Q001 | « The postpunk vanguard [...] defined punk as an imperative to constant change » | candidate / vérifié | Cadre théorique post-punk. |
| S72-Q002 | « radical content demands radical form » | candidate / vérifié | Éthique formelle du post-punk. |
| S72-Q003 | « the bass [could] step forward [...] to become the lead instrumental voice » | candidate / vérifié | Basse mélodique. |
| S72-Q004 | « some critics actually playing a part in shaping and directing the culture » | candidate / vérifié | Presse musicale comme acteur. |
| S72-Q005 | « No contracts were signed with the groups... » | candidate / vérifié | Factory et absence de contrats. |
| S72-Q006 | « the traumatized urban landscape serves not only as the backdrop... » | candidate / vérifié | Ballard et paysage traumatisé. |
| S72-Q007 | « poised on the membrane between the local and universal » | candidate / vérifié | Citation clé local / universel. |
| S72-Q008 | « Something about the city’s gloom and decrepitude... » | candidate / vérifié | Manchester et matière sonore. |
| S72-Q009 | « coldness, pressure, darkness, crisis, failure, collapse, loss of control » | candidate / vérifié | Lexique critique de Curtis. |
| S72-Q010 | « All that space in Joy Division’s music... » | candidate / vérifié | Espace musical. |
| S72-Q011 | « Curtis intoned from ‘a lonely place’... » | candidate / vérifié | Voix et vide. |

---

# 3. Règles d’arbitrage maintenues

```yaml
id: QUOTES-CONSOLIDATION-RULES-001
statut_consolidation: active
rules:
  - Les citations historiques sont importées comme matériau de travail, non comme vérité supérieure.
  - Les citations atomisées sont importées comme candidates, sauf promotion explicite.
  - Les titres de chansons, concepts et paraphrases ne doivent pas être mis entre guillemets comme citations directes.
  - Les citations issues de S68 et S70 doivent être vérifiées sur fac-similé ou scan propre.
  - Les citations de paroles de chansons doivent rester très courtes et strictement nécessaires.
  - Les citations indirectement attribuées doivent être vérifiées dans la source primaire lorsque celle-ci existe.
```
