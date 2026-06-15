# Changelog

Alle noemenswaardige wijzigingen aan Luminosity OS. Het formaat volgt
[Keep a Changelog](https://keepachangelog.com/) en de versies volgen
[Semantic Versioning](https://semver.org/lang/nl/).

## [0.2.1] — 2026-06-09

### Toegevoegd
- **Geautomatiseerde boot-test in CI**: de GitHub Actions-workflow boot elke
  gebouwde ISO headless in QEMU en bevestigt dat de live-omgeving en de
  installer-backend opkomen (markering via de seriële poort). De seriële log
  wordt als artifact bewaard.

### Gewijzigd
- De installer-server draait nu als **systemd-service**
  (`luminosity-installer.service`), losgekoppeld van de Hyprland-schil — robuuster
  en headless testbaar. De kiosk-launcher opent alleen nog de browser (met
  fallback als de service nog niet luistert).

## [0.2.0] — 2026-06-09 — "Luminosity OS Installer"

De live-ISO boot nu in een grafische installer in plaats van direct in de schil.

### Toegevoegd
- **Grafische installer** (`iso/installer/`): een kiosk-webinterface met de
  mascotte "Lumo", stappen voor taal, licentie, schijf, schijf-indeling,
  account, regio, stijl (live accentkleur + donkere/lichte modus), overzicht en
  een geanimeerde installatievoortgang.
- **Lokale install-server** (`server.py`): serveert de UI en biedt `/api/disks`,
  `/api/install` (streamt voortgang via Server-Sent Events) en `/api/reboot`.
- **Arch-installatiescript** (`install.sh`): partitioneren → pacstrap →
  chroot-configuratie (account, tijdzone, locale, autostart) → systemd-boot →
  Luminosity-engine/schil plaatsen op het doelsysteem.
- **Kiosk-autostart**: de live-ISO start de installer fullscreen (Chromium op
  Hyprland); `SUPER+L` om de schil te proberen, `SUPER+RETURN` voor een terminal.

### Gewijzigd
- ISO-pakketten uitgebreid met `chromium`, `gptfdisk`, `dosfstools`, `parted`,
  `arch-install-scripts`.
- QEMU-testscript gebruikt `virtio-vga-gl` zodat Hyprland (Wayland) rendert.
- ISO-builds verlopen voortaan via GitHub Actions, met release op een versietag.

### Bekende beperkingen
- `install.sh` is niet op echte hardware uitgevoerd (geen doel-schijf/boot in de
  ontwikkelomgeving); test in een VM met een lege schijf.

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
