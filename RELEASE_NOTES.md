# Luminosity OS v0.3.0 — "Alles op een rij"

**Datum:** 30 juni 2026

Luminosity OS is een op **Arch Linux** gebaseerd besturingssysteem dat je **volledig in gewone taal**
bedient. Je typt wat je wilt — "installeer firefox", "maak een back-up van mijn documenten", "verbind
met wifi" — en een **lokale, offline taal-engine** zet dat om naar het juiste Linux-commando, legt uit
wat er gebeurt, vraagt bevestiging en voert het pas dáárna uit. Geen cloud-AI, geen API-sleutel.

Deze release maakt de oorspronkelijke opdracht **compleet**: de laatste twee user stories zijn af en
alle ontwerpdocumenten zijn opgeleverd.

## Nieuw in 0.3.0

- **US9 — 'Ongedaan maken'-suggestie.** Na een geslaagde opdracht stelt Luminosity voor hoe je die
  terugdraait (installeren ⇄ verwijderen). Veilig: de tegenactie gaat opnieuw langs bevestiging.
- **US7 — echte statuswidgets.** De bovenbalk toont nu live schijfruimte en klok in plaats van vaste
  plaatjes (`--widgets`-CLI levert de data).
- **Ontwerpdocumenten** (`docs/ontwerp/`): flowdiagram taal-engine, ERD logboek, flowchart
  back-up/herstel, en wireframes van de schil, invoerbalk en netwerk-/back-upschermen.
- **Testverslag** (`docs/TESTVERSLAG.md`) met een testcases-tabel.

## Sinds v0.1.0 (samengevat)

- **Grafische web-installer** met firmware-bewuste bootloader (BIOS **én** UEFI), schaalbare UI en een
  verzorgde boot-splash — zie de `[0.2.x]`-regels in `CHANGELOG.md`.
- **ISO-pipeline** via GitHub Actions: bouwen → boot-test in QEMU → publiceren bij een versietag.

## Volledige functielijst

- Offline taal-engine: installeren, verwijderen, updaten, schijfruimte, systeemstatus.
- Veiligheidslaag die gevaarlijke commando's blokkeert (`rm -rf /`, fork-bomb, `mkfs`, `dd`) en
  waarschuwt bij risicovolle acties.
- Uitleg + bevestiging vóór élke uitvoering; niets gebeurt zonder akkoord.
- Quickshell-schil (QML op Hyprland): invoerbalk, bevestigingskaart, knoppen, **echte statuswidgets**,
  resultaatvenster, **ongedaan maken** en logboekpaneel.
- Netwerk-/wifibeheer (nmcli) en back-up/herstel (rsync), volledig in dezelfde veilige pipeline.
- Logboek van elke opdracht (geslaagd / mislukt / geannuleerd / geblokkeerd).

## Tests

**46 pytest-tests slagen** (engine, modules, integratie, schil-CLI, ongedaan maken, statuswidgets).
Zie `docs/TESTVERSLAG.md` en `dist/coverage-report.txt`. Kernlogica: engine 93%, modules 100%,
ongedaan/widgets 100%.

## Downloads

| Bestand | Beschrijving |
|---|---|
| `luminosity-0.3.0-x86_64.iso` | Bootbare Arch-gebaseerde live-ISO (BIOS + UEFI) |

> De ISO wordt automatisch gebouwd en gepubliceerd via GitHub Actions
> (`.github/workflows/build-iso.yml`) bij het taggen van deze release.

## Installeren / proberen

```bash
# ISO op een USB zetten (vervang sdX door je USB-stick):
sudo dd if=luminosity-0.3.0-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync

# Of testen in QEMU:
cd iso && ./test-qemu.sh
```

Zie `BUILDING.md` voor bouwen/testen en `CHANGELOG.md` voor alle wijzigingen.
