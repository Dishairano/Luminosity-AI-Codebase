#!/usr/bin/env bash
# Luminosity OS - bouwt de bootbare ISO (OS4).
#
# Werkt op een Arch Linux-systeem of in een Arch-container (zie build-docker.sh).
# Stappen:
#   1. Kopieer engine + schil + modules in het OS (airootfs/opt/luminosity).
#   2. Zorg voor een geldige lokale repo (optioneel met quickshell uit de AUR).
#   3. Roep mkarchiso aan -> resultaat: out/luminosity-*.iso
#
# Gebruik (op Arch):                 sudo ./build.sh
# Met quickshell uit de AUR:         sudo ./build.sh --with-quickshell
# Via Docker:                        ./build-docker.sh   (zie README.md)

set -euo pipefail
HIER="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HIER/.." && pwd)"
REPO=/tmp/luminosity-repo
MET_QUICKSHELL=0
[ "${1:-}" = "--with-quickshell" ] && MET_QUICKSHELL=1

echo ">> 1. Engine, schil en modules in het OS plaatsen..."
rm -rf "$HIER/airootfs/opt/luminosity"
mkdir -p "$HIER/airootfs/opt/luminosity"
cp -r "$ROOT/luminosity_engine" "$HIER/airootfs/opt/luminosity/"
cp -r "$ROOT/luminosity-shell"  "$HIER/airootfs/opt/luminosity/"
cp -r "$ROOT/modules"           "$HIER/airootfs/opt/luminosity/"
find "$HIER/airootfs/opt/luminosity" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

if ! command -v mkarchiso >/dev/null; then
    echo "!! mkarchiso niet gevonden. Installeer 'archiso' of gebruik build-docker.sh." >&2
    exit 1
fi

echo ">> 2. Lokale repo voorbereiden ($REPO)..."
# pacman.conf verwijst naar [luminosity-local]; die repo MOET een geldige db hebben,
# anders faalt mkarchiso. We maken altijd een (eventueel lege) geldige db aan.
rm -rf "$REPO" && mkdir -p "$REPO"

if [ "$MET_QUICKSHELL" = "1" ]; then
    echo ">>    quickshell (AUR) bouwen..."
    # makepkg mag niet als root: bouw als een onbevoorrechte gebruiker.
    BOUWER="${SUDO_USER:-builder}"
    id "$BOUWER" >/dev/null 2>&1 || useradd -m "$BOUWER"
    install -d -o "$BOUWER" /tmp/qs-build
    sudo -u "$BOUWER" bash -c '
        cd /tmp/qs-build && rm -rf quickshell &&
        git clone --depth=1 https://aur.archlinux.org/quickshell.git &&
        cd quickshell && makepkg -s --noconfirm
    ' && cp /tmp/qs-build/quickshell/*.pkg.tar.zst "$REPO"/ \
      || echo "(!! quickshell-build mislukt; ISO bouwt door zonder quickshell)"
fi

# Maak/actualiseer de repo-db (werkt ook als er 0 pakketten zijn).
shopt -s nullglob
pkgs=("$REPO"/*.pkg.tar.zst)
if [ ${#pkgs[@]} -gt 0 ]; then
    repo-add "$REPO/luminosity-local.db.tar.gz" "${pkgs[@]}" >/dev/null 2>&1 || true
else
    # Lege maar geldige db zodat pacman de repo accepteert.
    tar -cf - --files-from /dev/null | gzip > "$REPO/luminosity-local.db.tar.gz"
    ln -sf luminosity-local.db.tar.gz "$REPO/luminosity-local.db"
    cp "$REPO/luminosity-local.db.tar.gz" "$REPO/luminosity-local.files.tar.gz"
    ln -sf luminosity-local.files.tar.gz "$REPO/luminosity-local.files"
fi
shopt -u nullglob

# Voeg quickshell alleen toe aan de pakketlijst als het pakket echt beschikbaar is.
sed -i '/^quickshell$/d' "$HIER/packages.x86_64"
if ls "$REPO"/quickshell-*.pkg.tar.zst >/dev/null 2>&1; then
    echo "quickshell" >> "$HIER/packages.x86_64"
    echo ">>    quickshell toegevoegd aan de pakketlijst."
fi

echo ">> 3. ISO bouwen met mkarchiso..."
# Alleen de work-map en oude ISO's wissen; out/ blijft bestaan zodat een
# meelopend build-log (build-docker.sh tee't hierheen) niet wordt verwijderd.
rm -rf "$HIER/work"
mkdir -p "$HIER/out"
rm -f "$HIER/out/"*.iso
mkarchiso -v -w "$HIER/work" -o "$HIER/out" "$HIER"

echo ">> Klaar! De ISO staat in: $HIER/out/"
ls -lh "$HIER/out/"/*.iso 2>/dev/null || true
