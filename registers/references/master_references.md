# Registre consolidé des références

Ce registre est une couche de consolidation. Il ne donne pas automatiquement raison aux anciens registres ni aux fichiers issus de l’atomisation.

Il fusionne progressivement les matériaux disponibles :

```text
data/registre.json
sources/*/source.md
sources/*/README.md
anciens registres et documents maîtres lorsqu’ils sont importés comme matériaux de travail
```

Chaque entrée conserve l’origine documentaire et les arbitrages à instruire.

---

## S01 — Manchester City Council, East Manchester economic base decline, s.d.

```yaml
id: S01
source_label: "S01 — Manchester City Council, East Manchester economic base decline, s.d."
auteur: Manchester City Council
titre: East Manchester economic base decline
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: institutionnel
statut: a_consolider
fiabilite: moyenne
usage: [contexte économique]
concepts: [déclin emploi, East Manchester]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Source présente dans les deux familles de travail ; référence complète à consolider."
```

## S02 — Sénat, Rapport shrinking cities Manchester, s.d.

```yaml
id: S02
source_label: "S02 — Sénat, Rapport shrinking cities Manchester, s.d."
auteur: Sénat
titre: Rapport d’information – shrinking cities Manchester / Greater Manchester
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: rapport institutionnel
statut: a_consolider
fiabilite: moyenne
usage: [données démographiques, shrinking cities]
concepts: [shrinking city, démographie, emploi]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Source présente dans les deux familles de travail ; référence complète et URL à vérifier."
```

## S03 — Demographia / ONS, séries emploi / population, s.d.

```yaml
id: S03
source_label: "S03 — Demographia / ONS, séries emploi / population, s.d."
auteur: Demographia / ONS
titre: Séries statistiques emploi / population
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: données statistiques
statut: a_consolider
fiabilite: moyenne
usage: [démographie urbaine, emploi, population]
concepts: [démographie urbaine, périmètres, emploi]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Le registre JSON mentionnait ONS ; le registre historique mentionne Demographia. Divergence à instruire avant validation."
```

## S04 — Kidd, Manchester: A History, 2006

```yaml
id: S04
source_label: "S04 — Kidd, Manchester: A History, 2006"
auteur: Alan Kidd
titre: Manchester: A History
annee: "2006"
reference_complete: "KIDD, Alan, Manchester: A History, Lancaster, Carnegie Publishing, 2006. Référence à vérifier."
nature: livre historique
statut: a_consolider
fiabilite: forte
usage: [industrialisation, histoire de Manchester]
concepts: [désindustrialisation, emplois manufacturiers]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Référence à vérifier bibliographiquement avant passage en statut vérifié."
```

## S05 — Jeffery, Moss Side riots study, s.d.

```yaml
id: S05
source_label: "S05 — Jeffery, Moss Side riots study, s.d."
auteur: Peter Jeffery
titre: Étude sur les émeutes de Moss Side, juillet 1981
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: étude universitaire ou historique
statut: a_consolider
fiabilite: moyenne
usage: [émeutes, police, ordres de grandeur]
concepts: [émeutes, police, ordres de grandeur]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Auteur, titre exact, date et support à vérifier."
```

## S06 — Carter, Hulme Crescents study, s.d.

```yaml
id: S06
source_label: "S06 — Carter, Hulme Crescents study, s.d."
auteur: Holly Carter
titre: Mémoire / thèse sur Hulme Crescents et régénération
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: mémoire ou thèse
statut: a_consolider
fiabilite: moyenne
usage: [Hulme, régénération urbaine]
concepts: [modernisme, échec urbain, logement social]
chapitres: [Chapitre 1]
source_origin: [data/registre.json, registre historique]
arbitrage: "Référence universitaire précise à identifier."
```

---

# Références historiques importées S07-S41

## S07 — Engels, La Situation de la classe laborieuse en Angleterre, 1845

