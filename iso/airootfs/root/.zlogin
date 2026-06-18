# fix for screen readers
if grep -Fqa 'accessibility=' /proc/cmdline &> /dev/null; then
    setopt SINGLE_LINE_ZLE
fi

~/.automated_script.sh

# Luminosity OS: start de grafische schil automatisch op tty1 (OS2).
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export PYTHONPATH=/opt/luminosity:$PYTHONPATH
    # Sta software-rendering (Mesa llvmpipe) toe als er geen werkende hardware-GL
    # is. Hyprland blijft hardware-GL gebruiken wanneer beschikbaar (integrated of
    # discrete GPU); dit voorkomt alleen een zwart scherm op GPU-loze/VM-systemen.
    export WLR_RENDERER_ALLOW_SOFTWARE=1
    export WLR_NO_HARDWARE_CURSORS=1
    exec Hyprland
fi
