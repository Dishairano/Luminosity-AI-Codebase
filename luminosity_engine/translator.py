"""US1 - Vertaler: zet gewone taal om naar een Linux-commando.

De vertaler is bewust "dom": hij denkt niet zelf na, maar gebruikt een
commando-bibliotheek met patronen. Elk patroon herkent een soort opdracht
(installeren, verwijderen, updaten, status) en bouwt het juiste commando.

Werkt volledig OFFLINE, zonder cloud-AI en zonder API-sleutel.
"""

import re
from dataclasses import dataclass


@dataclass
class Vertaling:
    """Het resultaat van een vertaling van taal naar commando."""
    herkend: bool          # heeft de engine de bedoeling begrepen?
    commando: str          # het Linux-commando (leeg als niet herkend)
    uitleg: str            # begrijpelijke uitleg voor de gebruiker
    soort: str             # type opdracht, bv. "installeren"


# De commando-bibliotheek: elke regel is (trefwoorden, soort, commando-sjabloon, uitleg-sjabloon).
# {pakket} wordt vervangen door de naam die de gebruiker noemde.
# Trefwoorden zijn synoniemen; als de zin er één bevat, herkent de engine de bedoeling.
_INSTALLEER_WOORDEN = ["installeer", "install", "download", "zet erop", "voeg toe"]
_VERWIJDER_WOORDEN = ["verwijder", "deinstalleer", "haal weg", "wis programma", "remove"]
_UPDATE_WOORDEN = ["update", "werk bij", "bijwerken", "upgrade"]
_SCHIJF_WOORDEN = ["schijfruimte", "hoeveel ruimte", "schijf vol", "opslag"]
_STATUS_WOORDEN = ["systeemstatus", "hoe gaat het systeem", "systeeminfo"]

# Stopwoorden die we uit de pakketnaam filteren (zodat "installeer firefox alsjeblieft"
# nog steeds "firefox" oplevert).
_STOPWOORDEN = set(
    _INSTALLEER_WOORDEN + _VERWIJDER_WOORDEN
    + ["het", "de", "een", "mijn", "alsjeblieft", "graag", "programma", "app",
       "voor", "me", "even", "pakket"]
)


def _bevat(tekst: str, woorden: list[str]) -> bool:
    """Geeft True als de tekst een van de trefwoorden bevat."""
    return any(woord in tekst for woord in woorden)


def _haal_pakketnaam(tekst: str) -> str:
    """Haalt de programmanaam uit de zin door trefwoorden/stopwoorden weg te halen."""
    woorden = re.findall(r"[a-z0-9.+-]+", tekst.lower())
    overig = [w for w in woorden if w not in _STOPWOORDEN]
    return overig[-1] if overig else ""


def vertaal(invoer: str) -> Vertaling:
    """Zet een zin in gewone taal om naar een Vertaling.

    Voorbeelden:
        "installeer firefox"   -> sudo pacman -S firefox
        "update mijn systeem"  -> sudo pacman -Syu
        "verwijder spotify"    -> sudo pacman -R spotify
        "hoeveel ruimte heb ik"-> df -h
    """
    tekst = invoer.strip().lower()

    if not tekst:
        return Vertaling(False, "", "Ik heb geen opdracht ontvangen.", "leeg")

    # Update heeft voorrang: "update" mag niet als pakketnaam worden gelezen.
    if _bevat(tekst, _UPDATE_WOORDEN):
        return Vertaling(
            True, "sudo pacman -Syu",
            "Ik werk je hele systeem bij naar de nieuwste versies.", "updaten")

    if _bevat(tekst, _SCHIJF_WOORDEN):
        return Vertaling(
            True, "df -h",
            "Ik laat zien hoeveel schijfruimte je nog hebt.", "schijfruimte")

    if _bevat(tekst, _STATUS_WOORDEN):
        return Vertaling(
            True, "uname -a && uptime",
            "Ik toon de status en hoe lang je systeem al aanstaat.", "status")

    if _bevat(tekst, _INSTALLEER_WOORDEN):
        naam = _haal_pakketnaam(tekst)
        if not naam:
            return Vertaling(False, "",
                             "Welk programma wil je installeren?", "installeren")
        return Vertaling(
            True, f"sudo pacman -S {naam}",
            f"Ik installeer '{naam}' met de pakketbeheerder pacman.", "installeren")

    if _bevat(tekst, _VERWIJDER_WOORDEN):
        naam = _haal_pakketnaam(tekst)
        if not naam:
            return Vertaling(False, "",
                             "Welk programma wil je verwijderen?", "verwijderen")
        return Vertaling(
            True, f"sudo pacman -R {naam}",
            f"Ik verwijder '{naam}' van je systeem.", "verwijderen")

    # Niets herkend: geef een begrijpelijke melding in plaats van een foutmelding.
    return Vertaling(
        False, "",
        "Ik snap deze opdracht nog niet. Probeer bijvoorbeeld "
        "'installeer firefox' of 'update mijn systeem'.", "onbekend")