```yaml
id: S07
source_label: "S07 — Engels, La Situation de la classe laborieuse en Angleterre, 1845"
auteur: Friedrich Engels
titre: La Situation de la classe laborieuse en Angleterre
annee: "1845"
reference_complete: "ENGELS, Friedrich, La Situation de la classe laborieuse en Angleterre, 1845. Édition utilisée à préciser."
nature: livre historique et politique
statut: a_consolider
fiabilite: forte
usage: [conditions de vie, Salford, Manchester]
concepts: [conditions de vie, Salford, Manchester]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; édition et pagination à préciser avant citation."
```

## S08 — Debord, psychogéographie / dérive, s.d.

```yaml
id: S08
source_label: "S08 — Debord, Psychogéographie / dérive, s.d."
auteur: Guy Debord
titre: Psychogéographie / dérive, Internationale situationniste
annee: "s.d."
reference_complete: "DEBORD, Guy, textes sur la psychogéographie et la dérive, référence précise à déterminer."
nature: texte théorique
statut: a_consolider
fiabilite: moyenne
usage: [psychogéographie, dérive]
concepts: [psychogéographie, dérive]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence théorique utile ; texte exact et édition à fixer."
```

## S09 — Cummins, corpus photographique Joy Division / Manchester, 1979

```yaml
id: S09
source_label: "S09 — Cummins, corpus photographique Joy Division / Manchester, 1979"
auteur: Kevin Cummins
titre: Corpus photographique Joy Division / Manchester
annee: "1979"
reference_complete: "CUMMINS, Kevin, corpus photographique Joy Division / Manchester, référence précise à déterminer."
nature: corpus photographique
statut: a_consolider
fiabilite: forte
usage: [iconographie, paysage urbain]
concepts: [iconographie, paysage urbain]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; préciser livre, exposition, archive ou image utilisée."
```

## S10 — University of Birmingham eTheses, Sumner sur Salford, s.d.

```yaml
id: S10
source_label: "S10 — University of Birmingham eTheses, Sumner sur Salford, s.d."
auteur: University of Birmingham eTheses
titre: Thèse / ressource citant Bernard Sumner sur Salford
annee: "s.d."
reference_complete: "Référence eTheses exacte à identifier."
nature: thèse ou ressource universitaire
statut: a_consolider
fiabilite: moyenne
usage: [témoignage, mémoire urbaine]
concepts: [témoignage, mémoire urbaine]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Source utilisée pour citations attribuées à Sumner ; retrouver la thèse exacte et la source primaire si possible."
```

## S11 — UK Gov / DTI, données industrielles 1978-1988, s.d.

```yaml
id: S11
source_label: "S11 — UK Gov / DTI, données industrielles 1978-1988, s.d."
auteur: Margaret Thatcher policies / UK Government statistics / DTI
titre: Données DTI / dépenses industrielles 1978-1988
annee: "s.d."
reference_complete: "Référence statistique gouvernementale exacte à préciser."
nature: données statistiques et politiques publiques
statut: a_consolider
fiabilite: moyenne
usage: [austérité, politique industrielle]
concepts: [austérité, politique industrielle]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; source gouvernementale exacte à identifier."
```

## S12 — Anderton, chef de police du Greater Manchester, s.d.

```yaml
id: S12
source_label: "S12 — Anderton, chef de police du Greater Manchester, s.d."
auteur: James Anderton
titre: Figure du chef de police du Greater Manchester, profil et citations
annee: "s.d."
reference_complete: "Source primaire ou secondaire à préciser."
nature: profil / citations / source historique
statut: a_consolider
fiabilite: moyenne
usage: [contrôle social, répression]
concepts: [contrôle social, répression]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Importer seulement les citations vérifiées dans master_quotes.md."
```

## S13 — Tomeo, Manchester / contrôle social sous Thatcher, s.d.

```yaml
id: S13
source_label: "S13 — Tomeo, Manchester / contrôle social sous Thatcher, s.d."
auteur: Caterina Tomeo
titre: Analyse sur Manchester / contrôle social sous Thatcher
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: analyse critique ou universitaire
statut: a_consolider
fiabilite: moyenne
usage: [ordre public, conservatisme moral]
concepts: [ordre public, conservatisme moral]
chapitres: [Chapitre 7]
source_origin: [registre historique]
arbitrage: "Référence importée ; l’affectation au chapitre 7 vient du registre historique."
```

