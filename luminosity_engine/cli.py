"""Terminal- en machine-interface om de engine aan te roepen.

Mens-vriendelijk (standaard):
    python -m luminosity_engine.cli "installeer firefox"
    python -m luminosity_engine.cli            (interactief)

Machine-vriendelijk (door de Quickshell-schil gebruikt, US5):
    python -m luminosity_engine.cli --json "installeer firefox"
        -> JSON met de bevestiging (voert NIETS uit)
    python -m luminosity_engine.cli --run --json "installeer firefox"
        -> bevestiging + uitvoering (gebruiker heeft in de UI bevestigd)
    python -m luminosity_engine.cli --cancel --json "installeer firefox"
        -> registreert een annulering in het logboek
    python -m luminosity_engine.cli --logboek
        -> JSON-lijst van het logboek (voor het logboekpaneel)

De JSON-interface houdt de schil simpel: de QML-kant hoeft alleen velden te
lezen en knoppen te tonen; alle logica blijft in de Python-engine.
"""

import argparse
import json
import sys
from dataclasses import asdict

from . import engine, logbook


def _bevestiging_json(invoer: str, run: bool, cancel: bool) -> dict:
    """Bouwt het JSON-antwoord voor de schil op basis van de gekozen actie."""
    bevestiging = engine.verwerk(invoer)
    antwoord = {"invoer": invoer, "bevestiging": asdict(bevestiging)}

    if run and bevestiging.mag_uitvoeren:
        resultaat = engine.voer_uit(invoer, bevestiging)
        antwoord["resultaat"] = asdict(resultaat)
    elif cancel:
        engine.annuleer(invoer, bevestiging)
        antwoord["resultaat"] = {"gelukt": False, "uitvoer": "Geannuleerd."}
    return antwoord


def _toon(invoer: str) -> None:
    """Interactieve, mens-vriendelijke weergave (voor testen zonder schil)."""
    bevestiging = engine.verwerk(invoer)
    print(f"\n  {bevestiging.titel}")
    if bevestiging.commando:
        print(f"  Commando : {bevestiging.commando}")
    print(f"  Uitleg   : {bevestiging.uitleg}")
    if bevestiging.veiligheidstekst:
        print(f"  Veiligheid: {bevestiging.veiligheidstekst}")

    if not bevestiging.mag_uitvoeren:
        return
    vraag = "  Extra bevestiging nodig. Uitvoeren? (j/n) " \
        if bevestiging.extra_waarschuwing else "  Uitvoeren? (j/n) "
    if input(vraag).strip().lower() in ("j", "ja", "y"):
        resultaat = engine.voer_uit(invoer, bevestiging)
        print(f"  Resultaat: {resultaat.uitvoer}\n")
    else:
        engine.annuleer(invoer, bevestiging)
        print("  Geannuleerd.\n")


def main() -> None:
    parser = argparse.ArgumentParser(prog="luminosity_engine.cli", add_help=True)
    parser.add_argument("invoer", nargs="*", help="opdracht in gewone taal")
    parser.add_argument("--json", action="store_true", help="geef JSON terug (voor de schil)")
    parser.add_argument("--run", action="store_true", help="voer uit (na bevestiging in de UI)")
    parser.add_argument("--cancel", action="store_true", help="registreer een annulering")
    parser.add_argument("--logboek", action="store_true", help="toon het logboek als JSON")
    args = parser.parse_args()

    if args.logboek:
        print(json.dumps(logbook.lees(), ensure_ascii=False, indent=2))
        return

    invoer = " ".join(args.invoer).strip()

    if args.json:
        if not invoer:
            print(json.dumps({"fout": "geen invoer"}, ensure_ascii=False))
            sys.exit(1)
        print(json.dumps(_bevestiging_json(invoer, args.run, args.cancel),
                         ensure_ascii=False, indent=2))
        return

    if invoer:
        _toon(invoer)
        return

    print("Luminosity - typ een opdracht in gewone taal (of 'stop').")
    while True:
        try:
            invoer = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if invoer.lower() in ("stop", "exit", "quit"):
            break
        if invoer:
            _toon(invoer)


if __name__ == "__main__":
    main()
