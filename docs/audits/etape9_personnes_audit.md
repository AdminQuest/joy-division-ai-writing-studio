# Étape 9 — Audit des acteurs (`PERSON-`) — passe en lecture seule

*Audit produit le 2026-05-31, révisé après la revue Codex de la PR #46. Lecture seule : aucun registre, atome ou master-doc modifié. Aucune fusion, aucun renommage, aucune canonicalisation — l'audit inventorie et signale, il ne tranche pas. Tous les chiffres sont recalculés depuis `exports/generated/people.json` et `quotes.json`.*

## 0. Méthode et périmètre

Sources balayées :

1. La couche provisoire `PERS-*` (`registers/people/`, agrégée dans `exports/generated/people.json`) : préfixes `PERS-0NN`, `PERS-SXX-NNN`, variantes épisodiques `PERS-S45-*`, compléments `PERS-00N-S75`.
2. Les champs d'attribution dénormalisés des 962 citations (`exports/generated/quotes.json`) : `locuteur`, `auteur_source`, `rapporteur`, `attribution_a_arbitrer`.
3. Les registres gelés (`CHR-`/`EVENT-`, `CONCERT-`, `PLACE-`) — consultés pour recoupement, non modifiés.

**Règle de typage (rappel, appliquée au §4).** Une entrée part vers `ORG-` **uniquement si son référent est une entité collective ou morale** (groupe, label, promoteur en tant que structure, salle-organisation, fanzine-publication, équipe). Un individu porteur d'un rôle organisationnel (« manager », « organisateur », « patron de label », « auteur de fanzine ») **reste `PERSON-`**. Le rôle ne détermine jamais le typage ; seule la nature du référent compte.

Volumétrie : **305** entrées `PERS-*` distinctes (couple id + nom) → **175** chaînes-noms distinctes ; **962** citations. Identité de partition vérifiée : 175 entrées en grappes (≥ 2 id) + 130 entrées à identifiant unique = **305**.

> Statuts de grappe : `fusion_evidente` · `a_arbitrer` · `distinct`.

## 1. Inventaire brut

### 1.1. Personnes portant plusieurs identifiants `PERS-*` (candidates `same_as`)