## S14 — Happy Mondays, God's Cop, s.d.

```yaml
id: S14
source_label: "S14 — Happy Mondays, God's Cop, s.d."
auteur: Happy Mondays
titre: God's Cop
annee: "s.d."
reference_complete: "HAPPY MONDAYS, « God's Cop », référence discographique à préciser."
nature: référence discographique
statut: a_consolider
fiabilite: moyenne
usage: [réappropriation musicale, police]
concepts: [réappropriation musicale, police]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence connexe, utile surtout pour réception mancunienne ultérieure."
```

## S15 — De Luca, concert Sex Pistols et scène mancunienne, s.d.

```yaml
id: S15
source_label: "S15 — De Luca, concert Sex Pistols et scène mancunienne, s.d."
auteur: Daniele De Luca
titre: Analyse du concert des Sex Pistols du 4 juin 1976 et de la scène mancunienne
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: analyse historique ou critique
statut: a_consolider
fiabilite: moyenne
usage: [événement fondateur, catalyseur]
concepts: [événement fondateur, catalyseur]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; à vérifier avec les sources primaires sur les concerts Sex Pistols à Manchester."
```

## S16 — Buzzcocks, Boredom, 1977

```yaml
id: S16
source_label: "S16 — Buzzcocks, Boredom, 1977"
auteur: Buzzcocks
titre: Boredom
annee: "1977"
reference_complete: "BUZZCOCKS, « Boredom », sur Spiral Scratch, New Hormones, 1977. Référence discographique à préciser."
nature: référence discographique
statut: a_consolider
fiabilite: forte
usage: [ennui, jeunesse]
concepts: [ennui, jeunesse]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence musicale à consolider avec Discogs ou source discographique stable."
```

## S17 — The Fall, Rowche Rumble, 1979

```yaml
id: S17
source_label: "S17 — The Fall, Rowche Rumble, 1979"
auteur: The Fall
titre: Rowche Rumble
annee: "1979"
reference_complete: "THE FALL, « Rowche Rumble », 1979. Référence discographique à préciser."
nature: référence discographique
statut: a_consolider
fiabilite: forte
usage: [critique sociale, médicaments]
concepts: [critique sociale, médicaments]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence connexe à la scène mancunienne ; préciser support et label."
```

## S18 — Fédida, Manchester : L’éveil d’une scène musicale, s.d.

```yaml
id: S18
source_label: "S18 — Fédida, Manchester : L’éveil d’une scène musicale, s.d."
auteur: Michel-Angelo Fédida
titre: Manchester : L’éveil d’une scène musicale
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: analyse critique ou historique
statut: a_consolider
fiabilite: moyenne
usage: [punk, génération]
concepts: [punk, génération]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; localisation bibliographique à faire."
```

## S19 — Bourdieu, reconversion du capital, s.d.

```yaml
id: S19
source_label: "S19 — Bourdieu, reconversion du capital, s.d."
auteur: Pierre Bourdieu
titre: Concept de reconversion du capital
annee: "s.d."
reference_complete: "BOURDIEU, Pierre, référence exacte sur la reconversion du capital à préciser."
nature: concept sociologique
statut: a_consolider
fiabilite: forte
usage: [capital culturel, conversion]
concepts: [capital culturel, conversion]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence conceptuelle ; ouvrage ou article exact à fixer avant citation."
```

## S20 — Reynolds, cadre historique post-punk, migré vers S72

```yaml
id: S20
canonical_id: S72
source_label: "S20 — Reynolds, cadre historique post-punk, s.d."
auteur: Simon Reynolds
titre: Cadre historique post-punk
annee: "s.d."
reference_complete: "Voir S72 — Reynolds, Rip It Up and Start Again, 2005/2006."
nature: legacy_reference
statut: migree
fiabilite: forte
usage: [post-punk, scène]
concepts: [post-punk, scène]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Identifiant historique conservé comme legacy_id ; l’identifiant repo canonique est S72."
```

