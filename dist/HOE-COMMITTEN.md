# Hoe commit ik mijn deel? (per persoon)

Dit is de nette, eerlijke manier om je eigen werk op GitHub te zetten, zodat bij het examen
**individueel herleidbaar** is wat jij deed. Iedereen doet dit op zijn **eigen account**.

## Eenmalig instellen (jouw identiteit)

Zet je eigen naam en GitHub-mail, zodat de commit aan **jouw** account wordt gekoppeld:

```bash
git config user.name  "Jouw naam"
git config user.email "jouw-github-mail@voorbeeld.nl"
```

> Je GitHub-mail vind je op github.com → Settings → Emails. Wil je je echte mail verbergen,
> gebruik dan het noreply-adres (bijv. `12345678+gebruikersnaam@users.noreply.github.com`).

## Je deel toevoegen

1. Pak je eigen zip uit in de projectmap (`Luminosity-AI-Codebase`).
2. Maak/gebruik je **eigen branch**:

   ```bash
   git checkout -b feature/shell      # Kenji
   # of: git checkout -b feature/netwerk   (Vinicius)
   ```

3. Commit **per taak** (niet alles in één keer), met het Trello-nummer in het bericht:

   ```bash
   git add luminosity-shell/
   git commit -m "US5: Luminosity-schil invoerbalk + bevestigingskaart"

   git add ...
   git commit -m "US8: logboekpaneel toevoegen"
   ```

4. Push je branch:

   ```bash
   git push -u origin feature/shell
   ```

5. Open op GitHub een **pull request** en laat een teamgenoot hem reviewen vóór de merge.

## Goede commit-gewoonten (telt mee voor je cijfer)

- **Kleine commits**: één logische stap per commit.
- **Duidelijke berichten**: begin met het Trello-nummer, bijv. `US11: wifi verbinden via nmcli`.
- **Eigen naam**: controleer met `git log` dat je naam erop staat.
- **Niet committen wat niet van jou is**: blijf in je eigen map/branch.

## Wie commit wat?

| Persoon | Map | Branch | User stories |
|---|---|---|---|
| Dishairano | `luminosity_engine/`, `iso/` | `feature/engine`, `feature/iso` | US1–US4, US6, US7, US9 |
| Kenji | `luminosity-shell/` | `feature/shell` | US5, US8 |
| Vinicius | `modules/` | `feature/netwerk`, `feature/backup` | US11, US12, US13 |
