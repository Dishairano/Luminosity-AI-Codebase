# Changelog

Alle noemenswaardige wijzigingen aan Luminosity OS. Het formaat volgt
[Keep a Changelog](https://keepachangelog.com/) en de versies volgen
[Semantic Versioning](https://semver.org/lang/nl/).

## [0.3.0] — 2026-06-30

### Toegevoegd
- **US9 — 'Ongedaan maken'-suggestie.** Na een geslaagde opdracht stelt Luminosity
  voor hoe je die terugdraait (een installatie ⇄ een verwijdering). De suggestie
  wordt niet automatisch uitgevoerd maar opnieuw als opdracht aangeboden, zodat ze
  weer langs de veiligheids- en bevestigingslaag gaat. Zichtbaar in de schil en de
  CLI. (`luminosity_engine/ongedaan.py`, `tests/test_ongedaan.py`)
- **US7 — echte statuswidgets.** De bovenbalk van de schil toont nu live
  schijfruimte en klok in plaats van vaste plaatjes. Nieuwe `--widgets`-CLI levert
  de gegevens. (`luminosity_engine/widgets.py`, `tests/test_widgets.py`)
- **Ontwerpdocumenten (ONT-kaarten)** in `docs/ontwerp/`: flowdiagram van de
  taal-engine, ERD van het logboek, flowchart van het back-up-/herstelproces, en
  wireframes van de schil, de invoerbalk en de netwerk-/back-upschermen.
- **Leesbaar testverslag** (`docs/TESTVERSLAG.md`) met een testcases-tabel.
- **VERB-G1 — netwerk/back-up-verbeteringen** (o.b.v. feedback): wifi aan/uit zetten
  en een opgeslagen netwerk vergeten; back-uplocatie instelbaar via
  `LUMINOSITY_BACKUP_DIR` en keuze van map (documenten, foto's, downloads, muziek…)
  i.p.v. alleen Documenten. (`modules/netwerk.py`, `modules/backup.py`)
- **VERB-T1 — UX-verbeteringen schil** (o.b.v. testgebruikers): automatische focus op
  de invoerbalk, een placeholder-hint, Esc om te wissen, en een vriendelijke lege-staat
  in het logboek. (`luminosity-shell/qml/shell.qml`)

### Gewijzigd
- Testsuite uitgebreid naar **51 tests** (was 37); engine 93%, modules 100%,
  ongedaan/widgets 100%.

## [0.2.11] — 2026-06-11

### Opgelost
- **Geïnstalleerd systeem boot nu in zowel BIOS- als UEFI-modus** (bug #1). De
  installer detecteert de firmware-modus en schrijft de juiste bootloader:
  systemd-boot bij UEFI, GRUB bij BIOS. De schijf krijgt een layout die beide
  ondersteunt (1 MiB BIOS-boot + EFI-partitie + root), zodat een install niet
  langer onbootbaar is wanneer de machine in BIOS/legacy-modus draait.

## [0.2.10] — 2026-06-11

### Opgelost
- **Installer: "Volgende" werkt nu direct bij de account-stap.** De knop wordt
  live bijgewerkt terwijl je typt; je hoeft niet meer eerst terug.
- **Installer: "Schijf /dev/None bestaat niet" verholpen.** Schijven met een
  spatie in de modelnaam (bv. VirtualBox "VBOX HARDDISK") werden gemist door de
  kolom-parsing; nu wordt `lsblk --json` gebruikt. Bovendien blokkeert de wizard
  "Volgende" als er geen schijf is, en weigert `install.sh` een lege schijfnaam.

### Verbeterd
- **Boot-splash herzien**: schaalt nu mee met elke resolutie (relatieve maten en
  uitlijning), met een verzorgder ontwerp (sterren, fijnere voortgangsring,
  leesbare typografie) dat beter bij de installer-stijl past.

## [0.2.9] — 2026-06-11

### Opgelost
- **Geen Hyprland-standaardwallpaper meer vóór de installer.** In het korte
  moment tussen het opkomen van de schil en het laden van de kiosk verscheen de
  standaard-wallpaper/het logo van Hyprland. Die zijn nu uitgeschakeld
  (`force_default_wallpaper=0`, `disable_hyprland_logo`); de achtergrond is onze
  donkere themakleur (#0a0c12), zodat de overgang van splash naar installer
  naadloos is.

## [0.2.8] — 2026-06-11

### Opgelost
- **"De installer moet als root draaien" verholpen.** Door een opstart-race kon
  de installer-server als gebruiker `lumo` starten i.p.v. als root, waardoor de
  installatie weigerde. Nu wacht de kiosk eerst op de root-systemd-service, en
  draait `server.py` het installatiescript en de herstart sowieso via `sudo`
  wanneer hij niet als root loopt — dus de installatie krijgt altijd root-rechten.

## [0.2.7] — 2026-06-11

### Opgelost / Verbeterd
- **Installer schaalt nu mee met elke schermresolutie.** De wizard is volledig
  responsive: op lage of kleine resoluties (zoals in een VM) vult hij het scherm,
  de zijbalk klapt in op smalle schermen en de inhoud wordt compacter op lage
  schermen i.p.v. afgesneden te worden.
- Hyprland kiest nu de **hoogst beschikbare resolutie** (`monitor=,highres,auto,1`),
  zodat de installer meer ruimte krijgt op VM's met een lage standaardresolutie.

## [0.2.6] — 2026-06-10

### Opgelost
- **Hyprland-crash ("Aborted") in VirtualBox verholpen — met behoud van
  hardware-versnelling.** De schil probeert nu eerst hardware-GL (GPU-versnelling
  op alle systemen die het ondersteunen, inclusief VM's met werkende 3D). Crasht
  Hyprland op een kapotte gast-GL (o.a. VirtualBox VMSVGA), dan herstart de schil
  automatisch met Mesa software-GL (llvmpipe) als nette terugval. Geen
  GPU-versnelling opofferen waar het wél werkt.

## [0.2.5] — 2026-06-10

### Toegevoegd
- **Custom grafische boot-splash (Plymouth)** in Luminosity-stijl: "Grote
  zonsopkomst" — een warme gloed die van onderaf opkomt, de ☀ Lumo-mascotte met
  draaiende stralen en een voortgangsring, het "Luminosity OS"-wordmark en een
  leesbare "OPSTARTEN…". Verbergt de kernel-/boottekst (`quiet splash`).
  De splash draagt naadloos over aan de schil (`plymouth quit --retain-splash`).
  Assets worden gegenereerd door `iso/plymouth/gen_assets.py`; HTML-mockup in
  `iso/installer/web/bootsplash.html`.

## [0.2.4] — 2026-06-10

### Gewijzigd
- **De ISO start direct door naar Luminosity** — geen 15 seconden-bootmenu meer.
  Zowel syslinux (BIOS) als systemd-boot (UEFI) en grub starten nu meteen de
  standaard-optie (timeout ~0).
- Het bootmenu en de boot-opties heten nu **"Luminosity OS"** in plaats van
  "Arch Linux install medium".

## [0.2.3] — 2026-06-10

### Opgelost
- **Zwart scherm bij het opstarten verholpen.** De grafische sessie draaide als
  root, en Hyprland (en Chromium) weigeren als root te starten — vandaar het
  zwarte scherm. De live-ISO logt nu automatisch in als onbevoorrechte gebruiker
  `lumo` en start de schil als die gebruiker. De installatie zelf houdt
  root-rechten via `luminosity-installer.service` (nette scheiding van rechten).
- De CI-boottest verifieert nu expliciet dat de schil **opkomt** (markering
  `LUMINOSITY_GUI_UP` via de seriële poort) en faalt met de reden als Hyprland
  stopt — zodat een release alleen uitgaat als de GUI daadwerkelijk start.

## [0.2.2] — 2026-06-10

### Gewijzigd
- **Werkt nu zonder dedicated GPU / met software-rendering.** De schil (Hyprland)
  staat Mesa's software-GL (llvmpipe) toe als er geen werkende hardware-GL is
  (`WLR_RENDERER_ALLOW_SOFTWARE=1`), zodat de grafische installer/schil ook op
  integrated graphics, zwakke of GPU-loze systemen en in VM's opstart in plaats
  van een zwart scherm. Hardware-GL wordt nog steeds gebruikt indien beschikbaar.
  `WLR_NO_HARDWARE_CURSORS=1` voorkomt cursorproblemen in VM's.

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