## S21 — City Fun, corpus 1978-1983, s.d.

```yaml
id: S21
source_label: "S21 — City Fun, corpus 1978-1983, s.d."
auteur: City Fun
titre: Corpus du fanzine City Fun, 1978-1983
annee: "1978-1983"
reference_complete: "CITY FUN, corpus 1978-1983, archives à préciser."
nature: fanzine / archive
statut: a_consolider
fiabilite: moyenne
usage: [médias alternatifs, DIY]
concepts: [médias alternatifs, DIY]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence d’archive ; préciser fonds, numéros et pages."
```

## S22 — Wilkinson, analyse de City Fun, s.d.

```yaml
id: S22
source_label: "S22 — Wilkinson, analyse de City Fun, s.d."
auteur: David Wilkinson
titre: Analyse de City Fun
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: analyse universitaire ou critique
statut: a_consolider
fiabilite: moyenne
usage: [médias, politique]
concepts: [médias, politique]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; à localiser."
```

## S23 — Rochdale Alternative Press, infrastructure contre-culturelle, s.d.

```yaml
id: S23
source_label: "S23 — Rochdale Alternative Press, infrastructure contre-culturelle, s.d."
auteur: Rochdale Alternative Press
titre: Imprimerie coopérative / infrastructure contre-culturelle
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: archive / infrastructure contre-culturelle
statut: a_consolider
fiabilite: moyenne
usage: [DIY, production]
concepts: [DIY, production]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importée ; préciser support documentaire."
```

## S24 — Boon / New Hormones, Spiral Scratch, s.d.

```yaml
id: S24
source_label: "S24 — Boon / New Hormones, Spiral Scratch, s.d."
auteur: Richard Boon / New Hormones
titre: New Hormones + Spiral Scratch, Buzzcocks
annee: "s.d."
reference_complete: "Référence exacte à préciser ; inclure Buzzcocks, Spiral Scratch, New Hormones, 1977."
nature: label indépendant / référence discographique
statut: a_consolider
fiabilite: forte
usage: [label indépendant, distribution]
concepts: [label indé, distribution]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "À rapprocher de S72-A008 et des atomes Reynolds sur DIY."
```

## S25 — Factory Records, philosophie pas de contrats, s.d.

```yaml
id: S25
source_label: "S25 — Factory Records, philosophie pas de contrats, s.d."
auteur: Factory Records
titre: Philosophie « pas de contrats » et écosystème Factory
annee: "s.d."
reference_complete: "Sources précises à déterminer ; à croiser avec Tony Wilson, Rob Gretton, Simon Reynolds et Claude Flowers."
nature: concept documentaire / archive label
statut: a_consolider
fiabilite: moyenne
usage: [indépendance, label]
concepts: [indépendance, label]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Entrée conceptuelle plus que référence unique ; peut être éclatée en sources primaires/secondaires."
```

## S26 — Butt, Post-Punk Then and Now, s.d.

```yaml
id: S26
source_label: "S26 — Butt, Post-Punk Then and Now, s.d."
auteur: Gavin Butt
titre: Post-Punk Then and Now
annee: "s.d."
reference_complete: "BUTT, Gavin, Post-Punk Then and Now, référence complète à préciser."
nature: ouvrage ou article critique
statut: a_consolider
fiabilite: forte
usage: [écoles d’art, réseaux]
concepts: [écoles d’art, réseaux]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence à localiser et compléter."
```

## S27 — Crossley, réseaux sociaux et scènes musicales, s.d.

```yaml
id: S27
source_label: "S27 — Crossley, réseaux sociaux et scènes musicales, s.d."
auteur: Nick Crossley
titre: Travaux sur réseaux sociaux et scènes musicales
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: sociologie des réseaux
statut: a_consolider
fiabilite: forte
usage: [réseaux, sociologie]
concepts: [réseaux, sociologie]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Déterminer quel ouvrage/article de Crossley fonde l’usage."
```

## S28 — Granada TV / Tony Wilson, So It Goes, s.d.

