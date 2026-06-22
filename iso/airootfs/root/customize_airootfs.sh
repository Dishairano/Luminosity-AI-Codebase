#!/usr/bin/env bash
# Wordt door archiso in de chroot uitgevoerd tijdens het bouwen.
set -e
systemctl enable NetworkManager.service
systemctl enable getty@tty1.service
systemctl enable luminosity-installer.service

# Boot-splash: zet ons Plymouth-thema als standaard (de initramfs-bouw verderop
# bundelt daardoor het 'luminosity'-thema + de script-plugin).
plymouth-set-default-theme luminosity

# Onbevoorrechte live-gebruiker voor de grafische sessie. Hyprland en Chromium
# weigeren als root te draaien; de installatie zelf draait als root via de
# luminosity-installer.service. Groepen video/input voor GPU/invoer, uucp/tty
# zodat diagnose-markeringen naar de seriële poort geschreven kunnen worden,
# wheel voor eventueel beheer.
# Home /home/lumo bestaat al (uit airootfs), dus geen -m.
useradd -d /home/lumo -s /bin/bash -G wheel,video,input,uucp,tty lumo
passwd -d lumo                       # wachtwoordloos (live-omgeving)
chown -R lumo:lumo /home/lumo
# lumo mag de installatie (root-service) starten zonder wachtwoord — niet nodig
# voor de GUI, maar handig voor de 'probeer'-terminal.
echo 'lumo ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/10-lumo
chmod 440 /etc/sudoers.d/10-lumo
