"""US8 - Logboek: bewaart elke uitgevoerde opdracht.

Slaat per opdracht op: invoertekst, commando, status en tijdstip. Gebruikt een
eenvoudig JSON-bestand zodat het overal werkt zonder database-installatie.
Komt overeen met de logboek-tabel uit het ERD (id, invoertekst, commando,
status, tijdstip).
"""

import json
import os
from datetime import datetime

STANDAARD_PAD = os.path.expanduser("~/.luminosity/logboek.json")


def _laad(pad: str) -> list[dict]:
    """Leest het logboek in; geeft een lege lijst als het bestand nog niet bestaat."""
    if not os.path.exists(pad):
        return []
    try:
        with open(pad, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def schrijf(invoertekst: str, commando: str, status: str, pad: str = STANDAARD_PAD) -> dict:
    """Voegt een opdracht toe aan het logboek en geeft de nieuwe regel terug.

    status is bijvoorbeeld: "geslaagd", "mislukt", "geannuleerd" of "geblokkeerd".
    """
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    regels = _laad(pad)
    regel = {
        "id": len(regels) + 1,
        "invoertekst": invoertekst,
        "commando": commando,
        "status": status,
        "tijdstip": datetime.now().isoformat(timespec="seconds"),
    }
    regels.append(regel)
    with open(pad, "w", encoding="utf-8") as f:
        json.dump(regels, f, indent=2, ensure_ascii=False)
    return regel


def lees(pad: str = STANDAARD_PAD) -> list[dict]:
    """Geeft alle logboek-regels terug (voor weergave in de schil)."""
    return _laad(pad)
