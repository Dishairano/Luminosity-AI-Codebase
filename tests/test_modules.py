"""TEST-G1 - Tests voor de netwerk- en back-upmodules (Vinicius)."""

from modules import backup, netwerk


# --- Netwerk (US11) ---

def test_netwerk_lijst():
    a = netwerk.verwerk_netwerk("welke wifi-netwerken zijn er")
    assert a.herkend
    assert a.commando == "nmcli device wifi list"


def test_netwerk_status():
    a = netwerk.verwerk_netwerk("wifi status")
    assert a.herkend
    assert a.commando == "nmcli general status"


def test_netwerk_verbinden_met_naam():
    a = netwerk.verwerk_netwerk('verbind met "Thuisnet"')
    assert a.herkend
    assert 'connect "Thuisnet"' in a.commando


def test_netwerk_onbekend():
    a = netwerk.verwerk_netwerk("bak een taart")
    assert not a.herkend


# --- Back-up (US12/US13) ---

def test_backup_maken():
    a = backup.verwerk_backup("maak een back-up van mijn documenten")
    assert a.herkend
    assert a.soort == "backup"
    assert a.commando.startswith("rsync -a")


def test_backup_terugzetten():
    a = backup.verwerk_backup("zet mijn back-up terug")
    assert a.herkend
    assert a.soort == "herstel"


def test_backup_onbekend():
    a = backup.verwerk_backup("speel muziek af")
    assert not a.herkend


# --- VERB-G1: verbeteringen op basis van feedback ---

def test_netwerk_wifi_uit():
    a = netwerk.verwerk_netwerk("zet wifi uit")
    assert a.herkend
    assert a.commando == "nmcli radio wifi off"


def test_netwerk_wifi_aan():
    a = netwerk.verwerk_netwerk("zet wifi aan")
    assert a.herkend
    assert a.commando == "nmcli radio wifi on"


def test_netwerk_vergeet_netwerk():
    a = netwerk.verwerk_netwerk('vergeet "Thuis"')
    assert a.herkend
    assert a.commando == 'nmcli connection delete "Thuis"'


def test_backup_kiest_de_juiste_map():
    a = backup.verwerk_backup("maak een back-up van mijn foto's")
    assert a.herkend
    assert a.soort == "backup"
    assert "Afbeeldingen" in a.commando


def test_backup_herstel_kiest_de_juiste_map():
    a = backup.verwerk_backup("zet mijn downloads terug")
    assert a.herkend
    assert a.soort == "herstel"
    assert "Downloads" in a.commando
