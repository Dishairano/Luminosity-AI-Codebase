"""US12/US13 - Back-up maken en terugzetten via gewone taal (Vinicius).

Gebruikt rsync om een map te kopiëren naar/van een back-uplocatie. Voert niets
zelf uit; de engine regelt bevestiging en uitvoering. Terugzetten geldt als een
gevaarlijke actie en krijgt daardoor automatisch een extra bevestiging via de
veiligheidslaag.
"""

import os
from dataclasses import dataclass

# Standaard back-uplocatie (kan later instelbaar worden gemaakt in de schil).
BACKUP_MAP = os.path.expanduser("~/Luminosity-Backups")
DOCUMENTEN = os.path.expanduser("~/Documenten")


@dataclass
class Backupactie:
    herkend: bool
    commando: str
    uitleg: str
    soort: str  # "backup" of "herstel"


_BACKUP_WOORDEN = ["maak een back-up", "maak back-up", "backup", "back-up maken", "bewaar mijn"]
_HERSTEL_WOORDEN = ["zet terug", "herstel", "restore", "terugzetten"]


def _bevat(tekst, woorden):
    return any(w in tekst for w in woorden)


def verwerk_backup(invoer: str) -> Backupactie:
    """Zet een back-up-opdracht in gewone taal om naar een rsync-commando."""
    tekst = invoer.strip().lower()

    if _bevat(tekst, _HERSTEL_WOORDEN):
        return Backupactie(
            True, f'rsync -a "{BACKUP_MAP}/Documenten/" "{DOCUMENTEN}/"',
            "Ik zet je documenten terug vanuit de laatste back-up. "
            "Let op: dit overschrijft je huidige bestanden.", "herstel")

    if _bevat(tekst, _BACKUP_WOORDEN):
        return Backupactie(
            True, f'rsync -a "{DOCUMENTEN}/" "{BACKUP_MAP}/Documenten/"',
            f"Ik maak een back-up van je documenten naar {BACKUP_MAP}.", "backup")

    return Backupactie(False, "",
                       "Ik snap deze back-up-opdracht nog niet. Probeer "
                       "'maak een back-up van mijn documenten' of 'zet mijn back-up terug'.",
                       "onbekend")
