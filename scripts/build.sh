#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required=(gcc as ld grub-file grub-mkrescue xorriso)
for tool in "${required[@]}"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "ERROR: Required tool '$tool' was not found."
        echo "Install tools using the commands in README.md."
        exit 1
    fi
done

mkdir -p build/isodir/boot/grub

echo "[1/4] Assembling startup code..."
as --32 src/boot.s -o build/boot.o

echo "[2/4] Compiling freestanding C kernel..."
gcc -m32 -std=gnu11 -ffreestanding -fno-stack-protector \
    -fno-pie -fno-pic -fno-asynchronous-unwind-tables \
    -Wall -Wextra -Werror -c src/kernel.c -o build/kernel.o

echo "[3/4] Linking kernel..."
ld -m elf_i386 -T linker.ld -nostdlib -o build/myos build/boot.o build/kernel.o

echo "Checking Multiboot v1 header..."
if ! grub-file --is-x86-multiboot build/myos; then
    echo "ERROR: GRUB did not recognize the kernel as Multiboot."
    exit 1
fi

cp build/myos build/isodir/boot/myos
cp grub/grub.cfg build/isodir/boot/grub/grub.cfg

echo "[4/4] Creating bootable ISO..."
grub-mkrescue -o build/myos.iso build/isodir

echo
echo "Build successful!"
echo "Kernel: $ROOT/build/myos"
echo "ISO:    $ROOT/build/myos.iso"
echo "Run it with: ./scripts/run.sh"
