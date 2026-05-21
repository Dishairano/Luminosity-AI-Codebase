"""Eenvoudige terminal-interface om de engine te testen zonder de schil.

Gebruik:
    python -m luminosity_engine.cli "installeer firefox"
    python -m luminosity_engine.cli            (interactief)

De schil (Quickshell) roept de engine straks op dezelfde manier aan.
"""

import sys

from . import engine


def _toon(invoer: str) -> None:
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
        print("  Geannuleerd.\n")


def main() -> None:
    if len(sys.argv) > 1:
        _toon(" ".join(sys.argv[1:]))
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
