# Tableau de bord des atomisations

> Régénéré le **26 mai 2026** depuis `data/registre.json`, `exports/generated/audit_repo.json` et `registers/`.  
> État vérifié : 0 erreur bloquante · 2 716 atomes · 7 292 enregistrements · 89 sources déclarées.

---

## Synthèse générale

| Indicateur | Valeur |
|---|---:|
| Total sources déclarées | **89** |
| Sources avec atomes | **70** |
| Total atomes dans le corpus | **2 716** |
| Total enregistrements (toutes types) | **7 292** |
| Erreurs bloquantes (audit) | **0** ✅ |
| Avertissements (audit) | 31 249 |
| Dette migration v2 (atomes incomplets) | 2 643 / 2 716 |

### Répartition des enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 2 716 |
| chronology | 476 |
| concept | 456 |
| metadata | 264 |
| motif | 424 |
| myth | 101 |
| person | 305 |
| quote | 539 |
| song | 110 |
| source | 114 |
| template | 360 |
| unknown | 1 425 |
| autres | 103 |

### Répartition des sources par statut (registre.json)

| Statut | Nb sources |
|---|---:|
| ✅ `atomisee` | 27 |
| 🔄 `2e_passe` / seconde passe | 2 |
| 🟢 `verifie` | 20 |
| 📌 `fixee` / autre | 30 |
| 🟡 `a_consolider` | 11 |
| 🔵 Référence interne | 1 |
| **Total** | **89** (+ REGISTRY) |

---

## Tableau principal

_Colonnes : ID · Auteur · Titre abrégé · Statut registre · Pages couvertes · Chapitres v2 · Atomes · Cit. · Act. · Conc. · Chans. · Couverture_

