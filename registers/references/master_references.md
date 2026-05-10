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
usage:
  - contexte économique
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
arbitrage: "Source présente dans le registre JSON, mais référence bibliographique complète non encore consolidée."
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
usage:
  - données démographiques
  - shrinking cities
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
arbitrage: "Source présente dans le registre JSON ; référence complète et URL à vérifier."
```

## S03 — ONS, séries emploi / population, s.d.

```yaml
id: S03
source_label: "S03 — ONS, séries emploi / population, s.d."
auteur: ONS
titre: Séries statistiques emploi / population
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: données statistiques
statut: a_consolider
fiabilite: forte
usage:
  - emploi
  - population
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
arbitrage: "Source statistique fiable par nature, mais référence précise à consolider."
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
usage:
  - industrialisation
  - histoire de Manchester
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
arbitrage: "Référence à vérifier bibliographiquement avant passage en statut vérifié."
```

## S05 — Jeffery, Moss Side riots study, s.d.

```yaml
id: S05
source_label: "S05 — Jeffery, Moss Side riots study, s.d."
auteur: Peter Jeffery
titre: Étude sur les émeutes de Moss Side
annee: "s.d."
reference_complete: "À consolider depuis les documents de travail historiques."
nature: étude universitaire ou historique
statut: a_consolider
fiabilite: moyenne
usage:
  - émeutes
  - contexte urbain
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
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
usage:
  - Hulme
  - régénération urbaine
chapitres:
  - Chapitre 1
source_origin:
  - data/registre.json
arbitrage: "Référence universitaire précise à identifier."
```

## S41 — Hook, Unknown Pleasures, 2012

```yaml
id: S41
source_label: "S41 — Hook, Unknown Pleasures, 2012"
auteur: Peter Hook
titre: Unknown Pleasures: Inside Joy Division
annee: "2012"
reference_complete: "HOOK, Peter, Unknown Pleasures: Inside Joy Division, Londres, Simon & Schuster, 2012."
nature: mémoire primaire
statut: atomisee_a_consolider
fiabilite: forte
usage:
  - mémoire interne
  - formation du groupe
  - dynamique musicale
  - Factory
chapitres:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 6
  - Chapitre 7
  - Chapitre 8
  - Chapitre 9
  - Chapitre 10
  - Chapitre 11
source_origin:
  - data/registre.json
  - atomisation
arbitrage: "Référence à conserver ; statut atomisé. Les citations doivent être arbitrées dans master_quotes.md."
```

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
usage:
  - mémoire intime
  - Ian Curtis
  - domesticité
  - maladie
  - derniers mois
chapitres:
  - Chapitre 10
  - Chapitre 11
  - Chapitre 12
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
arbitrage: "Référence à conserver ; source primaire à manier avec précautions mémorielles."
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
usage:
  - chronologie fondatrice
  - premières années
  - discographie initiale
chapitres:
  - Chapitre 2
  - Chapitre 8
  - Chapitre 14
source_origin:
  - data/registre.json
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
usage:
  - recoupement biographique
  - recoupement chronologique
  - critique du mythe Curtis
chapitres:
  - Chapitre 2
  - Chapitre 5
  - Chapitre 10
  - Chapitre 11
  - Chapitre 14
source_origin:
  - data/registre.json
arbitrage: "Source repère ; atomisation complète souhaitable."
```

## S68 — Broll, Joy Division, s.d.

```yaml
id: S68
legacy_id:
  - S-BROLL-JOY-001
source_label: "S68 — Broll, Joy Division, s.d."
auteur: Marco Broll
titre: Joy Division
annee: "s.d."
reference_complete: "BROLL, Marco, Joy Division, référence complète à consolider."
nature: document critique ou documentaire OCRisé
statut: atomisee_a_consolider
fiabilite: moyenne
usage:
  - recoupement chronologique
  - recoupement discographique
  - sessions
  - concerts
  - objets discographiques
  - bootlegs
chapitres:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 6
  - Chapitre 8
  - Chapitre 9
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
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
usage:
  - nostalgie
  - mémoire culturelle
  - témoins d’autorité
  - patrimonialisation
  - réception contemporaine
  - marketing
chapitres:
  - Chapitre 9
  - Chapitre 10
  - Chapitre 11
  - Chapitre 12
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
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
usage:
  - chronologie
  - discographie
  - réception
  - analyse sonore
  - paroles
  - culte
  - Factory
  - héritage posthume
chapitres:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 6
  - Chapitre 7
  - Chapitre 8
  - Chapitre 9
  - Chapitre 10
  - Chapitre 11
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
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
usage:
  - Joy Division
  - New Order
  - Manchester
  - Factory
  - transition posthume
  - Hacienda
  - Blue Monday
  - Substance
  - héritage
chapitres:
  - Chapitre 1
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 6
  - Chapitre 7
  - Chapitre 8
  - Chapitre 9
  - Chapitre 10
  - Chapitre 11
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
arbitrage: "Source secondaire publiée ; citations d’acteurs à distinguer de la narration de Flowers."
```

## S72 — Reynolds, Rip It Up and Start Again, 2005/2006

```yaml
id: S72
legacy_id:
  - S20
source_label: "S72 — Reynolds, Rip It Up and Start Again, 2005/2006"
auteur: Simon Reynolds
titre: Rip It Up and Start Again: Postpunk 1978–1984
annee: "2005/2006"
reference_complete: "REYNOLDS, Simon, Rip It Up and Start Again: Postpunk 1978–1984, Londres, Faber and Faber, 2005 ; New York, Penguin Books, 2006."
nature: essai historique et critique
statut: atomisee
fiabilite: forte
usage:
  - post-punk
  - Joy Division
  - Manchester
  - Factory
  - Ballard
  - DIY
  - New Order
  - goth
  - héritage
chapitres:
  - Chapitre 1
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 7
  - Chapitre 8
  - Chapitre 9
  - Chapitre 10
  - Chapitre 11
  - Chapitre 13
  - Chapitre 14
source_origin:
  - data/registre.json
  - atomisation
  - ancien document de travail probable
arbitrage: "S72 est l’identifiant canonique du repo ; S20 est conservé comme legacy_id issu des anciens documents de travail. Décision réversible par migration dédiée."
```

---

# Entrées réservées à consolider

Les identifiants `S07` à `S40` sont signalés comme probablement présents dans les anciens registres de chapitre mais absents de `data/registre.json` à ce stade.

```yaml
range: S07-S40
statut: a_importer_ou_a_ecarter
source_origin:
  - documents de travail historiques probables
arbitrage: "Ne pas réutiliser ces numéros pour de nouvelles atomisations avant examen des anciens registres."
```
