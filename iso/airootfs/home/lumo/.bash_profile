# Luminosity OS — start de grafische schil automatisch op tty1, als gebruiker lumo.
# (Hyprland en Chromium weigeren als root; de installatie zelf draait als root via
#  luminosity-installer.service.)
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export PYTHONPATH=/opt/luminosity:$PYTHONPATH
    # Sta software-rendering (Mesa llvmpipe) toe als er geen werkende hardware-GL
    # is. Hardware-GL wordt gebruikt indien beschikbaar (integrated of discrete GPU);
    # dit voorkomt alleen een zwart scherm op GPU-loze/VM-systemen.
    export WLR_RENDERER_ALLOW_SOFTWARE=1
    export WLR_NO_HARDWARE_CURSORS=1
    # Boot-splash naadloos overdragen: laat het beeld staan tot Hyprland tekent.
    plymouth quit --retain-splash 2>/dev/null || true

    # Eerst hardware-versnelling proberen (werkt op echte GPU's én VM's met
    # werkende 3D). Crasht Hyprland meteen op een kapotte gast-GL (bv. VirtualBox
    # VMSVGA), dan automatisch een tweede poging met Mesa software-GL (llvmpipe).
    # Zo houden we GPU-versnelling waar het kan, met software als nette terugval.
    Hyprland >/tmp/hyprland.log 2>&1
    rc=$?
    if [ "$rc" -ne 0 ]; then
        echo "LUMINOSITY_HYPR_RETRY_SOFTWARE rc=$rc" > /dev/ttyS0 2>/dev/null || true
        LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe Hyprland >/tmp/hyprland.log 2>&1
        rc=$?
    fi
    echo "LUMINOSITY_HYPR_EXITED rc=$rc :: $(tail -n 3 /tmp/hyprland.log 2>/dev/null | tr '\n' '|')" \
        > /dev/ttyS0 2>/dev/null || true
fi
