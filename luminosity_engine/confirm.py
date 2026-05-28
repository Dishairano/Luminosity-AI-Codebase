"""US2 - Bevestiging: bouwt de uitleg + bevestigingsvraag voor de gebruiker.

Dit onderdeel voert NIETS uit. Het maakt alleen het 'wat ga ik doen'-bericht
dat de schil aan de gebruiker toont, met het commando, de uitleg en het
veiligheidsoordeel. Pas ná 'Uitvoeren' gebeurt er echt iets (zie engine.py).
"""

from dataclasses import dataclass

from .safety import Veiligheidsoordeel
from .translator import Vertaling


@dataclass
class Bevestiging:
    """Het 'wat ga ik doen'-bericht dat de gebruiker te zien krijgt."""
    titel: str            # korte samenvatting
    commando: str         # het commando dat uitgevoerd zou worden
    uitleg: str           # begrijpelijke uitleg
    veiligheidstekst: str # melding van de veiligheidslaag
    mag_uitvoeren: bool   # mag de 'Uitvoeren'-knop aan?
    extra_waarschuwing: bool  # vraagt dit een extra bevestiging?


def bouw(vertaling: Vertaling, oordeel: Veiligheidsoordeel) -> Bevestiging:
    """Combineert vertaling + veiligheidsoordeel tot een bevestigingsbericht."""
    if not vertaling.herkend:
        return Bevestiging(
            titel="Niet begrepen", commando="", uitleg=vertaling.uitleg,
            veiligheidstekst="", mag_uitvoeren=False, extra_waarschuwing=False)

    titels = {
        "installeren": "Klaar om te installeren",
        "verwijderen": "Klaar om te verwijderen",
        "updaten": "Klaar om bij te werken",
        "schijfruimte": "Schijfruimte opvragen",
        "status": "Systeemstatus opvragen",
        "netwerk": "Netwerk-opdracht klaar",
        "backup": "Klaar om een back-up te maken",
        "herstel": "Klaar om een back-up terug te zetten",
    }
    return Bevestiging(
        titel=titels.get(vertaling.soort, "Klaar om uit te voeren"),
        commando=vertaling.commando,
        uitleg=vertaling.uitleg,
        veiligheidstekst=oordeel.reden,
        mag_uitvoeren=not oordeel.geblokkeerd,
        # Extra bevestiging als de veiligheidslaag waarschuwt OF als de opdracht
        # zelf als gevaarlijk is gemarkeerd (bijv. een back-up terugzetten).
        extra_waarschuwing=(
            ((not oordeel.veilig) and (not oordeel.geblokkeerd)) or vertaling.gevaarlijk
        ),
    )
