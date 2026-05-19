# Luminosity OS — Projectstatusrapport (Fase 1: Analyse)

> Bron-volgorde van analyse: **1. Trello** (bron van waarheid) → **2. Codebase** → **3. Documentatie**.
> Opgesteld onder één eerlijke git-identiteit (`Luminosity Bot <luminosity@local>`); teamleden worden
> alleen in Trello, documentatie en `CONTRIBUTORS.md` genoemd, niet in git-authorship.

## 1. Wat is Luminosity OS?

Een op **Arch Linux** gebaseerde distributie die je **volledig in gewone taal** bedient. De gebruiker
typt bijvoorbeeld "installeer firefox" of "maak een back-up van mijn documenten". Een **lokale, offline
regel-/patroonengine** (géén cloud-AI, géén API-sleutel, géén internet) zet dat om naar het juiste
Linux-commando, legt uit wat er gebeurt, vraagt bevestiging en voert het pas dáárna uit. De grafische
schil is gebouwd in **Quickshell (QML)** op **Hyprland**.

## 2. Team & verdeling (uit Trello + docs)

| Persoon | Trello-account | Verantwoordelijkheid | Trello-kaarten |
|---|---|---|---|
| **Dishairano** | Dishairano de Boer | Taal-engine, veiligheidslaag, ISO/infra | ONT-D1/D2, OS1, US1–US4, US6, US7, US9, OS4, TEST-D1/D2/D3, VERB-D1/D2 |
| **Kenji** | kenji vliet | Quickshell-schil + logboek | ONT-T1, ONT-K1, OS2, OS3, US5, US8, TEST-T1/T2, VERB-T1 |
| **Vinicius** | Polsvini0 | Netwerk-/wifibeheer + back-up | ONT-G1/G2, US11, US12, US13, TEST-G1, VERB-G1 |

## 3. Status per feature (Trello → code)

Trello-borden: **Backlog** (34), **To do** (0), **Doing** (2: ONT-G1, ONT-G2), **Done** (0).
De code in deze repo is verder dan het bord suggereert; hieronder de feitelijke stand.

| User story | Omschrijving | Code aanwezig? | Stand |
|---|---|---|---|
| US1 | Taal → commando | `luminosity_engine/translator.py` | ✅ werkend (install/remove/update/schijf/status) |
| US2 | Uitleg + bevestiging | `luminosity_engine/confirm.py` | ✅ werkend |
| US3 | Veiligheidslaag | `luminosity_engine/safety.py` | ✅ werkend (blokkeer + waarschuw) |
| US4/US6 | Software installeren/verwijderen/updaten | translator + pacman | ✅ werkend |
| US7 | Schijfruimte + systeemstatus | translator (`df -h`, `uname`) | ✅ engine; ⚠️ UI-widgets nog niet |
| US8 | Logboek | `luminosity_engine/logbook.py` | ✅ engine; ⚠️ UI-paneel nog niet |
| US5 | Quickshell-schil | `luminosity-shell/qml/shell.qml` | ⚠️ skelet: invoer + kaart, **geen knoppen/logboek** |
| US11 | Netwerk/wifi | `modules/netwerk.py` | ⚠️ module bestaat, **niet in pipeline** |
| US12/US13 | Back-up/herstel | `modules/backup.py` | ⚠️ module bestaat, **niet in pipeline** |
| US9 | 'Ongedaan maken'-suggestie | — | ❌ nog niet |
| OS1–OS4 | Arch-basis, Hyprland, schil-autostart, ISO | `iso/` (archiso-profiel) | ⚠️ config aanwezig, ISO nog niet gebouwd |
| TEST-* | pytest | `tests/test_translator.py`, `test_safety.py` | ⚠️ alleen engine; modules/shell ontbreken |

## 4. Architectuur

### 4.1 De pipeline (kern van het systeem)