| ID | Auteur | Titre abrégé | Statut | Pages atomisées | Chap. v2 | At. | Cit. | Act. | Conc. | Ch. | Couverture |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|
| S01 | Blakeley | The Regeneration of East Manchester | 🟢 Vérifié | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S02 | Sénat | Villes du futur, futur des villes | 🟢 Vérifié | — | — | 11 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S03 | Demographia | England Largest Cities | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S04 | Kidd | Manchester: A History | 🟢 Vérifié | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S05 | Jeffery | Policing and the Reproduction of Locality | 🟢 Vérifié | 1–18, 20–23 | — | 14 | 0 | 0 | 1 | 0 | 🟡 Partielle ⚠️ _Manque pp. 118–128_ |
| S06 | Carter | Youth, race and the inner-city estate | 🟢 Vérifié | 248–263 | — | 13 | 0 | 0 | 0 | 0 | ✅ Complète |
| S07 | Engels | The Condition of the Working Class | 📌 Fixée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S08 | I.S. | Internationale situationniste, n° 2 | 📌 Fixée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S09 | Cummins | Joy Division (photo) | 🟢 Vérifié | — | — | 11 | 0 | 0 | 5 | 0 | 🔵 Partielle (pag. NR) |
| S10 | Sumner | Chapter and Verse | 🟢 Vérifié | 7, 11–15, 23–41, 52–110 | — | 40 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S11 | Treasury | Budget Report 1987–88 | 🟢 Vérifié | 1–67 | — | 11 | 0 | 0 | 5 | 0 | 🔵 Partielle (pag. NR) |
| S12 | Times | Bundle AIDS / Anderton 1986 | 🟢 Vérifié | — | — | 9 | 0 | 0 | 1 | 0 | 🔵 Partielle (pag. NR) |
| S13 | Tomeo | Dance Dance Dance! L'Interzone | 🟢 Vérifié | — | — | 11 | 0 | 0 | 1 | 0 | 🔵 Partielle (pag. NR) |
| S14 | Mondays | God's Cop | 🟢 Vérifié | — | — | 9 | 0 | 0 | 4 | 0 | 🔵 Partielle (pag. NR) |
| S15 | De Luca | The Sound and the Fury | ✅ Atomisé | 54–63 | — | 15 | 5 | 0 | 8 | 0 | 🔵 Partielle (pag. NR) |
| S16 | Songfacts | Boredom by Buzzcocks | 📌 Fixée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S17 | Contrib. | Rowche Rumble (Wikipedia) | 📌 Fixée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S18 | Fédida | Manchester : L'éveil d'une scène | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S19 | Bourdieu | Les trois états du capital culturel | 📌 Fixée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S20 | Dodge | Mapping Manchester's housing | 🟡 À consolider | 19–36 | — | 15 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S21 | MDMArchive | City Fun: The Hidden History | 📌 Fixée | — | — | 10 | 4 | 7 | 5 | 2 | 🔵 Partielle (pag. NR) |
| S22 | Wilkinson | City Fun and the politics of post-punk | 🟢 Vérifié | 91–109 | — | 16 | 0 | 0 | 9 | 0 | 🔵 Partielle (pag. NR) |
| S23 | Press | Rochdale Alternative Press / RAP | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S24 | Boon | New Hormones / Spiral Scratch EP | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S25 | Factory | Factory Records : philosophie | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S26 | Butt | Post-Punk Then and Now | 🟢 Vérifié | 5–95 | — | 18 | 0 | 0 | 10 | 0 | 🔵 Partielle (pag. NR) |
| S27 | Riom | Compte rendu Crossley | 🟢 Vérifié | 223–225 | — | 11 | 0 | 0 | 6 | 0 | ✅ Complète |
| S28 | Granada | So It Goes | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S29 | Goddard | Missions of Dead Souls | 🟢 Vérifié | 34–47 | — | 23 | 5 | 12 | 4 | 5 | 🟡 Partielle ⚠️ _Manque pp. 3–16_ |
| S30 | Frith | Sound Effects | 🟢 Vérifié | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S31 | Allegri | Living in the Ice Age | 📌 Fixée | — | — | 15 | 6 | 8 | 10 | 3 | 🔵 Partielle (pag. NR) |
| S32 | Kraftwerk | Trans-Europe Express / Radio-Activity | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S33 | Can | Tago Mago | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S34 | Fraser | Manchester, 1976 | 🟢 Vérifié | — | — | 12 | 6 | 12 | 3 | 7 | 🟡 Partielle ⚠️ _Manque pp. 139–154_ |
| S35 | Morris | Record Play Pause | 📌 Fixée | 1–358 | — | 90 | 0 | 0 | 24 | 0 | 🔵 Partielle (pag. NR) |
| S36 | Crosthwaite | Trauma and Degeneration | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S38 | Saville | Pulsebeat of Manchester | 🟡 À consolider | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S39 | Bauman | Liquid Modernity | 🟢 Vérifié | — | — | 8 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S40 | Cacciatore | …waiting for something to happen | 🟢 Vérifié | — | — | 9 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S41 | Hook | Unknown Pleasures | ✅ Atomisé | 10–297 (sélectif) | — | 430 | 9 | 9 | 0 | 7 | 🔵 Partielle (pag. NR) |
| S42 | Troianiello | Metropoli e spazio periferico | 📌 Fixée | — | — | 13 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S43 | Capozzi | The weight on their shoulders | 📌 Fixée | 64–75 | — | 15 | 0 | 0 | 5 | 0 | 🔵 Partielle (pag. NR) |
| S44 | Guarino | I Joy Division tra vomito culturale | 📌 Fixée | 76–92 | — | 16 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S45 | Curtis D. | Touching from a Distance | ✅ Atomisé | 17–218 (sélectif) | — | 205 | 56 | 37 | 0 | 5 | 🔵 Partielle (pag. NR) |
| S46 | Johnson | An Ideal for Living | ✅ Atomisé | 2–122 (sélectif) | — | 190 | 5 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S47 | West | Joy Division | 🟡 Consolidée | — | — | 200 | 15 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S48 | De Sia | Il segno, la grafica, la visione | 📌 Fixée | 94–98 | — | 13 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S49 | Farci | Here are the Young Men | 📌 Fixée | — | — | 17 | 3 | 3 | 3 | 3 | 🔵 Partielle (pag. NR) |
| S50 | Bertetti | Reimmaginare l'immaginario | 📌 Fixée | — | — | 19 | 4 | 5 | 5 | 4 | 🔵 Partielle (pag. NR) |
| S51 | Malvezzi | Dream English Kid 1978–1980 | 📌 Fixée | — | — | 15 | 4 | 4 | 5 | 2 | 🔵 Partielle (pag. NR) |
| S52 | Rabbito | Control e l'infrangimento del vetro | 📌 Fixée | — | — | 20 | 12 | 12 | 6 | 4 | 🔵 Partielle (pag. NR) |
| S53 | La Rocca | Immagini e simboli | 📌 Fixée | — | — | 16 | 15 | 11 | 7 | 2 | 🔵 Partielle (pag. NR) |
| S54 | Gnocchi | Interzona. Burroughs e Ballard | 📌 Fixée | — | — | 15 | 15 | 9 | 8 | 6 | 🔵 Partielle (pag. NR) |
| S55 | Romania | A guide to come | 📌 Fixée | — | — | 12 | 7 | 5 | 8 | 1 | 🔵 Partielle (pag. NR) |
| S56 | Barone | Directionless so plain to see | 📌 Fixée | — | — | 21 | 7 | 4 | 11 | 3 | 🔵 Partielle (pag. NR) |
| S57 | Villani | Ti sfido a disperarti | 📌 Fixée | — | — | 15 | 6 | 4 | 10 | 4 | 🔵 Partielle (pag. NR) |
| S58 | Ilardi | Ian Curtis is not dead | 📌 Fixée | — | — | 15 | 8 | 6 | 13 | 4 | 🔵 Partielle (pag. NR) |
| S59 | Ferrara | Joy Division: una poetica della distanza | 📌 Fixée | — | — | 15 | 6 | 5 | 10 | 5 | 🔵 Partielle (pag. NR) |
| S60 | Federici | Unknown Pleasures: Pulsar di una t-shirt | 📌 Fixée | — | — | 15 | 6 | 5 | 15 | 2 | 🔵 Partielle (pag. NR) |
| S61 | Iovane | Trademark will tear us apart again | 📌 Fixée | 287–307 | — | 16 | 0 | 0 | 1 | 2 | 🔵 Partielle (pag. NR) |
| S68 | Broll | Joy Division (1988) | ✅ Atomisé | 1–3 | — | 39 | 3 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S69 | Greig | But We Remember When We Were Young | ✅ Atomisé | 2–13 | — | 36 | 6 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S70 | Suatoni | Dal cuore della città | ✅ Atomisé | 1–12 | — | 40 | 11 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S71 | Flowers | Dreams Never End | 🔄 2e passe | 8–224 (sélectif) | — | 75 | 20 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S72 | Reynolds | Rip It Up and Start Again | 🔄 2e passe | 7–440 (sélectif) | — | 61 | 11 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S73 | Orchids | Référence historique à consolider | 🔵 Déplacée | — | — | 0 | 0 | 0 | 0 | 0 | ⭕ Non démarrée |
| S74 | Middles | From Joy Division to New Order | ✅ Atomisé | — | — | 61 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S75 | Ott | Joy Division's Unknown Pleasures | ✅ Atomisé | — | — | 75 | 21 | 27 | 0 | 33 | 🔵 Partielle (pag. NR) |
| S76 | Middles | Torn Apart: The Life of Ian Curtis | ✅ Atomisé | — | — | 229 | 195 | 89 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S77 | Worley | Punk, Politics and British (fan)zines | 📌 Fixée | — | — | 16 | 10 | 10 | 8 | 3 | 🔵 Partielle (pag. NR) |
| S78 | Nevarez | How Joy Division Came to Sound Like Manchester | 📌 Fixée | — | — | 20 | 14 | 10 | 9 | 4 | 🔵 Partielle (pag. NR) |
| S37 | Morley | Joy Division: Piece by Piece | 📌 Fixée | 21–52 (sélectif) | — | 78 | 11 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |
| S79 | Curtis/Savage | So This Is Permanence | 🟢 Vérifié | 2–101 (sélectif) | — | 133 | 0 | 0 | 0 | 0 | 🔵 Partielle (pag. NR) |

