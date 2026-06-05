# Controle M1 - DM vers atomes

Rapport genere par `python3 tools/check_dm_atoms_traceability.py`.

Ce controle est strictement en lecture sur les documents maitres, exports, registres, atomes et manifeste. Il produit des constats et ne corrige aucun ecart.

Limite MVP : le controle verifie les identifiants atomiques explicitement visibles et les volumetries principales. Il ne realise pas de tracabilite passage par passage.

### Résumé global

| Indicateur | Valeur |
|------------|---------|
| Documents declares dans le manifeste | 14 |
| Documents traçables | 14 |
| Documents partiellement traçables | 0 |
| Documents non traçables | 0 |
| Atomes visibles | 2477 |
| Atomes retrouvés | 2477 |
| Identifiants résolus par alias | 9 |
| Écarts détectés | 0 |
| Atomes introuvables | 0 |
| Incohérences de volumétrie | 0 |
| Documents maîtres absents | 0 |
| Manifestes incohérents | 0 |

### Audit par document maître

| DM | Statut | Atomes visibles | Atomes retrouvés | Écarts |
|----|----|----|----|----|
| `chapters/01/document_maitre.md` | traçable | 184 | 184 | Aucun |
| `chapters/02/document_maitre.md` | traçable | 197 | 197 | Aucun |
| `chapters/03/document_maitre.md` | traçable | 171 | 171 | Aucun |
| `chapters/04/document_maitre.md` | traçable | 188 | 188 | Aucun |
| `chapters/05/document_maitre.md` | traçable | 167 | 167 | Aucun |
| `chapters/06/document_maitre.md` | traçable | 223 | 223 | Aucun |
| `chapters/07/document_maitre.md` | traçable | 156 | 156 | Aucun |
| `chapters/08/document_maitre.md` | traçable | 166 | 166 | Aucun |
| `chapters/09/document_maitre.md` | traçable | 121 | 121 | Aucun |
| `chapters/10/document_maitre.md` | traçable | 162 | 162 | Aucun |
| `chapters/11/document_maitre.md` | traçable | 183 | 183 | Aucun |
| `chapters/12/document_maitre.md` | traçable | 194 | 194 | Aucun |
| `chapters/13/document_maitre.md` | traçable | 157 | 157 | Aucun |
| `chapters/14/document_maitre.md` | traçable | 208 | 208 | Aucun |

### Écarts détectés

Aucun écart détecté dans le perimetre MVP.

### Limites observees

- Les documents maitres exposent des atomes visibles, mais pas une table complete passage -> atome.
- Le controle compare la volumetrie `Atomes` du tableau de bord avec `exports/generated/master_docs_index.json`, pas le nombre d'atomes visibles avec le nombre total d'atomes rattaches.
- Les variantes historiques `Sxx-000` et `Sxx-A000` sont resolues comme alias lorsqu'une forme correspond a un atome exporte.
- Certains atomes peuvent etre rattaches au document maitre sans etre affiches dans les sections visibles, ce qui n'est pas traite comme un ecart par le MVP.
- Les sources, registres, citations et exports autres que `atoms.json` et `master_docs_index.json` restent hors perimetre.

### Faux positifs possibles

- Un atome non affiche peut etre volontairement omis par selection redactionnelle.
- Un identifiant visible dans une section de relations peut etre verifie comme atome existant sans prouver qu'il soutient un passage precis.
- Une volumetrie correcte ne prouve pas la derivabilite fine du contenu redactionnel.
- Une absence d'ecart dans ce rapport ne vaut pas validation DM -> sources, DM -> registres ou DM -> exports.
