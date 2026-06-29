# ONT-G1 — Flowchart back-up-/herstelproces (technisch)

De back-up- en herstelmodule (`modules/backup.py`, US12/US13) loopt — net als alles in Luminosity —
door de volledige engine-pijplijn. Het verschil met gewone opdrachten: **terugzetten is gevaarlijk**
(het overschrijft bestaande bestanden), dus de engine markeert herstel als `gevaarlijk=True` waardoor
de bevestigingslaag een **extra bevestiging** vraagt (US13).

```mermaid
flowchart TD
    A([Gewone taal: 'maak back-up' of 'zet terug']) --> B[backup.verwerk_backup]
    B --> C{Soort?}
    C -- back-up --> D[Commando: rsync bron - reservekopie]
    C -- herstel --> E[Commando: rsync reservekopie - bron<br/>gevaarlijk = True]
    D --> F[Veiligheidslaag US3]
    E --> F
    F --> G[Bevestiging US2]
    G --> H{Gevaarlijk?}
    H -- nee --> I[Knop 'Uitvoeren']
    H -- ja --> J[Knop 'Toch uitvoeren'<br/>extra waarschuwing US13]
    I --> K([Gebruiker bevestigt])
    J --> K
    K --> L{Keuze}
    L -- Annuleren --> M[logbook: 'geannuleerd']
    L -- Uitvoeren --> N[rsync via subprocess]
    N --> O{Gelukt?}
    O -- ja --> P[logbook: 'geslaagd']
    O -- nee --> Q[Begrijpelijke fout + logbook: 'mislukt']
```

## Toelichting

- **Back-up (US12):** kopieert de documentenmap naar een reservekopie-locatie met `rsync`
  (`modules/backup.py`). Niet-destructief → normale bevestiging.
- **Herstel (US13):** kopieert de reservekopie terug over de originelen. Dit **overschrijft** bestanden
  en is daarom als gevaarlijk gemarkeerd (`engine._vertaal` zet `gevaarlijk=True` voor `soort == "herstel"`),
  zodat de gebruiker bewust "Toch uitvoeren" moet kiezen.
- **Integratie:** beide lopen via dezelfde veiligheids-, bevestigings- en logboeklaag als de rest —
  aangetoond in `tests/test_integration.py`.
