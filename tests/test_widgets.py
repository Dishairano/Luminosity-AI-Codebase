"""US7 - tests voor de statuswidgets (echte schijf-/tijdgegevens)."""

import re

from luminosity_engine import widgets


def test_schijf_geeft_geldig_percentage():
    s = widgets.schijf("/")
    assert 0 <= s["percent_gebruikt"] <= 100
    assert s["vrij_gb"] >= 0
    assert s["totaal_gb"] > 0


def test_verzamel_levert_de_verwachte_velden():
    w = widgets.verzamel()
    assert set(["tijd", "schijf_percent", "schijf_vrij_gb", "schijf_tekst"]).issubset(w)


def test_tijd_heeft_het_formaat_uu_mm():
    w = widgets.verzamel()
    assert re.fullmatch(r"\d{2}:\d{2}", w["tijd"])


def test_schijf_tekst_is_leesbaar():
    w = widgets.verzamel()
    assert "gebruikt" in w["schijf_tekst"]