---

## Sources Heart & Soul (S62–S88) — état détaillé

_Volume Heart & Soul (H&S) : Power, Devereux, Dillane (dir.), Rowman & Littlefield, 2018. PDF partagé. Offset pagination : pages_pdf = pages_livre + 31._

| ID | Auteur | Titre abrégé | Pages livre | Pages PDF | At. | Cit. | Act. | Conc. | Chap. couverts | Couverture |
|---|---|---|---|---|---:|---:|---:|---:|---|---|
| S62 | Power et al. | Introduction H&S | xvii–xxx | 48–61 | 9 | 0 | 0 | 2 | 14 | ✅ Complète (citations section absente) |
| S63 | Jacobson & Jeffrey | Tony Wilson's Bloody Contract | p. 17–32 | 48–63 | 11 | 0 | 0 | 3 | 2, 3, 12, 14 | ✅ Complète |
| S64 | Bottà | European Imaginary of Joy Division | p. 33–46 | 64–77 | 8 | 0 | 0 | 3 | 1, 4, 14 | 🟡 Partielle (85%) ⚠️ _Manque pp. 45–46_ |
| S65 | Martínez | Literary Influences on Joy Division | p. 47–62 | 78–93 | 8 | 0 | 0 | 3 | 3, 4, 6, 11, 14 | 🟡 Partielle (87%) ⚠️ _Manque pp. 50, 62_ |
| S66 | Schütte | On Ian Curtis's Lyrics | p. 63–80 | 94–111 | 8 | 0 | 0 | 5 | 1, 2, 4, 6, 7, 11, 14 | 🟡 Partielle (88%) ⚠️ _Manque pp. 79–80_ |
| S67 | Naiman | Illness and Temporal Exile | p. 83–98 | 114–129 | 9 | 0 | 0 | 3 | 3, 4, 12, 14 | 🟡 Partielle (81%) ⚠️ _Manque pp. 96–98_ |
| S80 | Valdés Miyares | Communication Breakdown / Transmission | p. 99–114 | 130–145 | 8 | 0 | 0 | 5 | 3, 4, 6, 12, 14 | 🟡 Partielle (68%) ⚠️ _Manque pp. 110–114_ |
| S81 | Devereux et al. | Revisiting Ian Curtis's Suicide | p. 115–130 | 146–161 | 9 | 0 | 0 | 6 | 12, 14 | 🟡 Partielle (87%) ⚠️ _Manque pp. 129–130_ |
| S82 | Parmar | Joy Division in Space | p. 133–154 | 164–185 | 9 | 0 | 0 | 5 | 3, 4, 5, 6, 13, 14 | 🟡 Partielle (86%) ⚠️ _Manque pp. 135, 153–154_ |
| S83 | Greenwood & Tarpey | Hannett's Pungent Architecture | p. 155–170 | 186–201 | 12 | 0 | 0 | 4 | 1, 3, 5, 6 | 🟡 Partielle (75%) ⚠️ _Manque pp. 160, 168–170_ |
| S84 | Cope | Moving Image Record (Factory Video) | p. 171–192 | 202–223 | 23 | 5 | 8 | 4 | 1, 2, 3, 5, 6, 8, 9, 10, 14 | 🟡 Partielle (77%) ⚠️ _Manque pp. 183–184, 190–192_ |
| S85 | Malcolm | Mining for Counterculture | p. 195–208 | 226–239 | 13 | 8 ✅ | 8 | 4 | 1, 2, 5, 8, 10, 13, 14 | 🟡 Partielle (92%) ⚠️ _Manque p. 208_ |
| S86 | Breyley | Iranian Musicians and Joy Division | p. 209–228 | 240–259 | 11 | 5 ✅ | 7 | 5 | 14 | ✅ Complète |
| S87 | Otter Bickerdike | Posteconomy of Joy Division | p. 229–242 | 260–273 | 10 | 6 ✅ | 7 | 5 | 13, 14 | ✅ Complète |
| S88 | Cashell | Spectral Presences / Joy Division → New Order | p. 245–266 | 276–297 | 11 | 10 ✅ | 7 | 6 | 4, 5, 11, 14 | ✅ Complète |

