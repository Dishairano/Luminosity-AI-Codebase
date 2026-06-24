#!/usr/bin/env bash
# Opent de kiosk-browser (fullscreen, Wayland) op de installer.
# Wordt door Hyprland gestart in de live-ISO (zie airootfs hyprland.conf).
#
# De installer-server draait als systemd-service (luminosity-installer.service),
# losgekoppeld van de compositor — dit script start die alleen als fallback.
set -u
HIER="$(cd "$(dirname "$0")" && pwd)"
PORT="${LUM_INSTALLER_PORT:-8723}"
export PYTHONPATH=/opt/luminosity:${PYTHONPATH:-}

# Dit script wordt alleen door Hyprland (exec-once) gestart; dat het draait
# bewijst dat de compositor is opgekomen — ook zonder GPU (software-GL).
# Markering naar de seriële poort voor een VM-/CI-boottest.
echo "LUMINOSITY_GUI_UP" > /dev/ttyS0 2>/dev/null || true

port_up() { (exec 3<>"/dev/tcp/127.0.0.1/$PORT") 2>/dev/null && { exec 3>&-; return 0; }; return 1; }

# Eerst de root-systemd-service de tijd geven om te luisteren (vermijd een race
# waarbij we per ongeluk zelf een niet-root server starten). Pas als die na ~6s
# nog niet luistert, starten we er zelf één als fallback (server.py draait de
# installatie dan via sudo, dus ook dat werkt met de juiste rechten).
up=0
for _ in $(seq 1 30); do port_up && { up=1; break; }; sleep 0.2; done
if [ "$up" != "1" ]; then
    python3 "$HIER/server.py" &
    trap 'kill %1 2>/dev/null' EXIT
    for _ in $(seq 1 50); do port_up && break; sleep 0.2; done
fi

# Kiosk-browser openen op de installer
exec chromium \
    --kiosk --app="http://127.0.0.1:$PORT/" \
    --ozone-platform=wayland --enable-features=UseOzonePlatform \
    --no-first-run --disable-translate --disable-features=TranslateUI \
    --overscroll-history-navigation=0 --check-for-update-interval=31536000
