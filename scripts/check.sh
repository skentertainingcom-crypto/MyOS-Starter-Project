#!/usr/bin/env bash
set -u
for tool in gcc as ld grub-file grub-mkrescue xorriso qemu-system-i386; do
    if command -v "$tool" >/dev/null 2>&1; then
        printf 'OK      %s\n' "$tool"
    else
        printf 'MISSING %s\n' "$tool"
    fi
done
