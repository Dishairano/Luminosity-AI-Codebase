#!/usr/bin/env bash
# Wordt door archiso in de chroot uitgevoerd tijdens het bouwen.
set -e
systemctl enable NetworkManager.service
systemctl enable getty@tty1.service
systemctl enable luminosity-installer.service
