# Luminosity Installer

Een grafische installer in de stijl van moderne setup-wizards, maar in
Luminosity-smaak (donker/licht, accentkleur, mascotte "Lumo"). De **UI is
HTML/CSS/JS** en draait in een kiosk-browser; een kleine **Python-server**
(`server.py`) stuurt de echte installatie aan via `install.sh`.

## Onderdelen

| Bestand | Wat het doet |
|---|---|
| `web/` | De installer-UI (index.html + assets). Werkt ook als website-mockup. |
| `server.py` | Lokale install-server: serveert de UI en biedt `/api/disks`, `/api/install` (SSE-voortgang), `/api/reboot`. |
| `install.sh` | De echte Arch-installatie: partitioneren → pacstrap → chroot-config → bootloader → Luminosity plaatsen. |
| `launch-installer.sh` | Start de server en opent de kiosk-browser (Hyprland/Wayland). |

## Hoe het in de live-ISO werkt

1. De live-ISO logt automatisch in en start Hyprland.
2. Hyprland start `launch-installer.sh` → server + Chromium-kiosk op
   `http://127.0.0.1:8723/`.
3. De gebruiker doorloopt de stappen; bij **Installeren** POST de UI de config
   naar `/api/install`, die `install.sh` draait en de voortgang terugstreamt.
4. Na afloop herstart de gebruiker; het **geïnstalleerde** systeem boot direct
   in de Luminosity-schil.

De UI detecteert zelf of er een server is: zonder server (bijv. op de website)
draait hij in **demo-modus** met een gesimuleerde installatie.

## Eerlijke beperking

`install.sh` is **niet** in deze ontwikkelomgeving uitgevoerd — er is geen echte
doel-schijf of boot. Het volgt de standaard Arch-installatiestappen en is bedoeld
om in de live-ISO (of een VM met een lege schijf) te draaien. Test bij voorkeur
eerst in QEMU met een lege virtuele schijf.
