"""US3 - Veiligheidslaag: detecteert en blokkeert gevaarlijke commando's.

Deze laag staat los van de vertaler, zodat hij ELK commando kan controleren
voordat het wordt uitgevoerd. Hij kijkt naar bekende gevaarlijke patronen
(bijv. alles wissen, de schijf overschrijven, een fork-bomb).
"""

import re
from dataclasses import dataclass


@dataclass
class Veiligheidsoordeel:
    """Het oordeel van de veiligheidslaag over een commando."""
    veilig: bool       # mag dit zonder extra waarschuwing?
    geblokkeerd: bool  # moet dit volledig geblokkeerd worden?
    reden: str         # uitleg voor de gebruiker


# Patronen die ALTIJD geblokkeerd worden: deze kunnen het systeem onherstelbaar slopen.
_GEBLOKKEERD = [
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+/(?:\s|$)", "alles vanaf de hoofdmap verwijderen"),
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+/\*", "alle bestanden in de hoofdmap verwijderen"),
    (r":\(\)\s*{\s*:\|:&\s*}\s*;", "een fork-bomb die de computer laat vastlopen"),
    (r"\bmkfs\b", "de harde schijf formatteren (alles wissen)"),
    (r"\bdd\b.*of=/dev/[sh]d", "de harde schijf rechtstreeks overschrijven"),
    (r">\s*/dev/[sh]d", "rechtstreeks naar de harde schijf schrijven"),
    (r"\bchmod\s+-r\s+777\s+/(?:\s|$)", "alle systeemrechten openzetten"),
]

# Patronen die niet meteen worden geblokkeerd, maar wél een EXTRA waarschuwing krijgen.
_WAARSCHUWING = [
    (r"\bsudo\s+rm\b", "je verwijdert bestanden met beheerdersrechten"),
    (r"\bpacman\s+-r", "je verwijdert software van je systeem"),
    (r"\bshutdown\b|\breboot\b|\bpoweroff\b", "je zet de computer uit of herstart hem"),
]


def controleer(commando: str) -> Veiligheidsoordeel:
    """Controleert een commando en geeft een Veiligheidsoordeel terug."""
    tekst = commando.strip().lower()

    for patroon, reden in _GEBLOKKEERD:
        if re.search(patroon, tekst):
            return Veiligheidsoordeel(
                veilig=False, geblokkeerd=True,
                reden=f"Geblokkeerd: dit zou {reden}. Dit voer ik niet uit.")

    for patroon, reden in _WAARSCHUWING:
        if re.search(patroon, tekst):
            return Veiligheidsoordeel(
                veilig=False, geblokkeerd=False,
                reden=f"Let op: {reden}. Weet je het zeker?")

    return Veiligheidsoordeel(veilig=True, geblokkeerd=False, reden="Dit commando is veilig.")