```yaml
id: S28
source_label: "S28 — Granada TV / Tony Wilson, So It Goes, s.d."
auteur: Granada TV / Tony Wilson
titre: So It Goes, archives émission
annee: "s.d."
reference_complete: "Référence audiovisuelle précise à déterminer."
nature: archive audiovisuelle
statut: a_consolider
fiabilite: forte
usage: [médiatisation, TV]
concepts: [médiatisation, TV]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Préciser épisode, date et accès archive."
```

## S29 — Goddard, post-punk et paysage industriel, s.d.

```yaml
id: S29
source_label: "S29 — Goddard, post-punk et paysage industriel, s.d."
auteur: Michael Goddard
titre: Analyse du post-punk et transformation du paysage industriel
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: article ou ouvrage critique
statut: a_consolider
fiabilite: forte
usage: [hantologie, esthétique]
concepts: [hantologie, esthétique]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence centrale à consolider si le chapitre mobilise hantologie/paysage industriel."
```

## S30 — Frith, musique populaire et résistance culturelle, s.d.

```yaml
id: S30
source_label: "S30 — Frith, musique populaire et résistance culturelle, s.d."
auteur: Simon Frith
titre: Travaux sur musique populaire et résistance culturelle
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: sociologie / musicologie populaire
statut: a_consolider
fiabilite: forte
usage: [résistance, musique pop]
concepts: [résistance, musique pop]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Déterminer l’ouvrage ou article exact de Frith utilisé."
```

## S31 — Allegri, Living in the Ice Age, s.d.

```yaml
id: S31
source_label: "S31 — Allegri, Living in the Ice Age, s.d."
auteur: Giuseppe Allegri
titre: Living in the Ice Age
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: analyse critique
statut: a_consolider
fiabilite: moyenne
usage: [froid, modernité]
concepts: [froid, modernité]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence à localiser."
```

## S32 — Kraftwerk, influence électronique, s.d.

```yaml
id: S32
source_label: "S32 — Kraftwerk, influence électronique, s.d."
auteur: Kraftwerk
titre: Influence électronique, références à préciser
annee: "s.d."
reference_complete: "Référence discographique ou critique à préciser."
nature: référence musicale / influence
statut: a_consolider
fiabilite: forte
usage: [avant-garde, mécanique]
concepts: [avant-garde, mécanique]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Entrée trop générale ; préciser albums, morceaux ou source critique."
```

## S33 — Can, influence krautrock, s.d.

```yaml
id: S33
source_label: "S33 — Can, influence krautrock, s.d."
auteur: Can
titre: Influence krautrock, références à préciser
annee: "s.d."
reference_complete: "Référence discographique ou critique à préciser."
nature: référence musicale / influence
statut: a_consolider
fiabilite: forte
usage: [expérimentation, répétition]
concepts: [expérimentation, répétition]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Entrée trop générale ; préciser albums, morceaux ou source critique."
```

## S34 — Fraser & Fuoto, incorporation urbaine dans Joy Division, s.d.

```yaml
id: S34
source_label: "S34 — Fraser & Fuoto, incorporation urbaine dans Joy Division, s.d."
auteur: Benjamin Fraser ; Abby Fuoto
titre: Étude sur l’incorporation urbaine dans la musique de Joy Division
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: article universitaire
statut: a_consolider
fiabilite: forte
usage: [urbanité, incorporation]
concepts: [urbanité, incorporation]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence importante pour géographie émotionnelle ; à localiser et atomiser si disponible."
```

## S35 — Peter Hook, autobiographie / mémoires, migré vers S73

```yaml
id: S35
canonical_id: S73
source_label: "S35 — Peter Hook, autobiographie / mémoires, s.d."
auteur: Peter Hook
titre: Autobiographie / mémoires
annee: "s.d."
reference_complete: "Voir S73 — Hook, Unknown Pleasures, 2012."
nature: legacy_reference
statut: migree
fiabilite: forte
usage: [ancrage territorial, Factory]
concepts: [ancrage territorial, Factory]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Identifiant historique conservé comme entrée migrée ; l’identifiant repo canonique pour Hook est S73."
```

## S36 — Crosthwaite, historicisme imaginatif, s.d.

