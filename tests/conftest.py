"""Gedeelde pytest-fixtures.

Belangrijk: het logboek schrijft standaard naar ~/.luminosity/logboek.json. Voor
tests leiden we dat om naar een tijdelijk bestand, zodat tests niets op het
echte systeem achterlaten en onafhankelijk van elkaar zijn.
"""

import pytest

from luminosity_engine import logbook


@pytest.fixture
def tmp_logboek(tmp_path, monkeypatch):
    """Laat de engine naar een tijdelijk logboek schrijven en geeft het pad terug."""
    pad = str(tmp_path / "logboek.json")
    monkeypatch.setattr(logbook, "STANDAARD_PAD", pad)
    # De pad-default is bij functiedefinitie gebonden; ook die omleiden.
    monkeypatch.setattr(logbook.schrijf, "__defaults__", (pad,))
    monkeypatch.setattr(logbook.lees, "__defaults__", (pad,))
    return pad
