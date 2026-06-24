#!/usr/bin/env bash
# Luminosity OS - archiso profieldefinitie.
# Bepaalt de naam, het label en de bestandsrechten van de ISO.
# shellcheck disable=SC2034

iso_name="luminosity"
iso_label="LUMINOSITY"
iso_publisher="Luminosity OS <https://github.com/Dishairano>"
iso_application="Luminosity OS - Linux in gewone taal"
iso_version="0.2.9"
install_dir="lum"
buildmodes=('iso')
bootmodes=('bios.syslinux' 'uefi.systemd-boot')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M')

# Bestandsrechten: zorg dat onze scripts/configs uitvoerbaar/leesbaar zijn.
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/.config/hypr/hyprland.conf"]="0:0:644"
  ["/usr/local/bin/luminosity"]="0:0:755"
  ["/usr/local/bin/luminosity-shell"]="0:0:755"
  ["/opt/luminosity-installer/launch-installer.sh"]="0:0:755"
  ["/opt/luminosity-installer/server.py"]="0:0:755"
  ["/opt/luminosity-installer/install.sh"]="0:0:755"
)
