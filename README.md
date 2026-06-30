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

## Ontwikkelproces

Hieronder de fasering zoals die echt is gelopen, gebaseerd op de git-historie,
de versietags (`v0.1.0` t/m `v0.3.0`) en de [`CHANGELOG.md`](CHANGELOG.md).

### 1. Analyse (18–29 mei)
Projectopzet en richting bepaald: projectstructuur en commit-richtlijn (PLAN-D),
README met projectoverzicht, en een statusrapport met architectuur en roadmap.
Hier is besloten dat de taal-engine **volledig offline** werkt, zonder cloud-AI.

### 2. Taal-engine — US1, US2, US4, US6, US7 (1–2 juni)
De kern: een vertaler die gewone taal omzet naar `pacman`-commando's (US1), een
bevestiging met uitleg vóór uitvoeren (US2) en het logboek dat elke opdracht als
JSON bewaart (US8). De pipeline knoopt vertaling, veiligheid, bevestiging en
uitvoering aaneen, met een CLI om de engine te proberen.

### 3. Veiligheid — US3 (1–5 juni)
Een veiligheidslaag die gevaarlijke commando's blokkeert (US3). Later uitgebreid
zodat ook netwerk- en back-upacties als gevaarlijk gemarkeerd kunnen worden en de
bevestiging dan extra akkoord vraagt (US13).

### 4. Schil + logboek — US5, US8 (4–5 juni)
Het Quickshell/QML-skelet van de schil (OS3/US5): invoerbalk, bevestigingskaart,
Uitvoeren/Annuleren, een statuswidget en een logboekpaneel. Een JSON-CLI laat de
schil de engine aansturen; annuleren wordt gelogd (US8).

### 5. Modules netwerk/back-up + integratie — US11, US12, US13 (3–5 juni)
Netwerk-/wifibeheer via `nmcli` (US11) en back-up maken/terugzetten via `rsync`
(US12/US13), als losse modules in `modules/`. De engine routeert deze door
dezelfde pipeline, inclusief de veiligheidsmarkering van een terugzet-actie.

### 6. Testen (3–8 juni)
Tests voor de vertaler, de veiligheidslaag, de engine-integratie, de netwerk- en
back-upherkenning en de JSON-CLI van de schil (TEST-D1/D2/D3, TEST-G1, TEST-T1),
met een coverage-rapport. GitHub Actions draait de suite bij elke push.

### 7. ISO-build — OS1–OS4 (6–11 juni, v0.1.0 → v0.2.11)
Het archiso-profiel (profiledef, packages, pacman.conf), de build-scripts (ook via
Docker), een QEMU-testscript en CI die de ISO bouwt en bij een release publiceert
(OS4). Daarna een lange reeks fixes richting een betrouwbaar bootbare ISO en een
grafische installer met de Lumo-mascotte: software-GL-terugval, schil als
onbevoorrechte gebruiker, custom Plymouth boot-splash, responsive installer,
installatie altijd als root, en — als sluitstuk — installs die in zowel BIOS- als
UEFI-modus booten (`v0.2.11`).

### 8. Afronding — US9 + statuswidgets + ontwerp + testverslag (30 juni, v0.3.0)
De laatste user stories en documentatie: de **'Ongedaan maken'-suggestie** (US9),
**echte statuswidgets** met live schijfruimte en klok (US7), de zes
**ontwerpdocumenten** in [`docs/ontwerp/`](docs/ontwerp/) (flowdiagram taal-engine,
ERD logboek, flowchart back-up/herstel, wireframes schil/invoerbalk/netwerk) en een
leesbaar **testverslag** ([`docs/TESTVERSLAG.md`](docs/TESTVERSLAG.md)). De
testsuite staat op **46 tests**. Dit is release `v0.3.0`.

> **US10** (betaalde abonnementen) valt buiten scope en blijft *Won't*.
