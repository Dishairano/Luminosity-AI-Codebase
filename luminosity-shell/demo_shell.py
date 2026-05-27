#!/usr/bin/env python3
"""Demo-harnas voor de Luminosity-schil (US5).

Quickshell heeft een grafische Wayland-omgeving nodig en kan niet headless
worden gerenderd. Dit script doet daarom precies wat shell.qml doet — het roept
de engine aan via dezelfde JSON-CLI — zodat de UI-flow reproduceerbaar te testen
is zonder beeldscherm.

Het demonstreert de drie verplichte testopdrachten uit de Definition of Done:
  1. een simpele opdracht (wordt uitgevoerd)
  2. een foutieve opdracht (foutafhandeling)
  3. een geannuleerde opdracht

Gebruik:  python3 luminosity-shell/demo_shell.py
"""

import json
import subprocess
import sys

CLI = [sys.executable, "-m", "luminosity_engine.cli", "--json"]


def roep(invoer: str, *vlaggen: str) -> dict:
    """Roept de engine aan zoals de schil dat doet en geeft het JSON-antwoord."""
    uit = subprocess.run(CLI + list(vlaggen) + [invoer],
                         capture_output=True, text=True).stdout
    return json.loads(uit)


def toon(kop: str, data: dict) -> None:
    b = data["bevestiging"]
    print(f"\n=== {kop} ===")
    print(f"  invoer    : {data['invoer']}")
    print(f"  titel     : {b['titel']}")
    print(f"  commando  : {b['commando'] or '(geen)'}")
    print(f"  uitleg    : {b['uitleg']}")
    if b["veiligheidstekst"]:
        print(f"  veiligheid: {b['veiligheidstekst']}")
    if "resultaat" in data:
        r = data["resultaat"]
        eerste = r["uitvoer"].splitlines()[0] if r["uitvoer"] else ""
        print(f"  resultaat : {'gelukt' if r['gelukt'] else 'mislukt'} — {eerste}")


def main() -> None:
    # 1. Simpele, veilige opdracht -> wordt uitgevoerd.
    toon("1. Simpele opdracht (uitvoeren)", roep("hoeveel ruimte heb ik nog", "--run"))

    # 2. Foutieve opdracht -> engine voert uit maar pacman geeft een nette fout.
    toon("2. Foutieve opdracht (foutafhandeling)",
         roep("installeer dit-pakket-bestaat-niet-12345", "--run"))

    # 3. Geannuleerde opdracht -> niets uitgevoerd, wel gelogd.
    toon("3. Geannuleerde opdracht", roep("verwijder firefox", "--cancel"))

    # Logboek tonen (US8): alle drie de opdrachten moeten zichtbaar zijn.
    print("\n=== Logboek ===")
    logboek = subprocess.run(
        [sys.executable, "-m", "luminosity_engine.cli", "--logboek"],
        capture_output=True, text=True).stdout
    for regel in json.loads(logboek):
        print(f"  #{regel['id']}  [{regel['status']:<11}] {regel['invoertekst']}")


if __name__ == "__main__":
    main()
