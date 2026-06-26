"""US9 - 'Ongedaan maken'-suggestie.

Na een geslaagde opdracht stelt Luminosity voor hoe je die kunt terugdraaien.
De suggestie is bewust een *suggestie*: ze wordt niet automatisch uitgevoerd,
maar als nieuwe opdracht aangeboden zodat ze opnieuw door de hele pipeline
(vertaling -> veiligheid -> bevestiging) loopt voordat er iets gebeurt.

Voorbeelden:
    sudo pacman -S firefox   ->  ongedaan: sudo pacman -R firefox
    sudo pacman -R spotify   ->  ongedaan: sudo pacman -S spotify

Voor opdrachten zonder veilige tegenhanger (een systeem-update, schijfruimte
opvragen, een back-up terugzetten) is er geen automatische 'ongedaan maken'.
"""

import re
from dataclasses import dataclass


@dataclass
class Ongedaansuggestie:
    """Een voorstel om de zojuist uitgevoerde opdracht terug te draaien."""
    mogelijk: bool      # is er een zinnige tegenhanger?
    commando: str       # het 'ongedaan maken'-commando (leeg als niet mogelijk)
    uitleg: str         # begrijpelijke uitleg van wat terugdraaien doet


def suggereer(commando: str) -> Ongedaansuggestie:
    """Bepaalt op basis van het uitgevoerde commando hoe je het terugdraait."""
    c = (commando or "").strip()

    # Een installatie draai je terug door te verwijderen.
    m = re.search(r"pacman\s+-S\s+(\S.*)$", c)
    if m:
        pakketten = m.group(1).strip()
        return Ongedaansuggestie(
            True, f"sudo pacman -R {pakketten}",
            f"Verwijdert '{pakketten}' weer, zodat je terug bent bij de situatie van daarvoor.")

    # Een verwijdering draai je terug door opnieuw te installeren.
    m = re.search(r"pacman\s+-R\s+(\S.*)$", c)
    if m:
        pakketten = m.group(1).strip()
        return Ongedaansuggestie(
            True, f"sudo pacman -S {pakketten}",
            f"Installeert '{pakketten}' opnieuw.")

    return Ongedaansuggestie(
        False, "",
        "Voor deze opdracht is er geen automatische 'ongedaan maken'.")
