# Politique de gel des schémas

## Objet

Le repo entre dans une phase de stabilisation.

Les schémas documentaires doivent désormais être considérés comme critiques.

Toute modification de schéma produit potentiellement :

- incompatibilités ;
- dette documentaire ;
- fragilité des automatisations ;
- incohérences silencieuses.

---

# 1. Principe général

Les schémas doivent désormais évoluer lentement.

Toute modification doit respecter :

```text
compatibilité
stabilité
traçabilité
lisibilité
```

---

# 2. Modifications interdites sans nécessité forte

- suppression d’un champ structurant ;
- renommage d’identifiants ;
- changement de logique documentaire ;
- duplication de schémas concurrents.

---

# 3. Modifications autorisées

- ajout prudent de champs optionnels ;
- amélioration des diagnostics ;
- enrichissements rétrocompatibles ;
- documentation.

---

# 4. Procédure recommandée

Avant toute modification :

- vérifier les impacts ;
- vérifier les exports ;
- vérifier les parseurs ;
- vérifier les registres ;
- vérifier les prompts.

---

# 5. Doctrine importante

Le repo doit désormais privilégier :

```text
solidité documentaire
```

plutôt que :

```text
innovation permanente
```

---

# 6. Critère de maturité

Le système devient mature lorsque :

- les schémas cessent de changer ;
- les nouveaux contenus entrent naturellement dans le système ;
- les automatisations restent stables ;
- les prompts deviennent réutilisables sans ajustement structurel.
