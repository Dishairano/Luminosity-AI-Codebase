# fix for screen readers
if grep -Fqa 'accessibility=' /proc/cmdline &> /dev/null; then
    setopt SINGLE_LINE_ZLE
fi

~/.automated_script.sh

# Luminosity OS: start de grafische schil automatisch op tty1 (OS2).
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export PYTHONPATH=/opt/luminosity:$PYTHONPATH
    exec Hyprland
fi
