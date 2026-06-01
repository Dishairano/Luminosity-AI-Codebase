#!/usr/bin/env bash
# Luminosity OS - bouwt de ISO in een Arch Linux Docker-container (OS4).
#
# Reden: de buildhost hoeft geen Arch te zijn. De container levert mkarchiso
# (archiso) en pacman, zodat de build reproduceerbaar is. quickshell komt uit de
# AUR en wordt los gebouwd (zie build.sh --with-quickshell).
#
# Gebruik:
#   ./build-docker.sh                 # ISO zonder quickshell (snel, betrouwbaar)
#   ./build-docker.sh --with-quickshell
#
# Vereist: Docker met --privileged (mkarchiso heeft loop-devices/mount nodig).
# Resultaat: iso/out/luminosity-*.iso  +  iso/out/build.log

set -euo pipefail
HIER="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HIER/.." && pwd)"
EXTRA="${1:-}"

mkdir -p "$HIER/out"
echo ">> ISO bouwen in archlinux:latest container... (log: iso/out/build.log)"

docker run --rm --privileged \
    -v "$ROOT":/repo \
    -w /repo/iso \
    archlinux:latest \
    bash -c "
        set -euo pipefail
        pacman -Sy --noconfirm --needed archiso git base-devel sudo &&
        ./build.sh $EXTRA
    " 2>&1 | tee "$HIER/out/build.log"

echo ">> Build-log: $HIER/out/build.log"
ls -lh "$HIER/out/"/*.iso 2>/dev/null || echo "(geen ISO gevonden — zie build.log)"
