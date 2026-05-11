# Workflow de maintenance

## Objet

Le repo ne doit plus évoluer de manière improvisée.

Ce workflow fixe désormais les opérations régulières de maintenance.

---

# 1. Workflow hebdomadaire

## Étape 1 — Validation documentaire

Lancer :

```bash
python tools/build_registers.py --strict
```

Vérifier :

- erreurs ;
- warnings ;
- compatibilité des schémas.

---

## Étape 2 — Diagnostics historiographiques

Lancer :

```bash
python tools/build_historiographical_diagnostics.py
```

Contrôler :

- atomes fragiles ;
- mythes ;
- risques élevés ;
- densité théorique.

---

## Étape 3 — Graphe documentaire

Lancer :

```bash
python tools/build_graph.py
```

Contrôler :

- relations cassées ;
- nœuds orphelins ;
- incohérences relationnelles.

---

## Étape 4 — Contexte IA

Lancer :

```bash
python tools/build_prompt_context.py
```

Vérifier :

- contraintes historiographiques ;
- warnings ;
- motifs dominants.

---

# 2. Workflow mensuel

## Contrôle de cohérence

Vérifier :

- équilibre des couches narratives ;
- répétitions ;
- stabilité des concepts ;
- stabilité des motifs.

---

## Contrôle documentaire

Vérifier :

- doublons ;
- sources orphelines ;
- citations non vérifiées ;
- atomes incomplets.

---

# 3. Doctrine importante

Le workflow vise désormais à limiter :

- l’entropie documentaire ;
- les dérives structurelles ;
- les incohérences silencieuses.

La stabilité du système devient prioritaire.
