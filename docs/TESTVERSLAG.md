# Testverslag — Luminosity OS

> Hoort bij de Trello-kaarten **TEST-D1/D2/D3**, **TEST-T1/T2** en **TEST-G1**.
> Laatst bijgewerkt: 30 juni 2026 · **46 tests, allemaal geslaagd** · totale dekking 73%.

## 1. Hoe draai je de tests?

```bash
pip install -e ".[dev]"      # of: pip install pytest pytest-cov
pytest                       # alle tests
pytest --cov=luminosity_engine --cov=modules --cov-report=term-missing
```

De volledige uitvoer staat in [`dist/coverage-report.txt`](../dist/coverage-report.txt).

## 2. Dekking per module

| Module | Dekking | Opmerking |
|---|---:|---|
| `translator.py` (US1) | 95% | vertaalregels |
| `safety.py` (US3) | 100% | blokkeren + waarschuwen |
| `confirm.py` (US2) | 100% | bevestiging bouwen |
| `engine.py` | 93% | routering, uitvoeren, logging |
| `ongedaan.py` (US9) | 100% | ongedaan-suggestie |
| `widgets.py` (US7) | 100% | statuswidgets |
| `modules/netwerk.py` (US11) | 100% | nmcli-vertaling |
| `modules/backup.py` (US12/13) | 100% | rsync-vertaling |
| `cli.py` | 0%* | *getest via subprocess (test_shell_cli), niet via import* |

## 3. Testcases (overzicht)

### Vertaler — TEST-D1 (`tests/test_translator.py`, 8)
| Testcase | Invoer | Verwacht |
|---|---|---|
| installeer | "installeer firefox" | `sudo pacman -S firefox` |
| installeer met extra woorden | "installeer firefox alsjeblieft" | naam = firefox |
| update | "update mijn systeem" | `sudo pacman -Syu` |
| verwijder | "verwijder spotify" | `sudo pacman -R spotify` |
| schijfruimte | "hoeveel ruimte heb ik" | `df -h` |
| onbekend / leeg / zonder naam | randgevallen | nette melding, niet uitvoerbaar |

### Veiligheidslaag — TEST-D2 (`tests/test_safety.py`, 6)
| Testcase | Invoer | Verwacht |
|---|---|---|
| rm -rf / | `rm -rf /` | **geblokkeerd** |
| fork-bomb | `:(){ :|:& };:` | **geblokkeerd** |
| mkfs | `mkfs.ext4 …` | **geblokkeerd** |
| normaal commando | `df -h` | veilig |
| verwijderen / shutdown | risicovol | **waarschuwing** (mag wel, extra bevestiging) |

### Engine & logboek (`tests/test_engine.py`, 7)
Veilige opdracht mag uit; gevaarlijke wordt geblokkeerd; geslaagd/mislukt/geannuleerd/geblokkeerd
worden correct in het **logboek (US8)** geschreven; ruwe fouten worden begrijpelijk vertaald (VERB-D1).

### Module-integratie — TEST-G1 (`tests/test_modules.py` 7 + `tests/test_integration.py` 5)
Netwerk (lijst/status/verbinden) en back-up (maken/terugzetten) vertalen correct; en — belangrijk —
ze lopen **door de hele engine-pipeline**: herstel vraagt een extra bevestiging, pakketbeheer heeft
voorrang op de modules, onbekende opdrachten zijn niet uitvoerbaar.

### Schil-CLI — TEST-T1 (`tests/test_shell_cli.py`, 4)
De JSON-interface die de Quickshell-schil aanroept: `--json` levert een bevestiging zonder iets uit te
voeren; `--run` voert uit en logt; `--cancel` logt een annulering; het logboek is leeg bij de start.

### US9 ongedaan maken (`tests/test_ongedaan.py`, 5)
Installatie ⇄ verwijdering wordt correct omgekeerd; systeemupdate, schijfopvraag en een leeg commando
geven géén ongedaan-suggestie.

### US7 statuswidgets (`tests/test_widgets.py`, 4)
Schijfpercentage ligt tussen 0–100; `verzamel()` levert de verwachte velden; de tijd heeft het formaat
`UU:MM`; de schijftekst is leesbaar.

## 4. Wat niet automatisch getest is (eerlijk vermeld)
- **De QML-schil zelf** rendert niet headless; de logica erachter is getest via de CLI-interface en het
  demo-harnas `luminosity-shell/demo_shell.py` (scenario's: simpel, fout, geannuleerd).
- **De ISO-boot** wordt niet als unittest gedraaid; daarvoor is `iso/test-qemu.sh` en de
  GitHub Actions boot-test (`.github/workflows/build-iso.yml`).
