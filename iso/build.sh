#!/usr/bin/env bash
# Luminosity OS - bouwt de bootbare ISO (OS4).
#
# Werkt op een Arch Linux-systeem (of via een Arch-container). De stappen:
#   1. Kopieer onze engine + schil in het OS (airootfs/opt/luminosity).
#   2. Bouw quickshell uit de AUR en zet het in een lokale repo.
#   3. Roep mkarchiso aan -> resultaat: out/luminosity-*.iso
#
# Gebruik (op Arch):   sudo ./build.sh
# Of via Docker:       zie README.md (archlinux-container).

set -euo pipefail
HIER="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HIER/.." && pwd)"

echo ">> 1. Engine en schil in het OS plaatsen..."
mkdir -p "$HIER/airootfs/opt/luminosity"
cp -r "$ROOT/luminosity_engine" "$HIER/airootfs/opt/luminosity/"
cp -r "$ROOT/luminosity-shell"  "$HIER/airootfs/opt/luminosity/"
cp -r "$ROOT/modules"           "$HIER/airootfs/opt/luminosity/" 2>/dev/null || true

echo ">> 2. quickshell (AUR) bouwen naar lokale repo /tmp/luminosity-repo..."
if ! command -v mkarchiso >/dev/null; then
    echo "!! mkarchiso niet gevonden. Installeer 'archiso' of gebruik de Docker-methode (README)." >&2
    exit 1
fi
mkdir -p /tmp/luminosity-repo
if [ ! -e /tmp/luminosity-repo/*.pkg.tar.zst ] 2>/dev/null; then
    # makepkg mag niet als root: bouw als bouw-gebruiker.
    sudo -u "${SUDO_USER:-nobody}" bash -c '
        cd /tmp && rm -rf quickshell &&
        git clone https://aur.archlinux.org/quickshell.git &&
        cd quickshell && makepkg -s --noconfirm
    ' || echo "(quickshell-build overgeslagen; voeg het pakket handmatig toe aan /tmp/luminosity-repo)"
    cp /tmp/quickshell/*.pkg.tar.zst /tmp/luminosity-repo/ 2>/dev/null || true
    repo-add /tmp/luminosity-repo/luminosity-local.db.tar.gz /tmp/luminosity-repo/*.pkg.tar.zst 2>/dev/null || true
fi

echo ">> 3. ISO bouwen met mkarchiso..."
rm -rf "$HIER/work" "$HIER/out"
mkarchiso -v -w "$HIER/work" -o "$HIER/out" "$HIER"

echo ">> Klaar! De ISO staat in: $HIER/out/"
ls -lh "$HIER/out/" 2>/dev/null || true
