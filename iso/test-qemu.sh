#!/usr/bin/env bash
# Luminosity OS - test de gebouwde ISO in QEMU.
#
# LET OP (eerlijk): dit script start een echte VM. In een omgeving zonder
# QEMU of zonder grafische/KVM-toegang kun je het niet draaien; het is bedoeld
# als reproduceerbare teststap op een werkstation. Er worden hier dus geen
# echte boot-resultaten gegenereerd.
#
# Gebruik:
#   ./test-qemu.sh                         # zoekt iso/out/*.iso
#   ./test-qemu.sh pad/naar/luminosity.iso
#   HEADLESS=1 ./test-qemu.sh              # zonder venster (serie-console)

set -euo pipefail
HIER="$(cd "$(dirname "$0")" && pwd)"
ISO="${1:-$(ls "$HIER/out/"*.iso 2>/dev/null | head -1 || true)}"

if [ -z "$ISO" ] || [ ! -f "$ISO" ]; then
    echo "!! Geen ISO gevonden. Bouw er eerst een met ./build-docker.sh" >&2
    exit 1
fi
if ! command -v qemu-system-x86_64 >/dev/null; then
    echo "!! qemu-system-x86_64 niet gevonden. Installeer QEMU (bv. 'pacman -S qemu-desktop')." >&2
    exit 1
fi

echo ">> Boot Luminosity OS in QEMU: $ISO"
ARGS=(-m 4096 -smp 2 -boot d -cdrom "$ISO" -name "Luminosity OS")
# KVM-versnelling gebruiken als het beschikbaar is.
[ -w /dev/kvm ] && ARGS+=(-enable-kvm -cpu host)
# UEFI-boot als de firmware aanwezig is (anders valt QEMU terug op BIOS/syslinux).
for ovmf in /usr/share/edk2/x64/OVMF_CODE.4m.fd /usr/share/OVMF/OVMF_CODE.fd; do
    [ -f "$ovmf" ] && { ARGS+=(-drive "if=pflash,format=raw,readonly=on,file=$ovmf"); break; }
done
if [ "${HEADLESS:-0}" = "1" ]; then
    ARGS+=(-nographic -serial mon:stdio)
fi

set -x
exec qemu-system-x86_64 "${ARGS[@]}"
