#!/usr/bin/env bash
# Luminosity Installer — installeert Luminosity OS op de gekozen schijf.
#
# Leest de config als JSON op stdin (door server.py aangeleverd) en print:
#   PROGRESS <pct>      voortgang (0-100)
#   <vrije tekst>       logregel voor de gebruiker
#   DONE                geslaagd
#   ERROR <melding>     mislukt
#
# EERLIJK: dit script is niet in deze omgeving uitgevoerd (er is geen echte
# doel-schijf of boot). Het is bedoeld om in de live-ISO als root te draaien.
# Het partitioneert, doet pacstrap, configureert in een chroot en schrijft de
# bootloader — de standaard Arch-installatiestappen.

set -uo pipefail

p()    { echo "PROGRESS $1"; }
log()  { echo "$1"; }
fail() { echo "ERROR $1"; exit 1; }

# --- Config inlezen (JSON op stdin -> shell-variabelen via python3) ---
CFG="$(cat)"
veld() { printf '%s' "$CFG" | python3 -c "import json,sys;print(json.load(sys.stdin).get('$1',''))"; }

DISK="$(veld disk)"
LAYOUT="$(veld layout)"
HOSTNAME="$(veld hostname)"
USERNAME="$(veld username)"
FULLNAME="$(veld fullname)"
PASSWORD="$(veld password)"
TIMEZONE="$(veld timezone)"
KEYBOARD="$(veld keyboard)"
UPDATES="$(veld updates)"

[ "$(id -u)" = "0" ] || fail "De installer moet als root draaien."
[ -n "$DISK" ] || fail "Geen schijf gekozen."
TARGET="/dev/$DISK"
[ -b "$TARGET" ] || fail "Schijf $TARGET bestaat niet."

# Veiligheidscheck: weiger de schijf waarop de live-ISO draait.
LIVE_SRC="$(findmnt -no SOURCE /run/archiso/bootmnt 2>/dev/null || true)"
if [ -n "$LIVE_SRC" ] && [[ "$LIVE_SRC" == "$TARGET"* ]]; then
    fail "Dit is de schijf waarvan de installer zelf boot. Kies een andere schijf."
fi

# Doelpakketten voor het geïnstalleerde systeem (geen archiso/live-pakketten).
TARGET_PACKAGES=(
  base linux linux-firmware
  sudo networkmanager nano zsh
  hyprland xdg-desktop-portal-hyprland qt6-base qt6-declarative wayland foot
  python git rsync
  mkinitcpio
)

log "Installatie gestart voor /dev/$DISK ($LAYOUT)"; p 2

# --- 1. Partitioneren + formatteren ---
if [ "$LAYOUT" = "whole" ]; then
    log "Schijf wissen en partities maken (EFI + root)…"
    wipefs -a "$TARGET"            || fail "Kon $TARGET niet wissen."
    sgdisk -Z "$TARGET"           >/dev/null 2>&1 || true
    sgdisk -n1:0:+512M -t1:ef00 -c1:EFI \
           -n2:0:0     -t2:8300 -c2:luminosity "$TARGET" >/dev/null \
        || fail "Partitioneren mislukt."
    # p1/p2 voor sd*, p1/p2 voor nvme heet nvme0n1p1
    if [[ "$DISK" == nvme* || "$DISK" == mmcblk* ]]; then EFI="${TARGET}p1"; ROOT="${TARGET}p2"
    else EFI="${TARGET}1"; ROOT="${TARGET}2"; fi
    sleep 1; partprobe "$TARGET" 2>/dev/null || true
    log "Bestandssystemen aanmaken…"
    mkfs.fat -F32 "$EFI"   >/dev/null 2>&1 || fail "Kon EFI niet formatteren."
    mkfs.ext4 -F "$ROOT"   >/dev/null 2>&1 || fail "Kon root niet formatteren."
else
    fail "Handmatige indeling: partitioneer zelf en mount root op /mnt, daarna verder."
fi
p 12

# --- 2. Mounten ---
log "Partities mounten…"
mount "$ROOT" /mnt              || fail "Kon root niet mounten."
mkdir -p /mnt/boot
mount "$EFI" /mnt/boot          || fail "Kon EFI niet mounten."
p 16

# --- 3. Basissysteem (pacstrap) ---
log "Basissysteem installeren (dit kan even duren)…"
pacstrap -K /mnt "${TARGET_PACKAGES[@]}" || fail "pacstrap mislukt (netwerk nodig)."
p 62

# --- 4. fstab ---
log "Bestandssysteem-tabel (fstab) schrijven…"
genfstab -U /mnt >> /mnt/etc/fstab || fail "genfstab mislukt."
p 66

