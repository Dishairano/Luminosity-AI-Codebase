"""US11 - Netwerk-/wifibeheer via gewone taal (Vinicius).

Volgt hetzelfde patroon als de taal-engine: herkent de bedoeling via patronen
en bouwt een nmcli-commando. Voert NIETS zelf uit; de engine regelt bevestiging
en uitvoering, zodat de veiligheidslaag er ook overheen werkt.
"""

import re
from dataclasses import dataclass


@dataclass
class Netwerkactie:
    herkend: bool
    commando: str
    uitleg: str


_VERBIND_WOORDEN = ["verbind", "connect", "maak verbinding", "ga op wifi"]
_LIJST_WOORDEN = ["welke wifi", "lijst wifi", "netwerken", "scan wifi"]
_STATUS_WOORDEN = ["wifi status", "ben ik verbonden", "netwerkstatus"]


def _bevat(tekst, woorden):
    return any(w in tekst for w in woorden)


def verwerk_netwerk(invoer: str) -> Netwerkactie:
    """Zet een netwerk-opdracht in gewone taal om naar een nmcli-commando."""
    tekst = invoer.strip().lower()

    if _bevat(tekst, _LIJST_WOORDEN):
        return Netwerkactie(True, "nmcli device wifi list",
                            "Ik laat de beschikbare wifi-netwerken zien.")

    if _bevat(tekst, _STATUS_WOORDEN):
        return Netwerkactie(True, "nmcli general status",
                            "Ik toon je huidige netwerkstatus.")

    if _bevat(tekst, _VERBIND_WOORDEN):
        # zoek de netwerknaam tussen aanhalingstekens, of het laatste woord
        match = re.search(r'"([^"]+)"|\'([^\']+)\'', invoer)
        naam = (match.group(1) or match.group(2)) if match else invoer.split()[-1]
        return Netwerkactie(
            True, f'nmcli device wifi connect "{naam}"',
            f"Ik verbind je met het wifi-netwerk '{naam}'. "
            "Mogelijk vraagt het systeem nog om het wachtwoord.")

    return Netwerkactie(False, "",
                        "Ik snap deze netwerk-opdracht nog niet. Probeer "
                        "'welke wifi-netwerken zijn er' of 'verbind met \"naam\"'.")
