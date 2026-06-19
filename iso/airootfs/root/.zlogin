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
    # Niet exec'en: zo kunnen we, als Hyprland onverwacht stopt, de reden naar de
    # seriële poort schrijven (diagnose; zichtbaar in een VM-/CI-boottest).
    Hyprland >/tmp/hyprland.log 2>&1
    echo "LUMINOSITY_HYPR_EXITED rc=$? :: $(tail -n 3 /tmp/hyprland.log 2>/dev/null | tr '\n' '|')" \
        > /dev/ttyS0 2>/dev/null || true
fi
