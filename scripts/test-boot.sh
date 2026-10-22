#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISO="$ROOT/build/myos.iso"
TIME_LIMIT_SECONDS="${QEMU_BOOT_TIMEOUT_SECONDS:-10}"

if ! command -v qemu-system-i386 >/dev/null 2>&1; then
    echo "ERROR: qemu-system-i386 was not found. Install qemu-system-x86."
    exit 1
fi
if ! command -v timeout >/dev/null 2>&1; then
    echo "ERROR: the 'timeout' command was not found (install coreutils)."
    exit 1
fi
if [[ ! -s "$ISO" ]]; then
    echo "ERROR: bootable ISO not found or empty: $ISO"
    echo "Run ./scripts/build.sh first."
    exit 1
fi

echo "Starting headless QEMU boot test (time limit: ${TIME_LIMIT_SECONDS}s)..."
set +e
OUTPUT="$(timeout "${TIME_LIMIT_SECONDS}s" qemu-system-i386 \
    -machine pc \
    -m 64M \
    -cdrom "$ISO" \
    -boot order=d \
    -display none \
    -serial stdio \
    -monitor none \
    -no-reboot \
    -no-shutdown 2>&1)"
QEMU_STATUS=$?
set -e

printf '%s\n' "$OUTPUT"

if grep -Fq "Welcome to MyOS!" <<< "$OUTPUT"; then
    echo "PASS: kernel booted and printed the expected serial message."
    exit 0
fi

if [[ $QEMU_STATUS -eq 124 ]]; then
    echo "ERROR: QEMU reached the ${TIME_LIMIT_SECONDS}s time limit without the expected serial message."
elif [[ $QEMU_STATUS -ne 0 ]]; then
    echo "ERROR: QEMU exited with status $QEMU_STATUS before the expected serial message appeared."
else
    echo "ERROR: QEMU exited without printing the expected serial message."
fi
exit 1
