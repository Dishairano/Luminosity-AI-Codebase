"""TEST-D2 - Tests voor de veiligheidslaag (gevaarlijke commando's)."""

from luminosity_engine import safety


def test_rm_rf_root_geblokkeerd():
    oordeel = safety.controleer("sudo rm -rf /")
    assert oordeel.geblokkeerd
    assert not oordeel.veilig


def test_fork_bomb_geblokkeerd():
    oordeel = safety.controleer(":(){ :|:& };:")
    assert oordeel.geblokkeerd


def test_mkfs_geblokkeerd():
    oordeel = safety.controleer("mkfs.ext4 /dev/sda1")
    assert oordeel.geblokkeerd


def test_normaal_commando_veilig():
    oordeel = safety.controleer("sudo pacman -S firefox")
    assert oordeel.veilig
    assert not oordeel.geblokkeerd


def test_verwijderen_geeft_waarschuwing():
    oordeel = safety.controleer("sudo pacman -R firefox")
    assert not oordeel.veilig        # niet zomaar veilig
    assert not oordeel.geblokkeerd    # maar ook niet geblokkeerd: extra bevestiging


def test_shutdown_waarschuwing():
    oordeel = safety.controleer("shutdown now")
    assert not oordeel.veilig
    assert not oordeel.geblokkeerd
