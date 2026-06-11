#!/usr/bin/env bash
# Start de installer-server en opent de kiosk-browser (fullscreen, Wayland).
# Wordt door Hyprland gestart in de live-ISO (zie airootfs hyprland.conf).
set -u
HIER="$(cd "$(dirname "$0")" && pwd)"
PORT="${LUM_INSTALLER_PORT:-8723}"
export PYTHONPATH=/opt/luminosity:${PYTHONPATH:-}

# Server starten
python3 "$HIER/server.py" &
SRV=$!
trap 'kill "$SRV" 2>/dev/null' EXIT

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
