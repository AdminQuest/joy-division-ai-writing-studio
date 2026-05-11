# Graphe documentaire

Le repo entre désormais dans une phase relationnelle.

Les atomes ne doivent plus seulement exister comme fragments isolés.

Ils doivent expliciter leurs relations.

Objectif :

```text
passer d’un corpus hiérarchique
à un système relationnel historiographique.
```

---

# 1. Principe fondamental

Chaque atome peut désormais entretenir des relations typées avec :

- d’autres atomes ;
- des concepts ;
- des citations ;
- des mythes ;
- des controverses.

Les relations deviennent des unités documentaires explicites.

---

# 2. Champ relationnel

Champ recommandé :

```yaml
relations:
```

Structure :

```yaml
relations:
  - type: soutient
    cible: S41-A018

  - type: nuance
    cible: S45-A011

  - type: contredit
    cible: S46-A004

  - type: derive_de
    cible: CONCEPT-001
```

---

# 3. Relations autorisées

## Relations argumentatives

```text
soutient
nuance
contredit
complète
illustre
```

---

## Relations conceptuelles

```text
derive_de
prolonge
réinterprète
théorise
```

---

## Relations historiographiques

```text
mythologise
corrige
reconstruit
simplifie
```

---

## Relations mémorielles

```text
témoigne
se_souvient
reformule
```

---

# 4. Objectifs stratégiques

Le graphe documentaire doit permettre :

- détection des chaînes argumentatives ;
- repérage des dépendances théoriques ;
- cartographie des mythes ;
- visualisation des controverses ;
- propagation conceptuelle ;
- recherche sémantique avancée.

---

# 5. Exemple critique — Ian Curtis

Le graphe doit permettre de distinguer explicitement :

- fait historique ;
- mémoire de Hook ;
- reconstruction journalistique ;
- lecture critique ;
- mythologie postérieure.

Le repo pourra alors raisonner historiographiquement.

---

# 6. Doctrine importante

Toutes les relations ne se valent pas.

Une relation :

```text
soutient
```

n’a pas le même poids qu’une relation :

```text
mythologise
```

Le graphe doit donc rester interprétable historiographiquement.

---

# 7. Évolution future

Le graphe documentaire prépare :

- visualisations réseau ;
- clusters thématiques ;
- scoring historiographique ;
- propagation automatique ;
- moteur RAG relationnel.