```
gewone taal
   │
   ▼
[translator]  US1  ── herkent bedoeling via patronen → Vertaling(commando, uitleg, soort)
   │
   ▼
[safety]      US3  ── controleert commando → Veiligheidsoordeel(veilig/geblokkeerd/reden)
   │
   ▼
[confirm]     US2  ── bouwt Bevestiging(titel, commando, uitleg, mag_uitvoeren, extra_waarschuwing)
   │                  ⟵ engine.verwerk() stopt HIER; er wordt nog niets uitgevoerd
   ▼
gebruiker bevestigt in de schil (Uitvoeren / Annuleren)
   │
   ▼
[engine.voer_uit]  ── voert uit via subprocess (alleen als mag_uitvoeren) → Uitvoerresultaat
   │
   ▼
[logbook]     US8  ── schrijft {id, invoertekst, commando, status, tijdstip} naar JSON
```

**Veiligheidsprincipe:** `engine.verwerk()` voert nooit iets uit; het bereidt alleen de bevestiging
voor. Pas na expliciete bevestiging roept de schil `engine.voer_uit()` aan. Geblokkeerde of
niet-herkende opdrachten bereiken `subprocess` nooit.

### 4.2 Componenten

| Laag | Map | Taal | Rol |
|---|---|---|---|
| Schil (UI) | `luminosity-shell/` | QML/Quickshell | Invoer, bevestigingskaart, knoppen, logboek; roept engine-CLI aan |
| Engine | `luminosity_engine/` | Python | Vertaler, veiligheid, bevestiging, uitvoering, logboek, CLI |
| Modules | `modules/` | Python | Domeinspecifiek: netwerk (nmcli), back-up (rsync) |
| OS/ISO | `iso/` | archiso/bash | Bootbare Arch-ISO met Hyprland-autostart van de schil |

**Integratiekeuze (optie A):** de QML-schil communiceert met de engine via de CLI
(`python -m luminosity_engine.cli`), niet via een ingebedde interpreter. Eenvoudig, taalonafhankelijk
en goed testbaar.

### 4.3 Belangrijkste tekortkoming gevonden in Fase 1

De `modules/` (netwerk, back-up) leveren wél een commando + uitleg, maar worden **nergens door de engine
aangeroepen**. Daardoor lopen netwerk- en back-up-acties nu niet door de veiligheids- en logboeklaag.
Dit is het kernpunt van **Fase 3 (module-integratie)**.

## 5. Roadmap

| Fase | Doel | Branch | Definition of Done |
|---|---|---|---|
| **1. Analyse** | Status, architectuur, roadmap | — | Dit rapport ✅ |
| **2. Quickshell UI** | Werkende schil + engine-integratie | `feature/quickshell-ui` | Execute/Cancel-knoppen, statuswidgets, logboekpaneel, output-rendering; 3 testopdrachten (simpel, fout, geannuleerd) zichtbaar in UI + logboek |
| **3. Module-integratie** | Modules via volledige pipeline | `feature/module-integration` | Netwerk- én back-upmodule lopen via engine (vertaling→veiligheid→bevestiging→uitvoering→logging) |
| **4. ISO-build** | Bootbare Arch-ISO | `feature/iso-build` | ISO gegenereerd via Arch-Docker + archiso; build-log; werkend QEMU-testscript |
| **5. Testing** | Volledige testdekking | `feature/testing` | Engine-, module- én shell-tests slagen; coverage-rapport |
| **Release** | Oplevering | `main` | Branches gemerged, tests groen, ISO-build, QEMU-script, CHANGELOG/RELEASE_NOTES/CONTRIBUTORS/BUILDING, tag `v0.1.0` |

## 6. Beperkingen (eerlijk vermeld)

- **Geen echte hardware/VM-boot.** Er worden geen echte boot-testresultaten gegenereerd; in plaats
  daarvan: build-logs, een QEMU-testscript en reproduceerbare stappen.
- **Quickshell zit in de AUR**, niet in de officiële Arch-repos. De ISO-build bouwt het apart in een
  Arch-container; lukt dat in een omgeving niet, dan bouwt de rest van de ISO door en wordt het pakket
  handmatig toegevoegd (gedocumenteerd in `BUILDING.md`).
- **Quickshell-runtime niet lokaal beschikbaar**, dus de QML-schil wordt niet visueel gerenderd in deze
  omgeving. De engine-integratie wordt aangetoond via de CLI/JSON-interface die de schil aanroept.
