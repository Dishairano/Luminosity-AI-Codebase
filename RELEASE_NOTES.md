# Luminosity OS v0.1.0 — "Luminosity OS Alpha"

**Datum:** 9 juni 2026

Luminosity OS is een op **Arch Linux** gebaseerd besturingssysteem dat je
**volledig in gewone taal** bedient. Je typt wat je wilt — "installeer firefox",
"maak een back-up van mijn documenten", "verbind met wifi" — en een **lokale,
offline taal-engine** zet dat om naar het juiste Linux-commando, legt uit wat er
gebeurt, vraagt bevestiging en voert het pas dáárna uit.

## Hoogtepunten

- **Offline taal-engine** (géén cloud-AI, géén API-sleutel, géén internet):
  installeren, verwijderen, updaten, schijfruimte en systeemstatus.
- **Veiligheidslaag** die gevaarlijke commando's blokkeert (`rm -rf /`,
  fork-bomb, `mkfs`, `dd`) en waarschuwt bij risicovolle acties.
- **Uitleg + bevestiging** vóór elke uitvoering; niets gebeurt zonder akkoord.
- **Quickshell-schil** (QML op Hyprland): invoerbalk, bevestigingskaart,
  Uitvoeren/Annuleren-knoppen, statuswidget, resultaatvenster en logboekpaneel.
- **Netwerk-/wifibeheer** (nmcli) en **back-up/herstel** (rsync) — volledig
  geïntegreerd in dezelfde veilige pipeline.
- **Logboek** van elke opdracht (geslaagd / mislukt / geannuleerd / geblokkeerd).

## Downloads

| Bestand | Grootte | Beschrijving |
|---|---|---|
| `luminosity-0.1.0-x86_64.iso` | ~1,5 GB | Bootbare Arch-gebaseerde live-ISO (BIOS + UEFI) |

> De ISO wordt gebouwd via een Arch Linux Docker-container (`iso/build-docker.sh`)
> of automatisch via GitHub Actions (zie `.github/workflows/build-iso.yml`), die
> hem bij deze release publiceert.

## Tests

37 pytest-tests slagen (engine, modules, integratie en de schil-CLI). Zie
`dist/coverage-report.txt`. Kernlogica: engine 93%, modules 100%.

## Bekende beperkingen (eerlijk)

- **Geen echte boot-testresultaten op hardware.** De ISO is gevalideerd als
  geldige ISO9660-image en via build-logs; booten test je reproduceerbaar met
  `iso/test-qemu.sh` (QEMU).
- **`quickshell` komt uit de AUR**, niet uit de officiële repos. De build bouwt
  het apart; lukt dat niet, dan start het OS via een nette terminal-terugval
  (`/usr/local/bin/luminosity-shell`) in plaats van de grafische schil.

## Installeren / proberen

```bash
# ISO op een USB zetten (vervang sdX door je USB-stick):
sudo dd if=luminosity-0.1.0-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync

# Of testen in QEMU:
cd iso && ./test-qemu.sh
```

Zie `BUILDING.md` voor bouwen en testen, en `CHANGELOG.md` voor alle wijzigingen.
