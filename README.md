# MyOS Starter — first bootable kernel

This is a tiny educational operating-system kernel for x86 PCs. It boots through GRUB using the Multiboot v1 protocol and writes `Welcome to MyOS!` to the classic VGA text buffer.

**This is not yet a mobile OS and will not run directly on a phone.** It is a safe first milestone to learn kernel development in an emulator.

## What is included

- `src/boot.s` — Multiboot header and startup assembly
- `src/kernel.c` — minimal freestanding C kernel
- `linker.ld` — places the kernel at 1 MiB
- `grub/grub.cfg` — GRUB boot menu
- `scripts/build.sh` — compiles the kernel and creates `myos.iso`
- `scripts/run.sh` — starts QEMU
- `scripts/check.sh` — checks the build tools and Multiboot header

## Requirements

- Windows 10 PC, ideally build 19041 or newer
- WSL 2 with Ubuntu
- About 2 GB of free disk space for the Linux environment and packages
- Internet access for initial installation

All tools listed below are free. Commands are run inside **Ubuntu/WSL**, not Windows PowerShell, unless clearly marked.

## 1. Install WSL and Ubuntu

Open **PowerShell as Administrator** and run:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if asked. Open **Ubuntu** from the Start menu and create a Linux username and password.

If that command is not recognized or installation fails:
1. Press `Win + R`, enter `winver`, and note your Windows version/build.
2. Run `wsl --status` in PowerShell.
3. Send the exact error text before trying random commands. Older Windows 10 versions may need updating or the manual WSL installation path.

## 2. Install the build tools

In the Ubuntu terminal, run:

```bash
sudo apt update
sudo apt install build-essential binutils grub-pc-bin grub-common xorriso make qemu-system-x86
```

Type `Y` if asked to confirm. Enter your Ubuntu password if prompted (the terminal will not show characters while you type it).

## 3. Copy the project into Ubuntu

Extract this ZIP in Windows. Then, from Ubuntu, copy the extracted folder into your Linux home directory. If the ZIP was extracted in your Windows Downloads folder, this example usually works:

```bash
cp -r /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/MyOS-Starter ~/myos
cd ~/myos
```

Replace `YOUR_WINDOWS_USERNAME` with your Windows account folder name. Alternatively, download/extract the ZIP directly inside your Ubuntu home folder.

**Tip:** Keep the project under `~/myos` rather than `/mnt/c/...`; Linux builds are usually more reliable and faster in the Linux filesystem.

## 4. Build the ISO

From the project folder in Ubuntu:

```bash
chmod +x scripts/*.sh
./scripts/build.sh
```

The script creates:
- `build/myos` — kernel ELF executable
- `build/myos.iso` — bootable ISO image

It also checks that GRUB recognizes the kernel as a Multiboot v1 kernel.

## 5. Run it in QEMU

Try the graphical emulator first:

```bash
./scripts/run.sh
```

If a QEMU window cannot open because your WSL setup has no graphical display, try the text-mode option:

```bash
./scripts/run.sh --text
```

Text mode needs a terminal that supports curses and QEMU's curses display. If neither mode works, copy the full error message and ask for help. Do not flash the ISO to a USB drive or install it on your real PC.

To close QEMU:
- Graphical window: close the window.
- Text mode: press `Ctrl+A`, release, then press `X`.

Expected output in the emulator:

```text
Welcome to MyOS!
```

## What the files do

### `src/boot.s`
Contains a Multiboot v1 header for GRUB, reserves a 16 KiB stack, and calls `kernel_main`.

### `src/kernel.c`
Writes the message to the legacy VGA text buffer at physical address `0xB8000`. This is intentionally simple and suitable for a first x86 emulator experiment. Modern phones do not use this display interface.

### `linker.ld`
Places the kernel at the 1 MiB mark and keeps the Multiboot header at the beginning of the image.

## Troubleshooting

### `grub-file` reports that the kernel is not Multiboot
Run the build script again and share the complete output. Make sure you did not edit the Multiboot header in `src/boot.s` or remove the `.multiboot` section from `linker.ld`.

### `grub-mkrescue: command not found`
Install the missing tools:

```bash
sudo apt update
sudo apt install grub-pc-bin grub-common xorriso
```

### `qemu-system-i386: command not found`
Install QEMU:

```bash
sudo apt install qemu-system-x86
```

### QEMU opens but the screen is blank
Check whether `./scripts/build.sh` completed successfully. Run:

```bash
grub-file --is-x86-multiboot build/myos
echo $?
```

A status of `0` means the Multiboot check passed. If the emulator still shows a blank screen, send a screenshot and the terminal output.

### `apt` cannot download packages
Check your internet connection, then retry `sudo apt update`. If errors continue, share the exact error text.

### Build commands say “Permission denied”
Run:

```bash
chmod +x scripts/*.sh
```

### `wsl --install` fails
Check the Windows version with `winver` and the WSL status with `wsl --status`. Do not disable security settings or change firmware settings blindly.

## Safety notes

- This project runs in an emulator. Keep it that way while learning.
- Do not write this kernel to your PC's boot drive, repartition your computer, or flash it to your phone.
- This starter uses 32-bit x86 and legacy VGA text output. A real mobile OS needs a different architecture/hardware port, drivers, memory management, security, graphics, networking, power management, and much more.
- A later development milestone should use a dedicated cross-compiler and a modern 64-bit kernel target.

## License

The source files in this starter project are provided under the MIT License. The third-party tools (Ubuntu, GCC, GRUB, QEMU, and related packages) have their own licenses.
