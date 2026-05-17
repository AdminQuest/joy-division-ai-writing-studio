# S39 — Source canonique — Bauman, *Liquid Modernity*, 2000

## 1. Identifiant canonique

```text
S39
```

## 2. Libellé source

```text
S39 — Bauman, Liquid Modernity, 2000
```

## 3. Dossier source

```text
sources/bauman_liquid_modernity/
```

## 4. Référence complète

BAUMAN, Zygmunt, *Liquid Modernity*, Cambridge, Polity Press, 2000.

## 5. Entrée canonique pour `data/registre.json`

```json
{
  "id": "S39",
  "source_label": "S39 — Bauman, Liquid Modernity, 2000",
  "source_short_title": "Bauman, Liquid Modernity, 2000",
  "auteur": "Zygmunt Bauman",
  "titre": "Liquid Modernity",
  "annee": "2000",
  "reference_complete": "BAUMAN, Zygmunt, Liquid Modernity, Cambridge, Polity Press, 2000.",
  "nature": "ouvrage théorique / sociologie de la modernité",
  "statut": "verifie ; source canonique fixée ; fichier Drive identifié",
  "fiabilite": "forte comme cadre théorique ; non spécialisée sur Joy Division",
  "usage": [
    "modernité liquide",
    "liquid modernity",
    "dissolution des cadres stables",
    "fragilité des liens sociaux",
    "mobilité",
    "incertitude",
    "précarité des appartenances",
    "dissolution des formes durables",
    "réception contemporaine",
    "patrimonialisation diffuse",
    "instabilité culturelle",
    "sociologie de la modernité"
  ],
  "chapitres": [
    "Chapitre 1",
    "Chapitre 11",
    "Chapitre 14"
  ],
  "chapitres_secondaires": [
    "Chapitre 3",
    "Chapitre 7",
    "Chapitre 13"
  ],
  "source_origin": [
    "Google Drive",
    "PDF intégral",
    "registre historique",
    "document maître"
  ],
  "dossier_source": "sources/bauman_liquid_modernity/",
  "fichier_source": "S39_bauman_liquid_modernity_2000.pdf",
  "fichier_source_original": "bauman-liquid-modernity.pdf",
  "source_drive": "https://drive.google.com/file/d/1hrtrNh8RCZXUmjeHTv5d2NkzucmxvwpU/view?usp=drive_link",
  "lieu_edition": "Cambridge",
  "editeur": "Polity Press",
  "niveau_preuve": "source secondaire théorique / sociologie de la modernité",
  "arbitrage": "S39 désigne désormais l’ouvrage de Zygmunt Bauman, Liquid Modernity, publié par Polity Press en 2000. L’ancienne entrée Liquid Modernity ; La vie liquide est resserrée : La vie liquide peut rester une référence baumanienne secondaire, mais elle ne gouverne plus l’identifiant canonique S39. S39 sert à penser la réception contemporaine, la dissolution des cadres stables et la fragilité des appartenances, non la genèse historique de Joy Division.",
  "prudence": "Ne pas utiliser S39 comme source historique ou musicale sur Joy Division, Manchester, Factory Records ou Ian Curtis. Employer Bauman comme cadre théorique rétrospectif. Distinguer Liquid Modernity de Liquid Life / La vie liquide. Ne pas écrire que Joy Division annonce ou illustre directement la modernité liquide. Croiser avec S29, S34 et S36 pour éviter les effets de grande théorie totalisante."
}
```

## 6. Risques de confusion

1. Ne pas utiliser S39 comme source historique sur Manchester, Salford, Factory Records, Ian Curtis ou les années 1970.
2. Ne pas confondre *Liquid Modernity* (2000) avec *Liquid Life* / *La vie liquide* (2005/2006).
3. Ne pas faire de Bauman une explication directe de Joy Division : son usage est rétrospectif et analytique.
4. Ne pas importer mécaniquement la notion de liquidité dans tous les chapitres.
5. Ne pas remplacer les sources musicales, biographiques ou historiques par un cadre sociologique général.
6. Croiser S39 avec S29, S34 et S36 afin d’éviter les effets de grande théorie totalisante.

## 7. Consignes pour les futurs atomes

Les atomes S39 doivent rester peu nombreux, conceptuels et strictement cadrés. Ils servent le livre comme appui théorique, non comme preuve historique sur Joy Division.

Atomes prioritaires recommandés :

```text
S39-A001 — S39 comme source théorique, non source Joy Division
S39-A002 — Modernité liquide : dissolution des cadres stables
S39-A003 — Fragilité des liens sociaux et précarité des appartenances
S39-A004 — Usage rétrospectif : Bauman comme horizon contemporain de réception
S39-A005 — Prudence anti-anachronique : ne pas faire parler 1979 avec 2000 sans médiation
S39-A006 — Patrimonialisation liquide : circulation diffuse du mythe Joy Division
S39-A007 — Permanence paradoxale : un groupe fixe dans une modernité instable
```

Bloc d’usage recommandé :

```yaml
source_id: S39
source_label: "S39 — Bauman, Liquid Modernity, 2000"
preuve: "source secondaire théorique / sociologie de la modernité"
usage: "modernité liquide, dissolution des cadres stables, mobilité, incertitude, fragilité des appartenances, réception contemporaine"
prudence: "ne pas utiliser comme source historique ou musicale ; employer Bauman comme cadre rétrospectif ; distinguer Liquid Modernity de La vie liquide"
```

Formules utilisables :

```text
modernité liquide
fragilité des appartenances
instabilité des cadres sociaux
dissolution des formes durables
réception contemporaine liquéfiée
patrimonialisation diffuse
```

Formules à proscrire :

```text
Bauman explique Joy Division
Joy Division annonce la modernité liquide
Curtis chante la modernité liquide
Manchester est une ville liquide
Liquid Modernity prouve le sens profond de Joy Division
```

## 8. Application au registre

Le patch opérationnel est conservé dans :

```text
sources/bauman_liquid_modernity/registre_patch_s39.json
```

Le script d’application est :

```text
tools/apply_s39_registre_patch.py
```

Il remplace l’entrée S39 existante dans `data/registre.json` par l’entrée canonique ci-dessus, en conservant l’ordre du registre.
