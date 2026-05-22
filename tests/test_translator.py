"""TEST-D1 - Tests voor de vertaler (taal -> commando)."""

from luminosity_engine import translator


def test_installeer():
    v = translator.vertaal("installeer firefox")
    assert v.herkend
    assert v.commando == "sudo pacman -S firefox"
    assert v.soort == "installeren"


def test_installeer_met_extra_woorden():
    v = translator.vertaal("installeer alsjeblieft het programma spotify")
    assert v.commando == "sudo pacman -S spotify"


def test_update():
    v = translator.vertaal("update mijn systeem")
    assert v.commando == "sudo pacman -Syu"
    assert v.soort == "updaten"


def test_verwijder():
    v = translator.vertaal("verwijder spotify")
    assert v.commando == "sudo pacman -R spotify"


def test_schijfruimte():
    v = translator.vertaal("hoeveel ruimte heb ik nog")
    assert v.commando == "df -h"


def test_onbekend():
    v = translator.vertaal("zfgdsf onzin blabla")
    assert not v.herkend
    assert v.commando == ""


def test_leeg():
    v = translator.vertaal("   ")
    assert not v.herkend


def test_installeer_zonder_naam():
    v = translator.vertaal("installeer")
    assert not v.herkend
