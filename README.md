# Luminosity OS — Codebase

De code van **Luminosity OS**: een Arch-gebaseerd besturingssysteem dat je in gewone taal bedient.

| Map | Module | Persoon |
|---|---|---|
| `luminosity_engine/` | Taal-engine (taal → commando, veiligheid, logboek) | Dishairano |
| `luminosity-shell/` | Quickshell/QML schil (de UI) | Kenji |
| `modules/` | Netwerk-/wifibeheer + back-up | Vinicius |
| `iso/` | archiso-config voor de bootbare ISO | Dishairano |
| `tests/` | pytest-tests | — |

De engine werkt **volledig offline**, zonder cloud-AI of API-sleutel.

## Snel proberen (engine)

```bash
python -m luminosity_engine.cli "installeer firefox"
pytest tests/
```

Zie [`dist/HOE-COMMITTEN.md`](dist/HOE-COMMITTEN.md) voor hoe ieder zijn eigen deel commit.
