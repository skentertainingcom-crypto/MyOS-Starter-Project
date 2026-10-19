#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISO="$ROOT/build/myos.iso"

if [[ ! -f "$ISO" ]]; then
    echo "ISO not found. Build it first:"
    echo "  cd \"$ROOT\" && ./scripts/build.sh"
    exit 1
fi

if ! command -v qemu-system-i386 >/dev/null 2>&1; then
    echo "QEMU is missing. Install it with:"
    echo "  sudo apt install qemu-system-x86"
    exit 1
fi

if [[ "${1:-}" == "--text" ]]; then
    exec qemu-system-i386 -cdrom "$ISO" -boot d -m 256M -display curses
else
    exec qemu-system-i386 -cdrom "$ISO" -boot d -m 256M
fi
