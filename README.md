# Joy Division — AI Writing Studio

## Registre Excel

Le registre des sources peut être maintenu dans Excel, puis converti en JSON pour l’application.

### Conversion

```bash
pip install openpyxl
python tools/convert_registre_xlsx.py mon_registre.xlsx
```

Le fichier `data/registre.json` est alors mis à jour automatiquement.

---

## Audit de chapitre

Le mode "Rédaction chapitre complet" permet désormais une production complète contrôlée.

Une prochaine version intégrera un audit automatique des chapitres.