```yaml
id: S36
source_label: "S36 — Crosthwaite, historicisme imaginatif, s.d."
auteur: Paul Crosthwaite
titre: Critique de l’historicisme imaginatif
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: critique méthodologique
statut: a_consolider
fiabilite: moyenne
usage: [réception critique, méthode]
concepts: [réception critique, méthode]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence à localiser ; utile pour cadrer les risques de projection rétrospective."
```

## S37 — Deborah Curtis, témoignage biographique, migré vers S45

```yaml
id: S37
canonical_id: S45
source_label: "S37 — Deborah Curtis, témoignage biographique, s.d."
auteur: Deborah Curtis
titre: Témoignage biographique
annee: "s.d."
reference_complete: "Voir S45 — Curtis, Touching from a Distance, 1995."
nature: legacy_reference
statut: migree
fiabilite: forte
usage: [biographie, vote 1979]
concepts: [biographie, vote 1979]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Identifiant historique conservé comme entrée migrée ; l’identifiant repo canonique pour Deborah Curtis est S45."
```

## S38 — Saville / Manchester United / Adidas, Pulsebeat of Manchester, 2023

```yaml
id: S38
source_label: "S38 — Saville / Manchester United / Adidas, Pulsebeat of Manchester, 2023"
auteur: Peter Saville / Manchester United / Adidas
titre: Collection Pulsebeat of Manchester
annee: "2023"
reference_complete: "Référence exacte à préciser."
nature: objet visuel / patrimonialisation contemporaine
statut: a_consolider
fiabilite: moyenne
usage: [patrimonialisation, design]
concepts: [patrimonialisation, design]
chapitres: [Chapitre 1, Chapitre 14]
source_origin: [registre historique]
arbitrage: "Source contemporaine ; probablement à traiter surtout au chapitre 14."
```

## S39 — Bauman, modernité liquide, s.d.

```yaml
id: S39
source_label: "S39 — Bauman, modernité liquide, s.d."
auteur: Zygmunt Bauman
titre: Concept de modernité liquide
annee: "s.d."
reference_complete: "BAUMAN, Zygmunt, Modernité liquide, édition à préciser."
nature: concept sociologique
statut: a_consolider
fiabilite: forte
usage: [liquidité, liens sociaux]
concepts: [liquidité, liens sociaux]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence conceptuelle ; édition française ou originale à fixer avant citation."
```

## S40 — Cacciatore, nostalgie du futur, s.d.

```yaml
id: S40
source_label: "S40 — Cacciatore, nostalgie du futur, s.d."
auteur: Fortunato M. Cacciatore
titre: Formule « nostalgie du futur »
annee: "s.d."
reference_complete: "Référence exacte à préciser."
nature: concept / citation à vérifier
statut: a_consolider
fiabilite: faible
usage: [temps, futur perdu]
concepts: [temps, futur perdu]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "Référence incertaine ; ne pas utiliser comme source probatoire avant identification exacte."
```

## S41 — Blue Orchids, entrée historique

```yaml
id: S41
source_label: "S41 — Blue Orchids, entrée historique à consolider, s.d."
auteur: Blue Orchids
titre: Référence à préciser
annee: "s.d."
reference_complete: "À consolider depuis le registre historique."
nature: référence musicale / scène Manchester
statut: a_consolider
fiabilite: moyenne
usage: [post-punk, scène de Manchester]
concepts: [post-punk, scène de Manchester]
chapitres: [Chapitre 1]
source_origin: [registre historique]
arbitrage: "S41 est réservé à l’entrée historique Blue Orchids. Peter Hook est déplacé vers S73."
```

---

# Sources atomisées et repères hors séquence historique importée

## S45 — Curtis, Touching from a Distance, 1995

