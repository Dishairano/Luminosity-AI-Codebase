"""TEST-T1 - Tests voor de schil-interface: de JSON-CLI die shell.qml aanroept.

De schil voert zelf niets uit; hij praat met de engine via deze CLI. Door de CLI
te testen toetsen we precies wat de UI te zien krijgt. HOME wijst naar een
tijdelijke map zodat het logboek geisoleerd blijft.
"""

import json
import subprocess
import sys

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


def _cli(*args, home):
    uit = subprocess.run(
        [sys.executable, "-m", "luminosity_engine.cli", *args],
        capture_output=True, text=True, cwd=ROOT,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
    )
    return uit.stdout


def test_json_bevestiging(tmp_path):
    data = json.loads(_cli("--json", "installeer firefox", home=tmp_path))
    b = data["bevestiging"]
    assert b["commando"] == "sudo pacman -S firefox"
    assert b["mag_uitvoeren"] is True
    assert "resultaat" not in data  # --json alleen voorbereiden, niet uitvoeren


def test_json_run_voert_uit_en_logt(tmp_path):
    data = json.loads(_cli("--run", "--json", "hoeveel ruimte heb ik nog", home=tmp_path))
    assert data["resultaat"]["gelukt"] is True
    logboek = json.loads(_cli("--logboek", home=tmp_path))
    assert logboek[-1]["status"] == "geslaagd"


def test_json_cancel_logt_geannuleerd(tmp_path):
    json.loads(_cli("--cancel", "--json", "installeer firefox", home=tmp_path))
    logboek = json.loads(_cli("--logboek", home=tmp_path))
    assert logboek[-1]["status"] == "geannuleerd"


def test_logboek_leeg_bij_start(tmp_path):
    assert json.loads(_cli("--logboek", home=tmp_path)) == []
