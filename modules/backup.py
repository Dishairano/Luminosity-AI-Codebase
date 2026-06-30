"""US12/US13 - Back-up maken en terugzetten via gewone taal (Vinicius).

Gebruikt rsync om een map te kopiëren naar/van een back-uplocatie. Voert niets
zelf uit; de engine regelt bevestiging en uitvoering. Terugzetten geldt als een
gevaarlijke actie en krijgt daardoor automatisch een extra bevestiging via de
veiligheidslaag.
"""

import os
from dataclasses import dataclass

# Back-uplocatie is instelbaar via de omgevingsvariabele LUMINOSITY_BACKUP_DIR
# (VERB-G1, op basis van feedback: niet meer hardcoded). Standaard: ~/Luminosity-Backups.
BACKUP_MAP = os.path.expanduser(os.environ.get("LUMINOSITY_BACKUP_DIR", "~/Luminosity-Backups"))
THUIS = os.path.expanduser("~")

# Welke mappen je kunt back-uppen (trefwoord -> mapnaam onder je thuismap).
# Voorheen kon alleen "Documenten"; testgebruikers wilden ook foto's e.d. (VERB-G1).
_MAPPEN = {
    "document": "Documenten",
    "foto": "Afbeeldingen",
    "afbeelding": "Afbeeldingen",
    "plaatje": "Afbeeldingen",
    "download": "Downloads",
    "muziek": "Muziek",
    "video": "Video's",
}


@dataclass
class Backupactie:
    herkend: bool
    commando: str
    uitleg: str
    soort: str  # "backup" of "herstel"


_BACKUP_WOORDEN = ["maak een back-up", "maak back-up", "backup", "back-up maken", "bewaar mijn"]
_HERSTEL_WOORDEN = ["zet terug", "herstel", "restore", "terugzetten", "terug"]


def _bevat(tekst, woorden):
    return any(w in tekst for w in woorden)


def _kies_map(tekst: str) -> str:
    """Bepaalt welke map de gebruiker bedoelt; standaard 'Documenten'."""
    for sleutel, mapnaam in _MAPPEN.items():
        if sleutel in tekst:
            return mapnaam
    return "Documenten"


def verwerk_backup(invoer: str) -> Backupactie:
    """Zet een back-up-opdracht in gewone taal om naar een rsync-commando."""
    tekst = invoer.strip().lower()
    mapnaam = _kies_map(tekst)
    bron = os.path.join(THUIS, mapnaam)
    reservekopie = os.path.join(BACKUP_MAP, mapnaam)

    if _bevat(tekst, _HERSTEL_WOORDEN):
        return Backupactie(
            True, f'rsync -a "{reservekopie}/" "{bron}/"',
            f"Ik zet je map '{mapnaam}' terug vanuit de laatste back-up. "
            "Let op: dit overschrijft je huidige bestanden.", "herstel")

    if _bevat(tekst, _BACKUP_WOORDEN):
        return Backupactie(
            True, f'rsync -a "{bron}/" "{reservekopie}/"',
            f"Ik maak een back-up van je map '{mapnaam}' naar {BACKUP_MAP}.", "backup")

    return Backupactie(False, "",
                       "Ik snap deze back-up-opdracht nog niet. Probeer "
                       "'maak een back-up van mijn documenten', 'back-up mijn foto's' "
                       "of 'zet mijn back-up terug'.",
                       "onbekend")
