# Changelog

Alle noemenswaardige wijzigingen aan Luminosity OS. Het formaat volgt
[Keep a Changelog](https://keepachangelog.com/) en de versies volgen
[Semantic Versioning](https://semver.org/lang/nl/).

## [0.1.0] — 2026-06-09 — "Luminosity OS Alpha"

Eerste alpha: een werkende offline taal-engine, een Quickshell-schil en een
bootbare Arch-gebaseerde ISO.

### Toegevoegd
- **Taal-engine (offline):** zet gewone taal om naar pacman-commando's
  (installeren, verwijderen, updaten, schijfruimte, systeemstatus) — US1, US4,
  US6, US7.
- **Veiligheidslaag:** blokkeert gevaarlijke commando's (`rm -rf /`, fork-bomb,
  `mkfs`, `dd` naar schijf) en waarschuwt bij risicovolle acties — US3.
- **Bevestiging:** elke opdracht toont eerst uitleg + commando en wordt pas na
  bevestiging uitgevoerd — US2.
- **Logboek:** elke opdracht (geslaagd/mislukt/geannuleerd/geblokkeerd) wordt
  gelogd — US8.
- **Quickshell-schil:** invoerbalk, bevestigingskaart, Uitvoeren/Annuleren-
  knoppen, statuswidget, resultaatvenster en logboekpaneel — US5/US7/US8.
- **JSON-CLI** waarmee de schil de engine aanstuurt (`--json`, `--run`,
  `--cancel`, `--logboek`).
- **Netwerk-/wifibeheer** via `nmcli` — US11.
- **Back-up & herstel** via `rsync`, met extra bevestiging bij terugzetten —
  US12/US13.
- **ISO-build:** archiso-profiel + Docker-build (`build-docker.sh`) voor een
  bootbare Arch-gebaseerde ISO met Hyprland-autostart van de schil — OS1–OS4.
- **QEMU-testscript** (`iso/test-qemu.sh`) en eerlijke schil-terugval zonder
  quickshell.
- **Tests:** pytest voor engine, modules, integratie en de schil-CLI, met een
  coverage-rapport.

### Architectuur
- De modules (netwerk, back-up) lopen nu door dezelfde pipeline als de vertaler:
  vertaling → veiligheid → bevestiging → uitvoering → logboek.

### Bekende beperkingen
- Geen echte boot-testresultaten op hardware; alleen build-logs + QEMU-script.
- `quickshell` komt uit de AUR; lukt de build daarvan niet, dan start het OS via
  een terminal-terugval.

[0.1.0]: https://github.com/Dishairano/Luminosity-AI-Codebase/releases/tag/v0.1.0
