# fix for screen readers
if grep -Fqa 'accessibility=' /proc/cmdline &> /dev/null; then
    setopt SINGLE_LINE_ZLE
fi

~/.automated_script.sh

# De grafische schil draait als onbevoorrechte gebruiker 'lumo' (Hyprland en
# Chromium weigeren als root) — zie /home/lumo/.bash_profile. Root logt hier niet
# automatisch grafisch in.
