"""US9 - tests voor de 'ongedaan maken'-suggestie."""

from luminosity_engine import ongedaan


def test_installatie_kan_worden_teruggedraaid_met_verwijderen():
    s = ongedaan.suggereer("sudo pacman -S firefox")
    assert s.mogelijk
    assert s.commando == "sudo pacman -R firefox"
    assert "firefox" in s.uitleg


def test_verwijdering_kan_worden_teruggedraaid_met_installeren():
    s = ongedaan.suggereer("sudo pacman -R spotify")
    assert s.mogelijk
    assert s.commando == "sudo pacman -S spotify"


def test_systeemupdate_heeft_geen_automatische_ongedaan():
    s = ongedaan.suggereer("sudo pacman -Syu")
    assert not s.mogelijk
    assert s.commando == ""


def test_schijfopvraag_heeft_geen_ongedaan():
    s = ongedaan.suggereer("df -h")
    assert not s.mogelijk


def test_leeg_commando_geeft_geen_ongedaan():
    s = ongedaan.suggereer("")
    assert not s.mogelijk
