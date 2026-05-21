# Luminosity Engine

De lokale, **offline** taal-naar-commando engine van Luminosity OS. Zet gewone taal om naar Linux-
commando's, legt uit wat er gebeurt, blokkeert gevaarlijke commando's en houdt een logboek bij.
Geen cloud-AI, geen API-sleutel, geen internet nodig.

## Onderdelen

| Bestand | User story | Wat het doet |
|---|---|---|
| `translator.py` | US1 | Herkent de bedoeling via patronen en bouwt het commando |
| `safety.py` | US3 | Detecteert en blokkeert gevaarlijke commando's |
| `confirm.py` | US2 | Bouwt de uitleg + bevestigingsvraag (voert niets uit) |
| `logbook.py` | US8 | Schrijft elke opdracht weg (JSON) |
| `engine.py` | — | Knoopt alles aan elkaar; voert pas uit ná bevestiging |
| `cli.py` | — | Terminal-interface om te testen |

## Gebruik

```bash
# Eenmalige opdracht
python -m luminosity_engine.cli "installeer firefox"

# Interactief
python -m luminosity_engine.cli
```

## Voorbeeld

```
> installeer firefox
  Klaar om te installeren
  Commando : sudo pacman -S firefox
  Uitleg   : Ik installeer 'firefox' met de pakketbeheerder pacman.
  Veiligheid: Dit commando is veilig.
  Uitvoeren? (j/n)
```

## Tests

```bash
pytest tests/
```

14 tests dekken de vertaler (taal → commando) en de veiligheidslaag (gevaarlijke commando's).