# --- 5. Engine + schil + modules naar het doelsysteem ---
log "Luminosity-engine en -schil plaatsen…"
mkdir -p /mnt/opt/luminosity
cp -r /opt/luminosity/. /mnt/opt/luminosity/ 2>/dev/null || true
p 70

# --- 6. Configuratie in de chroot ---
log "Systeem configureren (tijdzone, taal, account, autostart)…"
cat > /mnt/root/lum-chroot.sh <<CHROOT
#!/usr/bin/env bash
set -e
ln -sf "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime
hwclock --systohc || true
sed -i 's/^#\(en_US.UTF-8\)/\1/; s/^#\(nl_NL.UTF-8\)/\1/' /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "KEYMAP=$KEYBOARD" > /etc/vconsole.conf
echo "$HOSTNAME" > /etc/hostname
printf '127.0.0.1 localhost\n::1 localhost\n127.0.1.1 %s\n' "$HOSTNAME" > /etc/hosts

# Account
useradd -m -G wheel -s /usr/bin/zsh -c "$FULLNAME" "$USERNAME"
echo "$USERNAME:$PASSWORD" | chpasswd
passwd -l root
echo "%wheel ALL=(ALL:ALL) ALL" > /etc/sudoers.d/10-wheel
chmod 440 /etc/sudoers.d/10-wheel

systemctl enable NetworkManager

# initramfs
mkinitcpio -P

# Autostart: log de gebruiker in op tty1 en start Hyprland -> Luminosity-schil
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf <<EOF
[Service]
ExecStart=
ExecStart=-/usr/bin/agetty --autologin $USERNAME --noclear %I 38400 linux
EOF

install -d -o "$USERNAME" -g "$USERNAME" /home/$USERNAME/.config/hypr
cat > /home/$USERNAME/.config/hypr/hyprland.conf <<EOF
monitor = , highres, auto, 1
exec-once = /usr/local/bin/luminosity-shell
general { gaps_in = 0; gaps_out = 0; border_size = 0 }
decoration { rounding = 0 }
misc { force_default_wallpaper = 0; disable_hyprland_logo = true; disable_splash_rendering = true; background_color = rgb(0a0c12) }
\\\$mod = SUPER
bind = \\\$mod, RETURN, exec, foot
bind = \\\$mod SHIFT, Q, exit
EOF
cat >> /home/$USERNAME/.zprofile <<EOF
if [ -z "\\\$WAYLAND_DISPLAY" ] && [ "\\\$(tty)" = "/dev/tty1" ]; then
    export PYTHONPATH=/opt/luminosity:\\\$PYTHONPATH
    export WLR_RENDERER_ALLOW_SOFTWARE=1
    export WLR_NO_HARDWARE_CURSORS=1
    # Hardware-versnelling eerst; bij een crash (kapotte gast-GL) terugvallen op
    # Mesa software-GL. Zo werkt het op echte GPU's én in VM's.
    Hyprland >/tmp/hyprland.log 2>&1
    if [ "\\\$?" -ne 0 ]; then
        LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe exec Hyprland
    fi
fi
EOF
chown -R "$USERNAME:$USERNAME" /home/$USERNAME/.config /home/$USERNAME/.zprofile

# Schil-launcher
cat > /usr/local/bin/luminosity-shell <<EOF
#!/usr/bin/env bash
export PYTHONPATH=/opt/luminosity:\\\$PYTHONPATH
if command -v quickshell >/dev/null; then
    exec quickshell -p /opt/luminosity/luminosity-shell/qml/shell.qml
fi
exec foot bash -c "cd /opt/luminosity && python -m luminosity_engine.cli"
EOF
chmod 755 /usr/local/bin/luminosity-shell

# Bootloader (systemd-boot, UEFI)
bootctl install
ROOT_UUID=\$(findmnt -no UUID /)
cat > /boot/loader/loader.conf <<EOF
default luminosity
timeout 2
EOF
cat > /boot/loader/entries/luminosity.conf <<EOF
title   Luminosity OS
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options root=UUID=\$ROOT_UUID rw quiet
EOF
CHROOT
chmod +x /mnt/root/lum-chroot.sh
arch-chroot /mnt /root/lum-chroot.sh || fail "Configuratie in chroot mislukt."
rm -f /mnt/root/lum-chroot.sh
p 90

# --- 7. Optioneel bijwerken ---
if [ "$UPDATES" = "True" ] || [ "$UPDATES" = "true" ]; then
    log "Systeem bijwerken…"
    arch-chroot /mnt pacman -Syu --noconfirm >/dev/null 2>&1 || log "(bijwerken overgeslagen)"
fi
p 96

# --- 8. Afronden ---
log "Afronden en ontkoppelen…"
umount -R /mnt 2>/dev/null || true
p 100
log "Installatie voltooid. Je kunt herstarten."
echo "DONE"
