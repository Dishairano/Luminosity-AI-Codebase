# Luminosity OS — ISO-bouw (OS1 + OS4)

Hier zit de `archiso`-configuratie waarmee Luminosity OS een **bootbare ISO** wordt: een echte
Arch-gebaseerde distributie die opstart in onze eigen Quickshell-schil.

## Wat zit erin?

| Bestand | Wat het doet |
|---|---|
| `packages.x86_64` | Welke pakketten in het OS zitten (Hyprland, Qt, Python, NetworkManager…) |
| `profiledef.sh` | Naam, label en versie van de ISO |
| `pacman.conf` | Pakketbronnen + lokale repo voor quickshell |
| `airootfs/` | De bestanden die ín het OS komen (configs, autostart, onze code) |
| `build.sh` | Bouwt de ISO |

### Hoe het opstart
1. Het OS logt automatisch in op tty1 (`getty@tty1` autologin).
2. `.bash_profile` start **Hyprland**.
3. Hyprland start via `exec-once` meteen de **Luminosity-schil** (`quickshell … shell.qml`), fullscreen.
4. De gebruiker ziet alleen Luminosity en typt in gewone taal.

## Bouwen op Arch Linux

```bash
sudo pacman -S archiso
sudo ./build.sh        # resultaat: iso/out/luminosity-*.iso
```

## Bouwen zonder Arch (via Docker)

Op elk systeem met Docker:

```bash
docker run --rm --privileged -v "$PWD/..":/repo archlinux:latest bash -c '
    pacman -Sy --noconfirm archiso git base-devel sudo &&
    cd /repo/iso && ./build.sh
'
```

De ISO komt in `iso/out/`. Zet hem op een USB met `dd` of een tool als Ventoy en boot ervan.

> **Let op (eerlijk):** `quickshell` komt uit de AUR en wordt door `build.sh` los gebouwd. Lukt dat in
> jouw omgeving niet meteen, bouw het pakket dan handmatig en leg het in `/tmp/luminosity-repo/`. De rest
> van de ISO bouwt gewoon door.