```yaml
id: S45
source_label: "S45 — Curtis, Touching from a Distance, 1995"
auteur: Deborah Curtis
titre: Touching from a Distance: Ian Curtis and Joy Division
annee: "1995"
reference_complete: "CURTIS, Deborah, Touching from a Distance: Ian Curtis and Joy Division, Londres, Faber and Faber, 1995."
nature: mémoire primaire
statut: atomisee_a_consolider
fiabilite: forte
usage: [mémoire intime, Ian Curtis, domesticité, maladie, derniers mois]
chapitres: [Chapitre 10, Chapitre 11, Chapitre 12, Chapitre 14]
source_origin: [data/registre.json, atomisation]
arbitrage: "Référence repo canonique ; S37 est conservé comme legacy migré."
```

## S46 — Johnson, An Ideal for Living, 1984

```yaml
id: S46
source_label: "S46 — Johnson, An Ideal for Living, 1984"
auteur: Mark Johnson
titre: An Ideal for Living: An History of Joy Division
annee: "1984"
reference_complete: "JOHNSON, Mark, An Ideal for Living: An History of Joy Division, Londres, Bobcat Books, 1984. Référence à vérifier."
nature: livre documentaire ancien
statut: a_atomiser
fiabilite: moyenne
usage: [chronologie fondatrice, premières années, discographie initiale]
chapitres: [Chapitre 2, Chapitre 8, Chapitre 14]
source_origin: [data/registre.json]
arbitrage: "Source repère non encore atomisée dans le repo ; vérifier titre exact et édition."
```

## S47 — West, Joy Division, 1983

```yaml
id: S47
source_label: "S47 — West, Joy Division, 1983"
auteur: Mike West
titre: Joy Division
annee: "1983"
reference_complete: "WEST, Mike, Joy Division, Londres, Babylon Books, 1983. Référence à vérifier."
nature: livre documentaire ancien
statut: source_repere_a_consolider
fiabilite: moyenne
usage: [recoupement biographique, recoupement chronologique, critique du mythe Curtis]
chapitres: [Chapitre 2, Chapitre 5, Chapitre 10, Chapitre 11, Chapitre 14]
source_origin: [data/registre.json]
arbitrage: "Source repère ; atomisation complète souhaitable."
```

## S68 — Broll, Joy Division, s.d.

```yaml
id: S68
legacy_id: [S-BROLL-JOY-001]
source_label: "S68 — Broll, Joy Division, s.d."
auteur: Marco Broll
titre: Joy Division
annee: "s.d."
reference_complete: "BROLL, Marco, Joy Division, référence complète à consolider."
nature: document critique ou documentaire OCRisé
statut: atomisee_a_consolider
fiabilite: moyenne
usage: [recoupement chronologique, recoupement discographique, sessions, concerts, objets discographiques, bootlegs]
chapitres: [Chapitre 2, Chapitre 3, Chapitre 6, Chapitre 8, Chapitre 9, Chapitre 14]
source_origin: [data/registre.json, atomisation]
arbitrage: "Identifiant long remplacé par S68 ; référence complète à consolider."
```

## S69 — Greig & Strong, But We Remember When We Were Young, 2014

```yaml
id: S69
source_label: "S69 — Greig & Strong, But We Remember When We Were Young, 2014"
auteur: Alastair Greig ; Catherine Strong
titre: But We Remember When We Were Young
annee: "2014"
reference_complete: "GREIG, Alastair ; STRONG, Catherine, « But We Remember When We Were Young », Volume ! La revue des musiques populaires, 11:1, 2014, p. 191-205, DOI : 10.4000/volume.4390."
nature: article scientifique traduit
statut: atomisee
fiabilite: forte
usage: [nostalgie, mémoire culturelle, témoins d’autorité, patrimonialisation, réception contemporaine, marketing]
chapitres: [Chapitre 9, Chapitre 10, Chapitre 11, Chapitre 12, Chapitre 14]
source_origin: [data/registre.json, atomisation]
arbitrage: "Référence consolidée ; citations à distinguer entre traduction publiée et citations indirectement rapportées."
```

## S70 — Suatoni, Joy Division, s.d.

