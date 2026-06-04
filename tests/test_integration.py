"""Integratietests: lopen netwerk- en back-up-opdrachten door de hele engine-pipeline?

Dit is de kern van fase 3: de engine moet domeinmodules routeren, zodat ook
netwerk- en back-up-acties door vertaling -> veiligheid -> bevestiging gaan.
"""

from luminosity_engine import engine


def test_engine_routeert_netwerk():
    b = engine.verwerk("welke wifi-netwerken zijn er")
    assert b.commando == "nmcli device wifi list"
    assert b.mag_uitvoeren


def test_engine_routeert_backup():
    b = engine.verwerk("maak een back-up van mijn documenten")
    assert b.commando.startswith("rsync -a")
    assert b.titel == "Klaar om een back-up te maken"


def test_engine_herstel_vraagt_extra_bevestiging():
    b = engine.verwerk("zet mijn back-up terug")
    assert b.mag_uitvoeren
    assert b.extra_waarschuwing  # terugzetten is gevaarlijk -> extra bevestiging


def test_engine_onbekende_opdracht_niet_uitvoerbaar():
    b = engine.verwerk("dans de polka")
    assert not b.mag_uitvoeren
    assert b.titel == "Niet begrepen"


def test_pakketbeheer_heeft_voorrang_op_modules():
    # "installeer" hoort bij de vertaler, niet bij een module.
    b = engine.verwerk("installeer firefox")
    assert b.commando == "sudo pacman -S firefox"
