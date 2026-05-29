# Luminosity OS: start de grafische schil automatisch op tty1.
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export PYTHONPATH=/opt/luminosity:$PYTHONPATH
    exec Hyprland
fi
