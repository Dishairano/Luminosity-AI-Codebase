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

# Fallback: start de server zelf als de systemd-service (nog) niet luistert.
if ! (exec 3<>"/dev/tcp/127.0.0.1/$PORT") 2>/dev/null; then
    python3 "$HIER/server.py" &
    trap 'kill %1 2>/dev/null' EXIT
else
    exec 3>&-
fi

# Wachten tot de poort luistert (zonder curl-afhankelijkheid)
for _ in $(seq 1 100); do
    (exec 3<>"/dev/tcp/127.0.0.1/$PORT") 2>/dev/null && { exec 3>&-; break; }
    sleep 0.2
done

# Kiosk-browser openen op de installer
exec chromium \
    --kiosk --app="http://127.0.0.1:$PORT/" \
    --ozone-platform=wayland --enable-features=UseOzonePlatform \
    --no-first-run --disable-translate --disable-features=TranslateUI \
    --overscroll-history-navigation=0 --check-for-update-interval=31536000
