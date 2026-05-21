"""De engine knoopt alle onderdelen aan elkaar in de juiste, veilige volgorde:

    taal  ->  vertaler (US1)  ->  veiligheidslaag (US3)  ->  bevestiging (US2)
                                                                  |
                                            gebruiker bevestigt --+--> uitvoeren -> logboek (US8)

Belangrijk: `verwerk()` voert NIETS uit. Het bereidt alleen de bevestiging voor.
Pas als de gebruiker akkoord gaat, roept de schil `voer_uit()` aan.
"""

import subprocess
from dataclasses import dataclass

from . import confirm, logbook, safety, translator
from .confirm import Bevestiging


@dataclass
class Uitvoerresultaat:
    """Het resultaat nadat een commando echt is uitgevoerd."""
    gelukt: bool
    uitvoer: str   # wat het commando teruggaf (of een begrijpelijke foutuitleg)


def verwerk(invoer: str) -> Bevestiging:
    """Stap 1: zet gewone taal om naar een bevestigingsbericht (voert niets uit)."""
    vertaling = translator.vertaal(invoer)
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
            return Uitvoerresultaat(True, proces.stdout.strip() or "Klaar.")
        # Maak van de ruwe fout een begrijpelijke uitleg (verbeterpunt US/VERB-D1).
        logbook.schrijf(invoer, bevestiging.commando, "mislukt")
        return Uitvoerresultaat(False, _begrijpelijke_fout(proces.stderr.strip()))
    except subprocess.TimeoutExpired:
        logbook.schrijf(invoer, bevestiging.commando, "mislukt")
        return Uitvoerresultaat(False, "De opdracht duurde te lang en is gestopt.")


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
