# formlang — squelette étudiant

Complétez les blocs `# TODO (Ex.)` repérés dans `formlang/` et `apps/`.
Chaque TODO renvoie à une question `E...` d'une fiche `docs/jourN_*.md`.

```bash
pip install pytest
pytest -q          # ROUGE au départ ; vire au VERT à mesure que vous complétez
python pipeline.py # démo Shield (après E3.x)
```

Règle d'or : les `apps/` **instancient** les automates de `formlang/`,
elles ne les réécrivent pas. Volet Shield : 100 % structurel, aucun contenu réel.
