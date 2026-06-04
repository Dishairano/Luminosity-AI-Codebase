"""Tests voor de engine: routering, veiligheid in de pipeline, uitvoeren en logging."""

from luminosity_engine import engine, logbook


def test_verwerk_veilige_opdracht_mag_uitvoeren():
    b = engine.verwerk("installeer firefox")
    assert b.mag_uitvoeren
    assert b.commando == "sudo pacman -S firefox"
    assert not b.extra_waarschuwing


def test_verwerk_gevaarlijke_opdracht_wordt_geblokkeerd():
    # rm -rf / komt niet uit de vertaler, maar de pipeline moet hem alsnog blokkeren
    # als hij langs de engine zou komen. We toetsen de bevestiging via de safety-laag:
    from luminosity_engine import confirm, safety, translator
    vertaling = translator.Vertaling(True, "sudo rm -rf /", "test", "test")
    oordeel = safety.controleer(vertaling.commando)
    b = confirm.bouw(vertaling, oordeel)
    assert not b.mag_uitvoeren


def test_voer_uit_geslaagd_logt_geslaagd(tmp_logboek):
    from luminosity_engine.confirm import Bevestiging
    bev = Bevestiging("t", "true", "uitleg", "", True, False)
    res = engine.voer_uit("doe iets", bev)
    assert res.gelukt
    regels = logbook.lees()
    assert regels[-1]["status"] == "geslaagd"


def test_voer_uit_mislukt_logt_mislukt(tmp_logboek):
    from luminosity_engine.confirm import Bevestiging
    bev = Bevestiging("t", "false", "uitleg", "", True, False)
    res = engine.voer_uit("doe iets fout", bev)
    assert not res.gelukt
    assert logbook.lees()[-1]["status"] == "mislukt"


def test_voer_uit_geblokkeerd_voert_niets_uit(tmp_logboek):
    from luminosity_engine.confirm import Bevestiging
    bev = Bevestiging("t", "", "niet begrepen", "", False, False)
    res = engine.voer_uit("onzin", bev)
    assert not res.gelukt
    assert logbook.lees()[-1]["status"] == "geblokkeerd"


def test_annuleer_logt_geannuleerd(tmp_logboek):
    bev = engine.verwerk("installeer firefox")
    engine.annuleer("installeer firefox", bev)
    assert logbook.lees()[-1]["status"] == "geannuleerd"


def test_begrijpelijke_fout_vertaalt_ruwe_melding():
    assert "spelling" in engine._begrijpelijke_fout("error: target not found: xyz").lower()
    assert "beheerdersrechten" in engine._begrijpelijke_fout("permission denied").lower()