```yaml
id: S70
source_label: "S70 — Suatoni, Joy Division, s.d."
auteur: Alfredo Suatoni
titre: Joy Division
annee: "s.d."
reference_complete: "SUATONI, Alfredo, Joy Division, source OCRisée, 12 pages, référence éditoriale à consolider."
nature: livret critique et documentaire OCRisé
statut: atomisee_a_consolider
fiabilite: moyenne
usage: [chronologie, discographie, réception, analyse sonore, paroles, culte, Factory, héritage posthume]
chapitres: [Chapitre 2, Chapitre 3, Chapitre 5, Chapitre 6, Chapitre 7, Chapitre 8, Chapitre 9, Chapitre 10, Chapitre 11, Chapitre 14]
source_origin: [data/registre.json, atomisation]
arbitrage: "Source utile mais OCR bruité ; citations à maintenir en statut candidat tant qu’elles ne sont pas revérifiées."
```

## S71 — Flowers, Dreams Never End, 1995/2012

```yaml
id: S71
source_label: "S71 — Flowers, Dreams Never End, 1995/2012"
auteur: Claude Flowers
titre: New Order + Joy Division: Dreams Never End
annee: "1995/2012"
reference_complete: "FLOWERS, Claude, New Order + Joy Division: Dreams Never End, Londres, Omnibus Press, 1995 ; édition numérique Omnibus Press, 2012, EISBN 978-0-85712-760-0."
nature: livre biographique et discographique
statut: atomisee
fiabilite: moyenne
usage: [Joy Division, New Order, Manchester, Factory, transition posthume, Hacienda, Blue Monday, Substance, héritage]
chapitres: [Chapitre 1, Chapitre 2, Chapitre 3, Chapitre 5, Chapitre 6, Chapitre 7, Chapitre 8, Chapitre 9, Chapitre 10, Chapitre 11, Chapitre 14]
source_origin: [data/registre.json, atomisation]
arbitrage: "Source secondaire publiée ; citations d’acteurs à distinguer de la narration de Flowers."
```

## S72 — Reynolds, Rip It Up and Start Again, 2005/2006

```yaml
id: S72
legacy_id: [S20]
source_label: "S72 — Reynolds, Rip It Up and Start Again, 2005/2006"
auteur: Simon Reynolds
titre: Rip It Up and Start Again: Postpunk 1978–1984
annee: "2005/2006"
reference_complete: "REYNOLDS, Simon, Rip It Up and Start Again: Postpunk 1978–1984, Londres, Faber and Faber, 2005 ; New York, Penguin Books, 2006."
nature: essai historique et critique
statut: atomisee
fiabilite: forte
usage: [post-punk, Joy Division, Manchester, Factory, Ballard, DIY, New Order, goth, héritage]
chapitres: [Chapitre 1, Chapitre 2, Chapitre 3, Chapitre 5, Chapitre 7, Chapitre 8, Chapitre 9, Chapitre 10, Chapitre 11, Chapitre 13, Chapitre 14]
source_origin: [data/registre.json, atomisation, registre historique]
arbitrage: "S72 est l’identifiant canonique du repo ; S20 est conservé comme legacy_id issu des anciens documents de travail."
```

## S73 — Hook, Unknown Pleasures, 2012

```yaml
id: S73
legacy_id: [S41-REPO, S35]
source_label: "S73 — Hook, Unknown Pleasures, 2012"
auteur: Peter Hook
titre: Unknown Pleasures: Inside Joy Division
annee: "2012"
reference_complete: "HOOK, Peter, Unknown Pleasures: Inside Joy Division, Londres, Simon & Schuster, 2012."
nature: mémoire primaire
statut: atomisee_a_migrer
fiabilite: forte
usage: [mémoire interne, formation du groupe, dynamique musicale, Factory]
chapitres: [Chapitre 1, Chapitre 2, Chapitre 3, Chapitre 5, Chapitre 6, Chapitre 7, Chapitre 8, Chapitre 9, Chapitre 10, Chapitre 11, Chapitre 13, Chapitre 14]
source_origin: [data/registre.json, atomisation, registre historique]
arbitrage: "Peter Hook est déplacé de S41 vers S73 pour libérer l’identifiant historique S41. Les fichiers sources/hook contiennent encore des atomes S41-* et doivent être migrés par opération dédiée vers S73-*."
```
