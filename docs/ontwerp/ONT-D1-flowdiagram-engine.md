# ONT-D1 — Flowdiagram taal-engine (offline regel-engine)

De kern van Luminosity is een **lokale, offline regel-engine** die gewone taal omzet naar een
Linux-commando en het pas uitvoert ná bevestiging. Geen cloud-AI, geen API-sleutel, geen internet.

Dit flowdiagram toont de volledige pijplijn van invoer tot logboek. Het bewijst het
**veiligheidsprincipe**: `verwerk()` voert nooit iets uit — er gebeurt pas iets na een expliciete
"Uitvoeren" door de gebruiker.

```mermaid
flowchart TD
    A([Gebruiker typt gewone taal]) --> B[Vertaler US1<br/>patroon-herkenning]
    B --> C{Herkend?}
    C -- nee --> D[Domeinmodules<br/>netwerk US11 / back-up US12-13]
    D --> E{Herkend?}
    C -- ja --> F
    E -- ja --> F[Veiligheidslaag US3<br/>controleer commando]
    E -- nee --> G[/Nette melding:<br/>'Ik snap deze opdracht nog niet'/]
    F --> H{Oordeel}
    H -- geblokkeerd --> I[/Knop 'Uitvoeren' uit<br/>reden tonen/]
    H -- veilig / waarschuwing --> J[Bevestiging US2<br/>titel, commando, uitleg]
    J --> K([Schil toont bevestigingskaart])
    K --> L{Gebruiker kiest}
    L -- Annuleren --> M[logbook: 'geannuleerd' US8]
    L -- Uitvoeren --> N[voer_uit: subprocess]
    N --> O{Gelukt?}
    O -- ja --> P[logbook: 'geslaagd' US8]
    P --> Q[Ongedaan maken-suggestie US9]
    O -- nee --> R[Begrijpelijke foutuitleg VERB-D1]
    R --> S[logbook: 'mislukt' US8]
    I --> T[logbook: 'geblokkeerd' US8]
```

## Toelichting per stap

1. **Vertaler (US1)** — `luminosity_engine/translator.py`: herkent de bedoeling via trefwoord-patronen
   (installeren, verwijderen, updaten, schijfruimte, status) en bouwt het commando.
2. **Domeinmodules (US11–US13)** — `modules/netwerk.py`, `modules/backup.py`: leveren hun eigen
   commando's; de engine routeert hierheen als de vertaler niets herkent (`engine._vertaal`).
3. **Veiligheidslaag (US3)** — `luminosity_engine/safety.py`: blokkeert gevaarlijke commando's
   (`rm -rf /`, `mkfs`, …) en waarschuwt bij risicovolle.
4. **Bevestiging (US2)** — `luminosity_engine/confirm.py`: bouwt het "wat ga ik doen"-bericht.
5. **Uitvoeren** — pas na akkoord; `engine.voer_uit` draait het commando in een subprocess.
6. **Logboek (US8)** — elke afloop (geslaagd/mislukt/geannuleerd/geblokkeerd) wordt vastgelegd.
7. **Ongedaan maken (US9)** — na succes stelt de engine voor hoe je de actie terugdraait.