| Nom | Occ. | Identifiants `PERS-*` | Sources | Rôle(s) observé(s) |
|-----|:----:|----------------------|---------|--------------------|
| Tony Wilson | 12 | PERS-007, PERS-S21-006, PERS-S31-005, PERS-S34-004, PERS-S45-TONY-WILSON-GRANADA, PERS-S52-011, PERS-S53-006, PERS-S58-004, PERS-S76-022, PERS-S76-050, PERS-S76-073, PERS-S78-005 | S21, S31, S34, S45, S52, S53, S58, S76, S78 | journaliste; entrepreneur culturel; fondateur Factory; médiateur / Médiateur télévisuel et Factory ; dans S34, sa mémoire de Manchester sout |
| Ian Curtis | 11 | PERS-001, PERS-S29-002, PERS-S34-010, PERS-S45-IAN-CURTIS-VOTE-CONSERVATEUR, PERS-S49-002, PERS-S53-002, PERS-S54-002, PERS-S55-002, PERS-S56-002, PERS-S57-004, PERS-S59-002 | S29, S34, S45, S49, S53, S54, S55, S56, S57, S59 | chanteur; parolier; figure centrale / Chanteur et parolier de Joy Division ; figure centrale de la lecture hauntologique, sous prudence anti |
| Martin Hannett | 9 | PERS-008, PERS-S31-004, PERS-S34-011, PERS-S45-MARTIN-HANNETT-UNKNOWN-PLEASURES, PERS-S58-006, PERS-S59-005, PERS-S76-024, PERS-S76-069, PERS-S76-072 | S31, S34, S45, S58, S59, S76 | producteur; ingénieur sonore; expérimentateur / Producteur dont l’usage de l’espace sonore est discuté par S34 via Reynolds, mais à ne pas i |
| Paul Morley | 9 | PERS-014, PERS-S21-007, PERS-S34-012, PERS-S45-PAUL-MORLEY-1977, PERS-S45-PAUL-MORLEY-BAND-ON-THE-WALL, PERS-S75-037, PERS-S76-089, PERS-S77-008, PERS-S78-003 | S21, S34, S45, S75, S76, S77, S78 | Critique cité pour caractériser l’espace sonore et la non-connexion dans *Unknown Pleasures*. / journaliste; critique; témoin / critique mus |
| Peter Saville | 7 | PERS-009, PERS-S31-008, PERS-S53-004, PERS-S59-004, PERS-S60-002, PERS-S75-029, PERS-S76-049 | S31, S53, S59, S60, S75, S76 | designer; directeur artistique / designer graphique; auteur de la pochette d'Unknown Pleasures / designer graphique; étudiant à Manchester P |
| Rob Gretton | 7 | PERS-006, PERS-S31-007, PERS-S45-ROB-GRETTON-GARDIEN, PERS-S58-005, PERS-S75-030, PERS-S76-027, PERS-S76-037 | S31, S45, S58, S75, S76 | manager; stratège; médiateur / manager de Joy Division; gardien de l'image et des objets Factory / futur manager de Joy Division; DJ à Rafte |
| Annik Honoré | 6 | PERS-S52-012, PERS-S54-007, PERS-S75-032, PERS-S76-063, PERS-S76-067, PERS-S76-070 | S52, S54, S75, S76 | relation intime de Ian Curtis; figure de la crise biographique finale / journaliste/fanzine En Attendant; future cofondatrice liée à Factory |
| Bernard Sumner | 6 | PERS-003, PERS-003-S75, PERS-S45-BERNARD-SUMNER-TABLETS, PERS-S52-006, PERS-S55-004, PERS-S58-003 | S45, S52, S55, S58, S75 | musicien; guitariste; témoin / musicien; guitariste; témoin; trajectoire sociale / Témoin mobilisé par Rabbito pour décrire la personnalité |
| Kevin Cummins | 6 | PERS-S53-003, PERS-S75-023, PERS-S76-012, PERS-S76-023, PERS-S76-056, PERS-S78-006 | S53, S75, S76, S78 | photographe; médiateur visuel / photographe; témoin de la scène mancunienne / photographe; témoin de l’Electric Circus; acteur fanzine / Neg |
| Peter Hook | 6 | PERS-002, PERS-S52-007, PERS-S54-006, PERS-S55-003, PERS-S58-002, PERS-S59-003 | S52, S54, S55, S58, S59 | musicien; bassiste; témoin; mémorialiste / Témoin mobilisé par Rabbito pour la violence scénique et la personnalité explosive de Curtis. / T |
| Stephen Morris | 6 | PERS-004, PERS-004-S75, PERS-S45-STEPHEN-MORRIS, PERS-S52-008, PERS-S55-005, PERS-S75-026 | S45, S52, S55, S75 | musicien; batteur; témoin / musicien; batteur; catalyseur formel / batteur de Joy Division; opérateur rythmique du son Hannett / Témoin mobi |
| Grant Gee | 5 | PERS-S29-010, PERS-S34-003, PERS-S52-010, PERS-S78-010, PERS-S84-007 | S29, S34, S52, S78, S84 | Réalisateur du documentaire *Joy Division*, valorisé par Goddard via Fisher pour son régime fragmentaire d’archive. / Réalisateur du documen |
| Anton Corbijn | 4 | PERS-S29-011, PERS-S52-002, PERS-S53-005, PERS-S78-007 | S29, S52, S53, S78 | Réalisateur de *Control*, film utilisé par Goddard comme contrepoint à l’archive fragmentaire de Grant Gee. / Réalisateur de Control ; ancie |
| Deborah Curtis | 4 | PERS-005, PERS-S45-DEBORAH-CURTIS-LOGISTIQUE-FORMATION, PERS-S45-DEBORAH-CURTIS-TEMOIN-POLITIQUE-DOMESTIQUE, PERS-S52-005 | S45, S52 | témoin; proche; autrice; gardienne d’archive / Source intime centrale mobilisée par Rabbito ; témoin des deux côtés de la personnalité de Cu |
| John Anderson | 4 | PERS-S45-JOHN-ANDERSON, PERS-S75-019, PERS-S76-034, PERS-S76-044 | S45, S75, S76 | producteur; responsable Grapevine; intermédiaire industriel / responsable de Grapevine Records; producteur / directeur de session associé au |
| Jon Savage | 4 | PERS-S52-009, PERS-S56-003, PERS-S77-003, PERS-S78-004 | S52, S56, S77, S78 | Source documentaire utilisée par Rabbito pour des témoignages sur Curtis et Joy Division. / Auteur discuté par Barone pour traduction, parat |
| Natalie Curtis | 4 | PERS-011, PERS-S45-NATALIE-CURTIS-BIRTH, PERS-S75-028, PERS-S76-061 | S45, S75, S76 | proche; enfant de Ian Curtis / fille de Ian et Deborah Curtis / fille de Ian Curtis et Deborah Curtis |
| Alan Erasmus | 3 | PERS-S31-006, PERS-S75-024, PERS-S76-045 | S31, S75, S76 | cofondateur Factory; organisateur; figure effacée du récit / acteur; cofondateur du dispositif Factory avec Tony Wilson; promoteur initial a |
| Derek Brandwood | 3 | PERS-S45-DEREK-BRANDWOOD, PERS-S75-017, PERS-S76-032 | S45, S75, S76 | responsable RCA nord; intermédiaire industrie musicale / représentant RCA nord de l’Angleterre; médiateur industriel des sessions RCA/Grapev |
| Liz Naylor | 3 | PERS-S21-001, PERS-S77-005, PERS-S78-002 | S21, S77, S78 | Contributrice associée à City Fun, à vérifier item par item ; voix importante à croiser avec S22. / Contributrice de City Fun, associée par |
| Mark Reeder | 3 | PERS-S76-011, PERS-S76-029, PERS-S76-053 | S76 | témoin des sociabilités de disquaires; ami musical de Ian Curtis / témoin de Rare Records/Virgin; ami de Ian Curtis; témoin du changement de |
| Richard Searling | 3 | PERS-S45-RICHARD-SEARLING, PERS-S75-018, PERS-S76-033 | S45, S75, S76 | DJ northern soul; producteur associé / DJ northern soul; assistant de Derek Brandwood; intermédiaire du projet RCA/Grapevine |
| Steve Brotherdale | 3 | PERS-015, PERS-S45-STEVE-BROTHERDALE, PERS-S76-020 | S45, S76 | musicien; batteur transitoire / batteur transitoire de Warsaw; acteur de la scène mancunienne |
| Terry Mason | 3 | PERS-S45-TERRY-MASON, PERS-S76-016, PERS-S76-074 | S45, S76 | ami de Bernard Sumner et Peter Hook; premier organisateur / manager informel de Warsaw; témoin direct des débuts / témoin logistique et anci |
| Vini Reilly | 3 | PERS-S75-027, PERS-S76-014, PERS-S76-088 | S75, S76 | musicien de The Durutti Column; témoin technique de l'usage du delay / musicien; futur membre / centre de Durutti Column; témoin pré-Warsaw |
| William S. Burroughs 📖 | 3 | PERS-S54-003, PERS-S56-004, PERS-S75-033 | S54, S56, S75 | écrivain; figure d'admiration pour Ian Curtis / Matrice littéraire centrale pour Interzone, Digital, langage-virus, contrôle et fragmentatio |
| Alan Hempsall | 2 | PERS-S75-035, PERS-S76-080 | S75, S76 | chanteur de Crispy Ambulance; substitut vocal ponctuel à Derby Hall / chanteur de Crispy Ambulance; voix de substitution au Derby Hall de Bu |
| Alan Wise | 2 | PERS-S76-047, PERS-S76-054 | S76 | promoteur local; gestionnaire des soirées au Russell Club selon S76; témoin du rôle visuel de Peter Saville / promoteur / acteur Factory Clu |
| Bernie Binnick | 2 | PERS-S45-BERNIE-BINNICK, PERS-S76-036 | S45, S76 | exécutif américain lié au projet Grapevine/RCA; producteur de soul destiné à l’export britannique |
| Bob Auger | 2 | PERS-S75-020, PERS-S76-035 | S75, S76 | producteur; ingénieur / superviseur studio / ingénieur / acteur technique des sessions Arrow selon S76 |
| Candy | 2 | PERS-S45-CANDY, PERS-S76-076 | S45, S76 | chien de Ian Curtis; élément domestique de la crise conjugale |
| Carole Curtis | 2 | PERS-S76-004, PERS-S76-087 | S76 | sœur de Ian Curtis; témoin familial / sœur de Ian Curtis; mémoire familiale endeuillée |
| Cath Carroll | 2 | PERS-S21-002, PERS-S77-006 | S21, S77 | Contributrice associée à City Fun, à vérifier item par item ; voix importante à croiser avec S22. / Contributrice de City Fun ; exemple de p |
| Ernest Beard | 2 | PERS-S45-ERNEST-BEARD, PERS-S45-ERNEST-BEARD-EPILEPSY | S45 |  |
| Genesis P-Orridge | 2 | PERS-S29-003, PERS-S76-086 | S29, S76 | Figure de Throbbing Gristle et Psychic TV ; témoin revendiquant une affinité avec Ian Curtis. / artiste Throbbing Gristle; témoin d’alerte a |
| Iain Gray | 2 | PERS-S45-IAIN-GRAY, PERS-S76-017 | S45, S76 | ami de Ian Curtis; guitariste des répétitions embryonnaires pré-Warsaw; acteur périphérique rapidement effacé |
| Jean-Pierre Turmel | 2 | PERS-S75-036, PERS-S76-066 | S75, S76 | auteur du texte de pochette de Licht und Blindheit; médiateur Sordide Sentimental / fondateur / animateur de Sordide Sentimental; médiateur |
| John Peel | 2 | PERS-S75-021, PERS-S76-057 | S75, S76 | DJ radio; médiateur national / animateur radio BBC; prescripteur national; réception critique de Joy Division |
| Lesley Gilbert | 2 | PERS-S45-LESLEY-GILBERT, PERS-S76-043 | S45, S76 | compagne de Rob Gretton; salariée d’un cabinet d’avocats selon Terry Mason |
| Malcolm Whitehead | 2 | PERS-S78-009, PERS-S84-001 | S78, S84 | Réalisateur du film Joy Division de 1979, mêlant scènes urbaines, publicités, Anderton et concert de Bowdon Vale. / Réalisateur amateur, fil |
| Martin Rushent | 2 | PERS-S75-022, PERS-S76-058 | S75, S76 | producteur; entrepreneur de production / producteur; fondateur / acteur de Genetic Records; producteur potentiel alternatif pour Joy Divisio |
| Raf Simons | 2 | PERS-S60-004, PERS-S85-005 | S60, S85 | Créateur de mode mobilisé pour les réemplois du motif Joy Division dans l’art, le vêtement et la distinction. / Designer belge — parka avec |
| Richard Boon | 2 | PERS-S76-019, PERS-S84-002 | S76, S84 | manager de Buzzcocks; interlocuteur précoce de Curtis; médiateur de scène / Manager des Buzzcocks, opérateur Betamax Apollo Manchester (28 o |
| Sue Barlow | 2 | PERS-S45-SUE-BARLOW, PERS-S45-SUE-BARLOW-GIRLIES | S45 |  |
| Tony Nuttall | 2 | PERS-S45-TONY-NUTTALL-RUPTURE-POLITIQUE, PERS-S76-007 | S45, S76 | ami d'enfance de Ian Curtis; compagnon de speedway et de sociabilité locale |

<sub>🅾 = au moins un id à sortir vers `ORG-` (§4.1) · 📖 = figure d'influence (§4.2).</sub>

### 1.2. Personnes à identifiant unique

| Source | Personnes (id — nom) |
|--------|----------------------|
| ? | PERS-010 — Annick Honoré; PERS-012 — John Brierley; PERS-013 — Chris Ott; PERS-016 — Bedhead |
| S21 | PERS-S21-003 — Andy Zero; PERS-S21-004 — Martin X; PERS-S21-005 — Neil Hargreaves |
| S29 | PERS-S29-001 — Michael Goddard; PERS-S29-004 — Cosey Fanni Tutti; PERS-S29-005 — Mark Fisher; PERS-S29-006 — Simon Reynolds; PERS-S29-007 — Jacques Derrida; PERS-S29-008 — Franco Berardi; PERS-S29-009 — Paul Crosthwaite; PERS-S29-012 — Nikolai Gogol |
| S31 | PERS-S31-001 — Giuseppe Allegri; PERS-S31-002 — Franco Berardi Bifo; PERS-S31-003 — Greil Marcus |
| S34 | PERS-S34-001 — Benjamin Fraser; PERS-S34-002 — Abby Fuoto; PERS-S34-005 — Marshall Berman; PERS-S34-006 — Henri Lefebvre; PERS-S34-007 — Georg Simmel; PERS-S34-008 — David Harvey; PERS-S34-009 — Jane Jacobs |
| S45 | PERS-S45-DEAN-CHECK-INN — Dean; PERS-S45-GILLIAN-GILBERT-GOSHES — Gillian Gilbert; PERS-S45-MICK-MIDDLES-BAND-ON-THE-WALL — Mick Middles; PERS-S45-STEPHANIE-MORRIS — Stephanie |
| S49 | PERS-S49-001 — Manolo Farci; PERS-S49-003 — David Byrne |
| S50 | PERS-S50-001 — Paolo Bertetti; PERS-S50-002 — Domenico Morreale; PERS-S50-003 — Orian Williams; PERS-S50-004 — Warren Jackson; PERS-S50-005 — Vincent Moon |
| S51 | PERS-S51-001 — Jennifer Malvezzi; PERS-S51-002 — Mark Leckey; PERS-S51-003 — Hito Steyerl; PERS-S51-004 — Aby Warburg |
| S52 | PERS-S52-001 — Andrea Rabbito; PERS-S52-003 — Sam Riley; PERS-S52-004 — Samantha Morton |
| S53 | PERS-S53-001 — Fabio La Rocca; PERS-S53-007 — Henri Bergson; PERS-S53-008 — Christian Norberg-Schulz; PERS-S53-009 — Arthur Schopenhauer; PERS-S53-010 — Friedrich Nietzsche; PERS-S53-011 — Michael Winterbottom |
| S54 | PERS-S54-001 — Alessandro Gnocchi; PERS-S54-004 — J. G. Ballard; PERS-S54-005 — Brion Gysin; PERS-S54-008 — Daniel Odier; PERS-S54-009 — Pete Shelley |
| S55 | PERS-S55-001 — Vincenzo Romania |
| S56 | PERS-S56-001 — Linda Barone |
| S57 | PERS-S57-001 — Massimo Villani; PERS-S57-002 — Maurice Blanchot; PERS-S57-003 — Georg Wilhelm Friedrich Hegel |
| S58 | PERS-S58-001 — Emiliano Ilardi |
| S59 | PERS-S59-001 — Francesca Ferrara |
| S60 | PERS-S60-001 — Raffaele Federici; PERS-S60-003 — Jacques Attali; PERS-S60-005 — Vince Staples |
| S75 | PERS-S75-025 — T.J. Davidson; PERS-S75-031 — Marcel Proust; PERS-S75-034 — Bob Krasnow |
| S76 | PERS-S76-001 — Lindsay Reade; PERS-S76-002 — Doreen Curtis; PERS-S76-003 — Kevin Curtis; PERS-S76-005 — Barbara Lloyd / Aunt Barbara; PERS-S76-006 — Pete Johnson; PERS-S76-008 — Paul Heapy; PERS-S76-009 — Deborah Woodruff / Deborah Curtis; PERS-S76-010 — David Bowie; PERS-S76-013 — Clinton Heylin; PERS-S76-015 — Kelvin Briggs; PERS-S76-018 — Steve Burke / Steve Shy; PERS-S76-021 — Steve Morris; PERS-S76-025 — Tosh Ryan; PERS-S76-026 — Lawrence Beedle; PERS-S76-028 — Bob Dickinson; PERS-S76-030 — John The Postman; PERS-S76-031 — Steven Morrissey; PERS-S76-038 — Mike Pickering; PERS-S76-039 — Donald Johnson; PERS-S76-040 — Eddie Garrity / Ed Banger; PERS-S76-041 — Ian Wood; PERS-S76-042 — Jeremy Kerr; PERS-S76-046 — Don Tonay; PERS-S76-048 — Roger Eagle; PERS-S76-051 — Tony Davidson / T. J. Davidson; PERS-S76-052 — Oz PA / Eddy et Oz; PERS-S76-055 — Dr David Holmes; PERS-S76-059 — Martin O’Neill; PERS-S76-060 — Paul Hanley; PERS-S76-062 — Dave McCullough; PERS-S76-064 — Dave Pils et Jasmine; PERS-S76-065 — Steve Harley; PERS-S76-068 — Buzzcocks; PERS-S76-071 — Minny Pops; PERS-S76-075 — John Curd; PERS-S76-077 — Dave Pils; PERS-S76-078 — Martyn Atkins; PERS-S76-079 — Bernard Pierre Wolff; PERS-S76-081 — Simon Topping; PERS-S76-082 — Perry Boys; PERS-S76-083 — Larry Cassidy; PERS-S76-084 — Kevin Wood; PERS-S76-085 — Pam Wood |
| S77 | PERS-S77-001 — Matthew Worley; PERS-S77-002 — Mark Perry / Mark P; PERS-S77-004 — Tony Drayton / Tony D / Tony Puppy; PERS-S77-007 — Andy Zero / Andy Waide; PERS-S77-009 — Penny Rimbaud; PERS-S77-010 — Lucy Toothpaste / Lucy Whitman |
| S78 | PERS-S78-001 — Leonard Nevarez; PERS-S78-008 — Charles Salem |
| S84 | PERS-S84-003 — Bob Jones; PERS-S84-004 — Michel Isbecque; PERS-S84-005 — Dik Verdult; PERS-S84-006 — Stuart Orme; PERS-S84-008 — Nick Cope |
| S85 | PERS-S85-001 — Colin Malcolm; PERS-S85-002 — Kevin Buckle; PERS-S85-003 — Tom Hingley; PERS-S85-004 — David Haslam; PERS-S85-006 — Lou Stoppard / Adam Murray; PERS-S85-007 — Bob Stanley; PERS-S85-008 — Jeremey Deller |

## 2. Grappes de déduplication pressenties

> Vérifications : `PERS-S76-022` = **Tony Wilson** (non Gretton) ; `PERS-003-S75` = **Bernard Sumner** ; aucun identifiant « Bernard Albrecht » n'existe (alias non internalisé, cf. §3.2).

### 2.1. Grappes explicitement demandées (vérifiées sur `people.json`)

| Personne | Occ. | Identifiants | Sources | Statut | Observation |
|----------|:----:|--------------|---------|:------:|-------------|
| Rob Gretton | 7 | PERS-006, PERS-S31-007, PERS-S45-ROB-GRETTON-GARDIEN, PERS-S58-005, PERS-S75-030, PERS-S76-027, PERS-S76-037 | S31, S45, S58, S75, S76 | `fusion_evidente` | Manager JD/New Order. |
| Martin Hannett | 9 | PERS-008, PERS-S31-004, PERS-S34-011, PERS-S45-MARTIN-HANNETT-UNKNOWN-PLEASURES, PERS-S58-006, PERS-S59-005, PERS-S76-024, PERS-S76-069, PERS-S76-072 | S31, S34, S45, S58, S59, S76 | `fusion_evidente` | Producteur (alias « Martin Zero » sur `PERS-S76-024`). |
| Peter Saville | 7 | PERS-009, PERS-S31-008, PERS-S53-004, PERS-S59-004, PERS-S60-002, PERS-S75-029, PERS-S76-049 | S31, S53, S59, S60, S75, S76 | `fusion_evidente` | Directeur artistique Factory. |
| Tony Wilson | 12 | PERS-007, PERS-S21-006, PERS-S31-005, PERS-S34-004, PERS-S45-TONY-WILSON-GRANADA, PERS-S52-011, PERS-S53-006, PERS-S58-004, PERS-S76-022, PERS-S76-050, PERS-S76-073, PERS-S78-005 | S21, S31, S34, S45, S52, S53, S58, S76, S78 | `fusion_evidente` | Granada / fondateur Factory ; inclut `PERS-S76-022`. |
| Kevin Cummins | 6 | PERS-S53-003, PERS-S75-023, PERS-S76-012, PERS-S76-023, PERS-S76-056, PERS-S78-006 | S53, S75, S76, S78 | `fusion_evidente` | Photographe. |
| Jean-Pierre Turmel | 2 | PERS-S75-036, PERS-S76-066 | S75, S76 | `fusion_evidente` | Sordide Sentimental. |
| John Anderson | 4 | PERS-S45-JOHN-ANDERSON, PERS-S75-019, PERS-S76-034, PERS-S76-044 | S45, S75, S76 | `a_arbitrer` | Grapevine / RCA-Northern Soul ; nom courant, homonymie non écartée. |
| Terry Mason | 3 | PERS-S45-TERRY-MASON, PERS-S76-016, PERS-S76-074 | S45, S76 | `fusion_evidente` | Cercle initial Warsaw. |
| Bernard Sumner | 6 | PERS-003, PERS-003-S75, PERS-S45-BERNARD-SUMNER-TABLETS, PERS-S52-006, PERS-S55-004, PERS-S58-003 | S45, S52, S55, S58, S75 | `fusion_evidente` | Guitariste ; alias « Bernard Albrecht » à ajouter en `alt_names` (§3.2). |

### 2.2. Autres grappes multi-identifiants (≥ 2 id) détectées automatiquement

Statut par défaut `fusion_evidente` (personne identifiable, nom non ambigu). Entités collectives et figures d'influence **exclues** (→ §4). « Steve Morris » (`PERS-S76-021`) est réintégré ici comme variante `a_arbitrer` de « Stephen Morris ».

| Personne | Occ. | Identifiants | Sources | Statut |
|----------|:----:|--------------|---------|:------:|
| Ian Curtis | 11 | PERS-001, PERS-S29-002, PERS-S34-010, PERS-S45-IAN-CURTIS-VOTE-CONSERVATEUR, PERS-S49-002, PERS-S53-002, PERS-S54-002, PERS-S55-002, PERS-S56-002, PERS-S57-004, PERS-S59-002 | S29, S34, S45, S49, S53, S54, S55, S56, S57, S59 | `fusion_evidente` |
| Paul Morley | 9 | PERS-014, PERS-S21-007, PERS-S34-012, PERS-S45-PAUL-MORLEY-1977, PERS-S45-PAUL-MORLEY-BAND-ON-THE-WALL, PERS-S75-037, PERS-S76-089, PERS-S77-008, PERS-S78-003 | S21, S34, S45, S75, S76, S77, S78 | `fusion_evidente` |
| Annik Honoré | 6 | PERS-S52-012, PERS-S54-007, PERS-S75-032, PERS-S76-063, PERS-S76-067, PERS-S76-070 | S52, S54, S75, S76 | `fusion_evidente` |
| Peter Hook | 6 | PERS-002, PERS-S52-007, PERS-S54-006, PERS-S55-003, PERS-S58-002, PERS-S59-003 | S52, S54, S55, S58, S59 | `fusion_evidente` |
| Stephen Morris | 6 | PERS-004, PERS-004-S75, PERS-S45-STEPHEN-MORRIS, PERS-S52-008, PERS-S55-005, PERS-S75-026 | S45, S52, S55, S75 | `fusion_evidente` |
| Grant Gee | 5 | PERS-S29-010, PERS-S34-003, PERS-S52-010, PERS-S78-010, PERS-S84-007 | S29, S34, S52, S78, S84 | `fusion_evidente` |
| Anton Corbijn | 4 | PERS-S29-011, PERS-S52-002, PERS-S53-005, PERS-S78-007 | S29, S52, S53, S78 | `fusion_evidente` |
| Deborah Curtis | 4 | PERS-005, PERS-S45-DEBORAH-CURTIS-LOGISTIQUE-FORMATION, PERS-S45-DEBORAH-CURTIS-TEMOIN-POLITIQUE-DOMESTIQUE, PERS-S52-005 | S45, S52 | `fusion_evidente` |
| Jon Savage | 4 | PERS-S52-009, PERS-S56-003, PERS-S77-003, PERS-S78-004 | S52, S56, S77, S78 | `fusion_evidente` |
| Natalie Curtis | 4 | PERS-011, PERS-S45-NATALIE-CURTIS-BIRTH, PERS-S75-028, PERS-S76-061 | S45, S75, S76 | `fusion_evidente` |
| Alan Erasmus | 3 | PERS-S31-006, PERS-S75-024, PERS-S76-045 | S31, S75, S76 | `fusion_evidente` |
| Derek Brandwood | 3 | PERS-S45-DEREK-BRANDWOOD, PERS-S75-017, PERS-S76-032 | S45, S75, S76 | `fusion_evidente` |
| Liz Naylor | 3 | PERS-S21-001, PERS-S77-005, PERS-S78-002 | S21, S77, S78 | `fusion_evidente` |
| Mark Reeder | 3 | PERS-S76-011, PERS-S76-029, PERS-S76-053 | S76 | `fusion_evidente` |
| Richard Searling | 3 | PERS-S45-RICHARD-SEARLING, PERS-S75-018, PERS-S76-033 | S45, S75, S76 | `fusion_evidente` |
| Steve Brotherdale | 3 | PERS-015, PERS-S45-STEVE-BROTHERDALE, PERS-S76-020 | S45, S76 | `fusion_evidente` |
| Vini Reilly | 3 | PERS-S75-027, PERS-S76-014, PERS-S76-088 | S75, S76 | `fusion_evidente` |
| Alan Hempsall | 2 | PERS-S75-035, PERS-S76-080 | S75, S76 | `fusion_evidente` |
| Alan Wise | 2 | PERS-S76-047, PERS-S76-054 | S76 | `fusion_evidente` |
| Bernie Binnick | 2 | PERS-S45-BERNIE-BINNICK, PERS-S76-036 | S45, S76 | `fusion_evidente` |
| Bob Auger | 2 | PERS-S75-020, PERS-S76-035 | S75, S76 | `fusion_evidente` |
| Candy | 2 | PERS-S45-CANDY, PERS-S76-076 | S45, S76 | `fusion_evidente` |
| Carole Curtis | 2 | PERS-S76-004, PERS-S76-087 | S76 | `fusion_evidente` |
| Cath Carroll | 2 | PERS-S21-002, PERS-S77-006 | S21, S77 | `fusion_evidente` |
| Ernest Beard | 2 | PERS-S45-ERNEST-BEARD, PERS-S45-ERNEST-BEARD-EPILEPSY | S45 | `fusion_evidente` |
| Genesis P-Orridge | 2 | PERS-S29-003, PERS-S76-086 | S29, S76 | `fusion_evidente` |
| Iain Gray | 2 | PERS-S45-IAIN-GRAY, PERS-S76-017 | S45, S76 | `fusion_evidente` |
| John Peel | 2 | PERS-S75-021, PERS-S76-057 | S75, S76 | `fusion_evidente` |
| Lesley Gilbert | 2 | PERS-S45-LESLEY-GILBERT, PERS-S76-043 | S45, S76 | `fusion_evidente` |
| Malcolm Whitehead | 2 | PERS-S78-009, PERS-S84-001 | S78, S84 | `fusion_evidente` |
| Martin Rushent | 2 | PERS-S75-022, PERS-S76-058 | S75, S76 | `fusion_evidente` |
| Raf Simons | 2 | PERS-S60-004, PERS-S85-005 | S60, S85 | `fusion_evidente` |
| Richard Boon | 2 | PERS-S76-019, PERS-S84-002 | S76, S84 | `fusion_evidente` |
| Sue Barlow | 2 | PERS-S45-SUE-BARLOW, PERS-S45-SUE-BARLOW-GIRLIES | S45 | `fusion_evidente` |
| Tony Nuttall | 2 | PERS-S45-TONY-NUTTALL-RUPTURE-POLITIQUE, PERS-S76-007 | S45, S76 | `fusion_evidente` |

## 3. Cas sensibles isolés — NE PAS fusionner

### 3.1. « Kevin Curtis » vs Ian Kevin Curtis

- **`PERS-S76-003` « Kevin Curtis »** (source S76) — rôle : *père de Ian Curtis; policier ferroviaire; ancien marin blessé pendant la guerre*.
- **`PERS-001` Ian Curtis** — nom complet *Ian Kevin Curtis*.

Le registre S76 décrit `PERS-S76-003` comme le **père de Ian Curtis** ; mais la chaîne coïncide avec le deuxième prénom de Ian (**Ian Kevin Curtis**). Deux lectures : (a) parent réel homonyme ; (b) artefact de segmentation. **Statut : `distinct` provisoire — documenté, non tranché.** Revérifier S76 (*Torn Apart*) avant décision.

### 3.2. Variantes orthographiques — confirmer le périmètre `same_as`

| Variante | Identifiant(s) | Périmètre `same_as` à confirmer |
|----------|----------------|---------------------------------|
| T.J. Davidson | PERS-S75-025 | « Tony Davidson » / « T. J. Davidson » (studio/label TJM) — `PERS-S75-025` + `PERS-S76-051` = paire `same_as`. |
| Tony Davidson / T. J. Davidson | PERS-S76-051 | « Tony Davidson » / « T. J. Davidson » (studio/label TJM) — `PERS-S75-025` + `PERS-S76-051` = paire `same_as`. |
| Eddie Garrity / Ed Banger | PERS-S76-040 | « Eddie Garrity » / « Ed Banger » (Ed Banger & the Nosebleeds) — deux formes déjà dans un seul id ; conserver en `alt_names`. |

**Bernard Sumner** : l'alias de scène « Bernard Albrecht » (var. « Bernard Dicken ») n'apparaît dans **aucune** entrée `PERS-*` ; à enregistrer en `alt_names` du futur `PERSON-` Sumner, sans créer d'identifiant concurrent.

## 4. Erreurs de typage — à renvoyer vers l'étape 10

### 4.1. Entités collectives → candidats `ORG-`

Typage **par nature du référent**, ligne par ligne (et non par rôle). Seules les entités collectives subsistent ici.

| Identifiant | Chaîne | Source | Nature du référent | Justification | Renvoi |
|-------------|--------|--------|--------------------|---------------|--------|
| PERS-016 | Bedhead |  | collectif | groupe musical (réception différée : Codeine, Bedhead, Interpol) | `ORG-` |
| PERS-S76-052 | Oz PA / Eddy et Oz | S76 | collectif_mixte | équipe de sonorisation « Oz PA » (entité) ; « Eddy » et « Oz » sont des individus à éclater en PERSON- distincts | `ORG-` (+ split PERSON-) |
| PERS-S76-068 | Buzzcocks | S76 | collectif | groupe musical (Buzzcocks) | `ORG-` |
| PERS-S76-071 | Minny Pops | S76 | collectif | groupe musical néerlandais (Minny Pops) | `ORG-` |
| PERS-S76-082 | Perry Boys | S76 | collectif | sous-culture juvénile mancunienne (Perry Boys) — pas un groupe ; → ORG-/concept de scène | `ORG-` |

**Réconciliation 13 vs 14 → 5.** La version initiale de la PR utilisait un filtre fondé sur le *rôle* (« manager », « fanzine », « groupe » dans la description), produisant 30 lignes brutes / 13–14 référents et de nombreux faux positifs. Après application de la règle « nature du référent », il reste **5 entités collectives**. Le chiffre juste est ce décompte après retrait des faux positifs ; il est désormais identique dans le tableau §7 et la recommandation §7.3.

**Cas signalés par Codex — individus reclassés `PERSON-` (réintégrés, non fusionnés) :**

| Identifiant | Chaîne | Pourquoi PERSON- | Réintégration | Statut |
|-------------|--------|------------------|---------------|:------:|
| PERS-S31-005 | Tony Wilson | fondateur Factory — individu | grappe Tony Wilson (§2.1) | `fusion_evidente` |
| PERS-S31-007 | Rob Gretton | manager — individu | grappe Rob Gretton (§2.1) | `fusion_evidente` |
| PERS-S34-011 | Martin Hannett | producteur — individu | grappe Martin Hannett (§2.1) | `fusion_evidente` |
| PERS-S75-024 | Alan Erasmus | cofondateur Factory — individu | grappe Alan Erasmus (§2.2) | `fusion_evidente` |
| PERS-S75-025 | T.J. Davidson | propriétaire de studio — individu | variante Davidson (§3.2) | `a_arbitrer` |
| PERS-S76-011 | Mark Reeder | disquaire / ami — individu | grappe Mark Reeder (§2.2) | `fusion_evidente` |
| PERS-S76-018 | Steve Burke / Steve Shy | fanzine Shy Talk — individu | entrée unique (§1.2) | `distinct` |
| PERS-S76-021 | Steve Morris | batteur de JD — individu ; variante de « Stephen Morris » | grappe Stephen Morris | `a_arbitrer` |
| PERS-S76-027 | Rob Gretton | fanzine Manchester Rains — individu | grappe Rob Gretton (§2.1) | `fusion_evidente` |
| PERS-S76-040 | Eddie Garrity / Ed Banger | chanteur — individu | variante Garrity (§3.2) | `a_arbitrer` |
| PERS-S76-042 | Jeremy Kerr | membre d'A Certain Ratio — individu | entrée unique (§1.2) | `distinct` |
| PERS-S76-045 | Alan Erasmus | cofondateur Factory — individu | grappe Alan Erasmus (§2.2) | `fusion_evidente` |
| PERS-S76-048 | Roger Eagle | DJ / promoteur — individu | entrée unique (§1.2) | `distinct` |
| PERS-S76-051 | Tony Davidson / T. J. Davidson | entrepreneur — individu | variante Davidson (§3.2) | `a_arbitrer` |
| PERS-S76-064 | Dave Pils et Jasmine | deux individus (hébergement londonien) | à éclater en PERSON- distincts | `a_arbitrer` |
| PERS-S77-002 | Mark Perry / Mark P | fondateur de Sniffin' Glue — individu | entrée unique (§1.2) | `distinct` |
| PERS-S77-004 | Tony Drayton / Tony D / Tony Puppy | éditeur de fanzine — individu | entrée unique (§1.2) | `distinct` |
| PERS-S78-005 | Tony Wilson | fondateur Factory — individu | grappe Tony Wilson (§2.1) | `fusion_evidente` |
| PERS-S85-004 | David Haslam | DJ / auteur fanzine Debris — individu | entrée unique (§1.2) | `distinct` |

Cas particuliers : **« Oz PA / Eddy et Oz » (`PERS-S76-052`)** mêle une entité (Oz PA, équipe de sono → `ORG-`) et deux individus (Eddy, Oz → `PERSON-`) : à éclater. **« Perry Boys » (`PERS-S76-082`)** est une **sous-culture** juvénile, pas un groupe musical : renvoi `ORG-`/concept de scène, jamais `PERSON-`. **« Dave Pils et Jasmine » (`PERS-S76-064`)** sont deux individus (et non une entité) : restent `PERSON-`, à scinder, `a_arbitrer`.

### 4.2. Figures d'influence (littéraires / philosophiques) → registre concept ou influence

Détection **par nom** (patronymes d'auteurs externes), ce qui exclut automatiquement Ian Curtis et les acteurs du corpus. Ce ne sont pas des acteurs de Joy Division mais des **influences citées**.

| Identifiant | Chaîne | Source | Description | Renvoi |
|-------------|--------|--------|-------------|--------|
| PERS-S53-010 | Friedrich Nietzsche | S53 | Référence philosophique sur musique, puissance et tragique, mobilisée par La Rocca. | influence — à arbitrer |
| PERS-S54-004 | J. G. Ballard | S54 | Matrice littéraire centrale pour Exercise One, Atrocity Exhibition, corps technologique et | influence — à arbitrer |
| PERS-S75-031 | Marcel Proust | S75 | écrivain; référence possible pour le titre Unknown Pleasures | influence — à arbitrer |
| PERS-S29-012 | Nikolai Gogol | S29 | Référence littéraire attachée au titre « Dead Souls » ; chez Goddard, la chanson n’est pas | influence — à arbitrer |
| PERS-S77-009 | Penny Rimbaud | S77 | Membre de Crass, associé à l’International Anthem et à la formulation d’un anarcho-punk ar | influence — à arbitrer |
| PERS-S54-003 | William S. Burroughs | S54 | Matrice littéraire centrale pour Interzone, Digital, langage-virus, contrôle et fragmentat | influence — à arbitrer |
| PERS-S56-004 | William S. Burroughs | S56 | Auteur admiré par Curtis ; figure de l’anecdote du Plan K. | influence — à arbitrer |
| PERS-S75-033 | William S. Burroughs | S75 | écrivain; figure d'admiration pour Ian Curtis | influence — à arbitrer |

Décompte recalculé : **6 figures distinctes** pour **8 identifiants**. Doublons internes à résorber : **William S. Burroughs** (3 ids : PERS-S54-003, PERS-S56-004, PERS-S75-033). Renvoi à l'étape 10 : registre `INFLUENCE-`/concept, ou `PERSON-` de type *influence_citée* explicitement distinct des acteurs. Ian Curtis lu « comme écrivain » (`PERS-S54-002`, `PERS-S56-002`) **n'est pas** une influence externe : ces entrées restent dans la grappe Ian Curtis (§1–§2).

## 5. Locuteurs « anonyme » (607)

Sur 962 citations : **355** locuteur nommé, **607** « anonyme » / vide. Partition (confirmée sur `quotes.json`) :

| Sous-ensemble | Définition | Volume |
|---------------|------------|:------:|
| (a) Narration d'auteur | « anonyme » **mais** `auteur_source` renseigné — locuteur réel = auteur de la source, à relier à un `PERSON-` auteur | **607** |
| (b) Locuteur réellement inconnu | « anonyme » **sans** `auteur_source` | **0** |
| **Total** | | **607** |

La totalité des 607 citations « anonyme » relève du cas (a) : **aucune** n'est dépourvue d'`auteur_source`. Il n'existe donc **aucun locuteur réellement inconnu** à laisser non rattaché.

### 5.1. Cas (a) — ventilation par `auteur_source`

| `auteur_source` (→ futur `PERSON-` auteur) | Nb de citations |
|--------------------------------------------|:---------------:|
| Peter Hook | 223 |
| Deborah Curtis | 103 |
| Claude Flowers | 20 |
| Alessandro Gnocchi | 15 |
| Fabio La Rocca | 15 |
| Mike West | 15 |
| Jon Savage | 14 |
| Leonard Nevarez | 14 |
| Andrea Rabbito | 12 |
| Alfredo Suatoni | 11 |
| Simon Reynolds | 11 |
| Matthew Worley | 10 |
| Uwe Schütte | 10 |
| Emiliano Ilardi | 8 |
| Mick Middles ; Lindsay Reade | 8 |
| Paul Morley | 8 |
| Dan Jacobson, Ian Jeffrey | 7 |
| Linda Barone | 7 |
| Sara Martínez | 7 |
| Vincenzo Romania | 7 |
| Alastair Greig ; Catherine Strong | 6 |
| Francesca Ferrara | 6 |
| Giuseppe Allegri | 6 |
| Massimo Villani | 6 |
| Raffaele Federici | 6 |
| David Wilkinson | 5 |
| Giacomo Bottà | 5 |
| Mark Johnson ; David Lees ; Paul Morley ; Jon Wozencroft | 5 |
| Caterina Tomeo | 4 |
| Daniele De Luca | 4 |
| Jennifer Malvezzi | 4 |
| Manchester Digital Music Archive | 4 |
| Paolo Bertetti ; Domenico Morreale | 4 |
| Giada Iovane ; Giovanni Maria Riccio | 3 |
| HM Treasury | 3 |
| Loïc Riom | 3 |
| Manolo Farci | 3 |
| Marco Broll | 3 |
| Happy Mondays | 1 |
| Kevin Cummins | 1 |

### 5.2. Liste exhaustive des citations du cas (a)

```
CIT-S13-001, CIT-S13-002, CIT-S13-003, CIT-S13-004, CIT-S61-001, CIT-S61-002, CIT-S61-003, CIT-S63-001, CIT-S63-002, CIT-S63-003
CIT-S63-004, CIT-S63-005, CIT-S63-006, CIT-S63-007, CIT-S64-001, CIT-S64-002, CIT-S64-003, CIT-S64-004, CIT-S64-005, CIT-S65-001
CIT-S65-002, CIT-S65-003, CIT-S65-004, CIT-S65-005, CIT-S65-006, CIT-S65-007, CIT-S66-001, CIT-S66-002, CIT-S66-003, CIT-S66-004
CIT-S66-005, CIT-S66-006, CIT-S66-007, CIT-S66-008, CIT-S66-009, CIT-S66-010, S09-Q001, S11-Q001, S11-Q002, S11-Q003
S14-Q001, S15-Q001, S15-Q002, S15-Q003, S15-Q004, S21-Q001, S21-Q002, S21-Q003, S21-Q004, S22-Q001
S22-Q002, S22-Q003, S22-Q004, S22-Q005, S27-Q001, S27-Q002, S27-Q003, S31-Q001, S31-Q002, S31-Q003
S31-Q004, S31-Q005, S31-Q006, S37-CIT-001, S37-CIT-002, S37-CIT-003, S37-CIT-004, S37-CIT-005, S37-CIT-006, S37-CIT-007
S37-CIT-008, S41-Q010, S41-Q011, S41-Q012, S41-Q013, S41-Q014, S41-Q015, S41-Q016, S41-Q017, S41-Q018
S41-Q019, S41-Q020, S41-Q021, S41-Q022, S41-Q023, S41-Q024, S41-Q025, S41-Q026, S41-Q027, S41-Q028
S41-Q029, S41-Q030, S41-Q031, S41-Q032, S41-Q033, S41-Q034, S41-Q035, S41-Q036, S41-Q037, S41-Q038
S41-Q039, S41-Q040, S41-Q041, S41-Q042, S41-Q043, S41-Q044, S41-Q045, S41-Q046, S41-Q047, S41-Q048
S41-Q049, S41-Q050, S41-Q051, S41-Q052, S41-Q053, S41-Q054, S41-Q055, S41-Q056, S41-Q057, S41-Q058
S41-Q059, S41-Q060, S41-Q061, S41-Q062, S41-Q063, S41-Q064, S41-Q065, S41-Q066, S41-Q067, S41-Q068
S41-Q069, S41-Q070, S41-Q071, S41-Q072, S41-Q073, S41-Q074, S41-Q075, S41-Q076, S41-Q077, S41-Q078
S41-Q079, S41-Q080, S41-Q081, S41-Q082, S41-Q083, S41-Q084, S41-Q085, S41-Q086, S41-Q087, S41-Q088
S41-Q089, S41-Q090, S41-Q091, S41-Q092, S41-Q093, S41-Q094, S41-Q095, S41-Q096, S41-Q097, S41-Q098
S41-Q099, S41-Q100, S41-Q101, S41-Q102, S41-Q103, S41-Q104, S41-Q105, S41-Q106, S41-Q107, S41-Q108
S41-Q109, S41-Q110, S41-Q111, S41-Q112, S41-Q113, S41-Q114, S41-Q115, S41-Q116, S41-Q117, S41-Q118
S41-Q119, S41-Q120, S41-Q121, S41-Q122, S41-Q123, S41-Q124, S41-Q125, S41-Q126, S41-Q127, S41-Q128
S41-Q129, S41-Q130, S41-Q131, S41-Q132, S41-Q133, S41-Q134, S41-Q135, S41-Q136, S41-Q137, S41-Q138
S41-Q139, S41-Q140, S41-Q141, S41-Q142, S41-Q143, S41-Q144, S41-Q145, S41-Q146, S41-Q147, S41-Q148
S41-Q149, S41-Q150, S41-Q151, S41-Q152, S41-Q153, S41-Q154, S41-Q155, S41-Q156, S41-Q157, S41-Q158
S41-Q159, S41-Q160, S41-Q161, S41-Q162, S41-Q163, S41-Q164, S41-Q165, S41-Q166, S41-Q167, S41-Q168
S41-Q169, S41-Q170, S41-Q171, S41-Q172, S41-Q173, S41-Q174, S41-Q175, S41-Q176, S41-Q177, S41-Q178
S41-Q179, S41-Q180, S41-Q181, S41-Q182, S41-Q183, S41-Q184, S41-Q185, S41-Q186, S41-Q187, S41-Q188
S41-Q189, S41-Q190, S41-Q191, S41-Q192, S41-Q193, S41-Q194, S41-Q195, S41-Q196, S41-Q197, S41-Q198
S41-Q199, S41-Q200, S41-Q201, S41-Q202, S41-Q203, S41-Q204, S41-Q205, S41-Q206, S41-Q207, S41-Q208
S41-Q209, S41-Q210, S41-Q211, S41-Q212, S41-Q213, S41-Q214, S41-Q215, S41-Q216, S41-Q217, S41-Q218
S41-Q219, S41-Q220, S41-Q221, S41-Q222, S41-Q223, S41-Q224, S41-Q225, S41-Q226, S41-Q227, S41-Q228
S41-Q229, S41-Q230, S41-Q231, S41-Q232, S45-Q006, S45-Q007, S45-Q008, S45-Q009, S45-Q010, S45-Q011
S45-Q012, S45-Q013, S45-Q014, S45-Q015, S45-Q016, S45-Q017, S45-Q018, S45-Q019, S45-Q020, S45-Q021
S45-Q022, S45-Q023, S45-Q024, S45-Q025, S45-Q026, S45-Q027, S45-Q028, S45-Q029, S45-Q030, S45-Q031
S45-Q032, S45-Q033, S45-Q034, S45-Q035, S45-Q036, S45-Q037, S45-Q038, S45-Q039, S45-Q040, S45-Q041
S45-Q042, S45-Q043, S45-Q044, S45-Q045, S45-Q046, S45-Q047, S45-Q048, S45-Q049, S45-Q050, S45-Q051
S45-Q052, S45-Q053, S45-Q054, S45-Q055, S45-Q056, S45-Q057, S45-Q058, S45-Q059, S45-Q060, S45-Q061
S45-Q062, S45-Q063, S45-Q064, S45-Q065, S45-Q066, S45-Q067, S45-Q068, S45-Q069, S45-Q070, S45-Q071
S45-Q072, S45-Q073, S45-Q074, S45-Q075, S45-Q076, S45-Q077, S45-Q078, S45-Q079, S45-Q080, S45-Q081
S45-Q082, S45-Q083, S45-Q084, S45-Q085, S45-Q086, S45-Q087, S45-Q088, S45-Q089, S45-Q090, S45-Q091
S45-Q092, S45-Q093, S45-Q094, S45-Q095, S45-Q096, S45-Q097, S45-Q098, S45-Q099, S45-Q100, S45-Q101
S45-Q102, S45-Q103, S45-Q104, S45-Q105, S45-Q106, S45-Q107, S45-Q108, S46-Q001, S46-Q002, S46-Q003
S46-Q004, S46-Q005, S47-Q001, S47-Q002, S47-Q003, S47-Q004, S47-Q005, S47-Q006, S47-Q007, S47-Q008
S47-Q009, S47-Q010, S47-Q011, S47-Q012, S47-Q013, S47-Q014, S47-Q015, S49-Q001, S49-Q002, S49-Q003
S50-Q001, S50-Q002, S50-Q003, S50-Q004, S51-Q001, S51-Q002, S51-Q003, S51-Q004, S52-Q001, S52-Q002
S52-Q003, S52-Q004, S52-Q005, S52-Q006, S52-Q007, S52-Q008, S52-Q009, S52-Q010, S52-Q011, S52-Q012
S53-Q001, S53-Q002, S53-Q003, S53-Q004, S53-Q005, S53-Q006, S53-Q007, S53-Q008, S53-Q009, S53-Q010
S53-Q011, S53-Q012, S53-Q013, S53-Q014, S53-Q015, S54-Q001, S54-Q002, S54-Q003, S54-Q004, S54-Q005
S54-Q006, S54-Q007, S54-Q008, S54-Q009, S54-Q010, S54-Q011, S54-Q012, S54-Q013, S54-Q014, S54-Q015
S55-Q001, S55-Q002, S55-Q003, S55-Q004, S55-Q005, S55-Q006, S55-Q007, S56-Q001, S56-Q002, S56-Q003
S56-Q004, S56-Q005, S56-Q006, S56-Q007, S57-Q001, S57-Q002, S57-Q003, S57-Q004, S57-Q005, S57-Q006
S58-Q001, S58-Q002, S58-Q003, S58-Q004, S58-Q005, S58-Q006, S58-Q007, S58-Q008, S59-Q001, S59-Q002
S59-Q003, S59-Q004, S59-Q005, S59-Q006, S60-Q001, S60-Q002, S60-Q003, S60-Q004, S60-Q005, S60-Q006
S68-Q001, S68-Q002, S68-Q003, S69-Q001, S69-Q002, S69-Q003, S69-Q004, S69-Q005, S69-Q006, S70-Q001
S70-Q002, S70-Q003, S70-Q004, S70-Q005, S70-Q006, S70-Q007, S70-Q008, S70-Q009, S70-Q010, S70-Q011
S71-Q001, S71-Q002, S71-Q003, S71-Q004, S71-Q005, S71-Q006, S71-Q007, S71-Q008, S71-Q009, S71-Q010
S71-Q011, S71-Q012, S71-Q013, S71-Q014, S71-Q015, S71-Q016, S71-Q017, S71-Q018, S71-Q019, S71-Q020
S72-Q001, S72-Q002, S72-Q003, S72-Q004, S72-Q005, S72-Q006, S72-Q007, S72-Q008, S72-Q009, S72-Q010
S72-Q011, S76-Q020, S76-Q079, S76-Q131, S76-Q163, S76-Q169, S76-Q181, S76-Q189, S76-Q190, S77-Q001
S77-Q002, S77-Q003, S77-Q004, S77-Q005, S77-Q006, S77-Q007, S77-Q008, S77-Q009, S77-Q010, S78-Q001
S78-Q002, S78-Q003, S78-Q004, S78-Q005, S78-Q006, S78-Q007, S78-Q008, S78-Q009, S78-Q010, S78-Q011
S78-Q012, S78-Q013, S78-Q014, S89-Q001, S89-Q002, S89-Q003, S89-Q004, S89-Q005, S89-Q006, S89-Q007
S89-Q008, S89-Q009, S89-Q010, S89-Q011, S89-Q012, S89-Q013, S89-Q014
```

## 6. Résidus à récurer — les 9 `attribution_a_arbitrer`

| Citation | Source | `locuteur` | `auteur_source` | `rapporteur` | Hypothèse de résolution |
|----------|--------|-----------|-----------------|--------------|-------------------------|
| S76-Q020 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q079 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q116 | S76 | Ian Curtis | Mick Middles ; Lindsay Reade | entretien McCullough | Citation rapportée : locuteur « Ian Curtis » transmis par Mick Middles ; Lindsay Reade via entretien McCullough. |
| S76-Q131 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q163 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q169 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q181 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q189 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |
| S76-Q190 | S76 | anonyme | Mick Middles ; Lindsay Reade | — | Narration d'auteur : rattacher au `auteur_source` (Mick Middles ; Lindsay Reade) ; verser en 5a. |

Les neuf cas relèvent de *Torn Apart* (Middles & Reade, S76) : huit sont des passages narratifs (locuteur = binôme d'auteurs) ; `S76-Q116` est une parole de Ian Curtis transmise via un entretien McCullough (citation rapportée à deux niveaux).

## 7. Synthèse chiffrée et recommandations

| Indicateur | Valeur |
|------------|:------:|
| Entrées `PERS-*` distinctes | 305 |
| Chaînes-noms distinctes | 175 |
| Grappes multi-identifiants (≥ 2 id) | 45 |
| Liens `same_as` à câbler | 130 |
| Entrées en grappes / à identifiant unique | 175 / 130 |
| Entités collectives → `ORG-` | 5 entrées / 5 noms |
| Figures d'influence → influence/concept | 8 entrées / 6 noms |
| **Personnes canoniques `PERSON-` pressenties** (175 noms − 5 ORG − 6 influences) | **≈ 164** |
| Citations narration d'auteur (5a) | 607 |
| Citations locuteur inconnu (5b) | 0 |
| Citations `attribution_a_arbitrer` | 9 |

### Recommandations (non exécutées ici)

1. Câbler les `same_as` des grappes `fusion_evidente` (§2) vers un `PERSON-` unique ; formes secondaires en `alt_names`.
2. Traiter `John Anderson`, « Steve Morris » et tout nom générique en `a_arbitrer` : contrôle source avant fusion.
3. Sortir les **5** entités collectives (§4.1) vers `ORG-` et les **6** figures d'influence (§4.2) vers un registre influence/concept ; résorber les doublons internes (Burroughs).
4. Maintenir `Kevin Curtis` (`PERS-S76-003`) **distinct** de `PERS-001`.
5. Ajouter l'alias « Bernard Albrecht » au futur `PERSON-` Sumner ; confirmer les paires Davidson et Garrity ; éclater « Oz PA / Eddy et Oz » et « Dave Pils et Jasmine ».
6. Relier les **607** citations de narration d'auteur (§5) aux `PERSON-` auteurs une fois canonisés ; **aucun** locuteur réellement inconnu n'est à laisser non rattaché (cas 5b = 0).
7. Résoudre les 9 `attribution_a_arbitrer` selon les hypothèses du §6.

---

## 8. Lien de la PR

Pull request : **[https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/46](https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/46)** (branche `claude/etape9-audit-personnes-13y69` → `main`).