> ✅ dans colonne Citations = section CITATIONS vérifiée sur PDF (note_verification présente sur chaque entrée).  
> Chapitres = champs `chapitres:` dans les atomes v2 ou les relations.

---

## Couverture par chapitre du manuscrit

_Sources atomisées couvrant chaque chapitre (ch. 1–14), d'après les champs `chapitres:` déclarés dans les atomes v2._

| Chapitre | Records totaux | Sources H&S couvrantes | Nb H&S |
|---|---:|---|---:|
| Ch. 01 | 541 | S66, S83, S84, S85 | 4 |
| Ch. 02 | 750 | S66, S84, S85 | 3 |
| Ch. 03 | 777 | S65, S67, S80, S82, S83, S84 | 6 |
| Ch. 04 | 672 | S65, S66, S67, S80, S82, S88 | 6 |
| Ch. 05 | 672 | S82, S83, S84, S85, S88 | 5 |
| Ch. 06 | 933 | S65, S66, S80, S82, S83, S84 | 6 |
| Ch. 07 | 298 | S66 | 1 ⚠️ |
| Ch. 08 | 658 | S84, S85 | 2 ⚠️ |
| Ch. 09 | 364 | S84 | 1 ⚠️ |
| Ch. 10 | 605 | S84, S85 | 2 ⚠️ |
| Ch. 11 | 650 | S65, S66, S88 | 3 |
| Ch. 12 | 717 | S67, S80, S81 | 3 |
| Ch. 13 | 443 | S82, S85, S87 | 3 |
| Ch. 14 | 2 285 | S62, S63, S64, S65, S66, S67, S80, S81, S82, S84, S85, S86, S87, S88 | 14 |

