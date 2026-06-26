"""De engine knoopt alle onderdelen aan elkaar in de juiste, veilige volgorde:

    taal  ->  vertaler (US1) + modules (US11-13)  ->  veiligheidslaag (US3)  ->  bevestiging (US2)
                                                                  |
                                            gebruiker bevestigt --+--> uitvoeren -> logboek (US8)

De vertaler dekt pakketbeheer (installeren, updaten, schijf, status). Domein-
modules (netwerk, back-up) leveren hún eigen commando's. De engine routeert de
invoer: eerst de vertaler, daarna de modules. Zo loopt ELKE opdracht — ook
netwerk en back-up — door dezelfde veiligheids-, bevestigings- en logboeklaag.

Belangrijk: `verwerk()` voert NIETS uit. Het bereidt alleen de bevestiging voor.
Pas als de gebruiker akkoord gaat, roept de schil `voer_uit()` aan.
"""

import subprocess
from dataclasses import dataclass

from . import confirm, logbook, ongedaan, safety, translator
from .confirm import Bevestiging
from .ongedaan import Ongedaansuggestie
from .translator import Vertaling

try:  # de modules zijn een los pakket naast de engine (modules/ in de repo, /opt/luminosity)
    from modules import backup, netwerk
except ImportError:  # pragma: no cover - modules niet aanwezig in deze omgeving
    backup = netwerk = None


def _vertaal(invoer: str) -> Vertaling:
    """Routeert de invoer langs de vertaler en daarna de domeinmodules.

    De eerste die de bedoeling herkent, wint. Zo komt netwerk- en back-up-werk
    in dezelfde Vertaling-vorm terecht en loopt het door de hele pipeline.
    """
    vertaling = translator.vertaal(invoer)
    if vertaling.herkend:
        return vertaling

    if netwerk is not None:
        actie = netwerk.verwerk_netwerk(invoer)
        if actie.herkend:
            return Vertaling(True, actie.commando, actie.uitleg, "netwerk")

    if backup is not None:
        actie = backup.verwerk_backup(invoer)
        if actie.herkend:
            # Terugzetten overschrijft bestaande bestanden -> markeer als gevaarlijk
            # zodat de bevestigingslaag een extra bevestiging vraagt (US13).
            return Vertaling(True, actie.commando, actie.uitleg, actie.soort,
                             gevaarlijk=(actie.soort == "herstel"))

    # Niets herkende de opdracht: geef de nette "niet begrepen"-vertaling terug.
    return vertaling


@dataclass
class Uitvoerresultaat:
    """Het resultaat nadat een commando echt is uitgevoerd."""
    gelukt: bool
    uitvoer: str   # wat het commando teruggaf (of een begrijpelijke foutuitleg)
    ongedaan: Ongedaansuggestie | None = None  # US9: hoe je dit kunt terugdraaien


def verwerk(invoer: str) -> Bevestiging:
    """Stap 1: zet gewone taal om naar een bevestigingsbericht (voert niets uit)."""
    vertaling = _vertaal(invoer)
    oordeel = safety.controleer(vertaling.commando) if vertaling.herkend \
        else safety.Veiligheidsoordeel(True, False, "")
    return confirm.bouw(vertaling, oordeel)


def voer_uit(invoer: str, bevestiging: Bevestiging) -> Uitvoerresultaat:
    """Stap 2: voert het commando uit ná bevestiging en schrijft naar het logboek.

    Geblokkeerde of niet-herkende opdrachten worden nooit uitgevoerd.
    """
    if not bevestiging.mag_uitvoeren or not bevestiging.commando:
        logbook.schrijf(invoer, bevestiging.commando, "geblokkeerd")
        return Uitvoerresultaat(False, "Dit commando is niet uitgevoerd.")

    try:
        proces = subprocess.run(
            bevestiging.commando, shell=True, capture_output=True, text=True, timeout=300)
        gelukt = proces.returncode == 0
        if gelukt:
            logbook.schrijf(invoer, bevestiging.commando, "geslaagd")
            # US9: stel voor hoe je deze geslaagde opdracht kunt terugdraaien.
            return Uitvoerresultaat(True, proces.stdout.strip() or "Klaar.",
                                    ongedaan.suggereer(bevestiging.commando))
        # Maak van de ruwe fout een begrijpelijke uitleg (verbeterpunt US/VERB-D1).
        logbook.schrijf(invoer, bevestiging.commando, "mislukt")
        return Uitvoerresultaat(False, _begrijpelijke_fout(proces.stderr.strip()))
    except subprocess.TimeoutExpired:
        logbook.schrijf(invoer, bevestiging.commando, "mislukt")
        return Uitvoerresultaat(False, "De opdracht duurde te lang en is gestopt.")


def annuleer(invoer: str, bevestiging: Bevestiging) -> None:
    """Registreert dat de gebruiker een opdracht heeft geannuleerd (US8).

    Hierdoor verschijnt ook een geannuleerde opdracht in het logboek, zodat de
    gebruiker kan terugzien dat er bewust niets is uitgevoerd.
    """
    logbook.schrijf(invoer, bevestiging.commando, "geannuleerd")


def _begrijpelijke_fout(ruwe_fout: str) -> str:
    """Vertaalt een ruwe foutmelding naar begrijpelijke taal met een vervolgstap."""
    fout = ruwe_fout.lower()
    if "target not found" in fout or "could not find" in fout:
        return "Dit programma bestaat niet onder die naam. Controleer de spelling."
    if "permission denied" in fout:
        return "Je hebt hier beheerdersrechten voor nodig (sudo)."
    if "unable to lock database" in fout:
        return "De pakketbeheerder is al bezig. Wacht even en probeer opnieuw."
    return ruwe_fout or "Er ging iets mis, maar de fout is onbekend."
