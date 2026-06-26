"""US7 - Statuswidgets: echte systeemgegevens voor de bovenbalk van de schil.

Levert begrijpelijke status (schijfruimte, tijd) die de Quickshell-schil toont.
Werkt volledig offline en zonder extra afhankelijkheden: schijfruimte komt uit
de standaardbibliotheek (shutil), de tijd uit datetime. Zo zijn de widgets
echte gegevens in plaats van vaste plaatjes.
"""

import shutil
from datetime import datetime


def schijf(pad: str = "/") -> dict:
    """Geeft schijfgebruik van het opgegeven pad: percentage en vrije ruimte."""
    totaal, gebruikt, vrij = shutil.disk_usage(pad)
    return {
        "percent_gebruikt": round(gebruikt / totaal * 100),
        "vrij_gb": round(vrij / (1024 ** 3), 1),
        "totaal_gb": round(totaal / (1024 ** 3), 1),
    }


def verzamel() -> dict:
    """Bundelt de widget-gegevens die de schil in de bovenbalk laat zien."""
    s = schijf()
    return {
        "tijd": datetime.now().strftime("%H:%M"),
        "schijf_percent": s["percent_gebruikt"],
        "schijf_vrij_gb": s["vrij_gb"],
        "schijf_tekst": f"{s['percent_gebruikt']}% gebruikt · {s['vrij_gb']} GB vrij",
    }