### Chapitres avec couverture H&S < 4 sources

- **Ch. 02** — 3 sources : `S66, S84, S85`  
- **Ch. 07** — 1 source : `S66` ← **lacune critique**  
- **Ch. 08** — 2 sources : `S84, S85`  
- **Ch. 09** — 1 source : `S84` ← **lacune critique**  
- **Ch. 10** — 2 sources : `S84, S85`  
- **Ch. 11** — 3 sources : `S65, S66, S88`  
- **Ch. 12** — 3 sources : `S67, S80, S81`  
- **Ch. 13** — 3 sources : `S82, S85, S87`  

> Ch. 07 et 09 sont couverts par d'autres sources du corpus (S41, S45, S46, S47, S75, S76…) mais dans le périmètre H&S, la couverture reste très limitée.

---

## Sources prioritaires — actions restantes

### A — Sources avec pages manquantes (H&S)

| ID | Auteur | Pages manquantes | % couvert |
|---|---|---|---|
| S64 | Bottà | pp. 45–46 | 85% |
| S65 | Martínez | pp. 50, 62 | 87% |
| S66 | Schütte | pp. 79–80 | 88% |
| S67 | Naiman | pp. 96–98 | 81% |
| S80 | Valdés Miyares | pp. 110–114 | 68% |
| S81 | Devereux et al. | pp. 129–130 | 87% |
| S82 | Parmar | pp. 135, 153–154 | 86% |
| S83 | Greenwood & Tarpey | pp. 160, 168–170 | 75% |
| S84 | Cope | pp. 183–184, 190–192 | 77% |
| S85 | Malcolm | p. 208 | 92% |

### B — Sources `deuxième_passe` engagées

| ID | Auteur | Titre | Atomes actuels |
|---|---|---|---:|
| S71 | Flowers | New Order + Joy Division: Dreams Never End | 75 |
| S72 | Reynolds | Rip It Up and Start Again | 61 |

### C — Sources fixées sans atomes (non démarrées)

| ID | Auteur | Titre | Note |
|---|---|---|---|
| S07 | Engels | The Condition of the Working Class | PDF identifié |
| S08 | I.S. | Internationale situationniste, n° 2 | OCR faible |
| S16 | Songfacts | Boredom by Buzzcocks | Web, évolutif |
| S17 | Contrib. | Rowche Rumble (Wikipedia) | Web, évolutif |
| S19 | Bourdieu | Les trois états du capital culturel | PDF identifié |

### D — Sources à consolider (aucun atome)

S01, S03, S04, S18, S23, S24, S25, S28, S30, S32, S33, S36, S38, S73

---

## État de l'audit

| Métrique | Valeur | Delta session |
|---|---|---|
| Erreurs bloquantes | **0** | -15 (était 15) |
| Doublons d'identifiants | **0** | -14 (supprimés / renommés) |
| YAML parse errors | **0** | -1 (corrigé master_concepts.md) |
| Avertissements | 31 249 | stable |
| unknown_yaml_blocks | 1 425 | stable (type: ajoutés → reste warn.) |
| v2 migration debt | 2 643 atomes | non démarrée (stratégique) |

---

## Notes d'interprétation

- **Pagination non déclarée** : les sources sans champ `pages_atomisees` dans `source.md` affichent "pag. NR". Des atomes existent mais la couverture est incalculable.
- **Chapitres v2** : la colonne "Chap. v2" ne compte que les atomes déclarant explicitement un champ `chapitres:` (format v2). Les atomes v1 affichent "—".
- **Dette migration v2** : 2 643 atomes sur 2 716 manquent de champs v2 obligatoires. Cette dette ne doit pas être corrigée mécaniquement — elle relève d'une migration progressive source par source.
- **REGISTRY** : identifiant interne de référence pour les chansons, ajouté au registre le 26/05/2026.

---

_Tableau régénéré le 26 mai 2026 — état complet post-audit. 0 erreur bloquante. Citations H&S S85–S88 vérifiées sur PDF._
