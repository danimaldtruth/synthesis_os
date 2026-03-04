#!/bin/bash

# =====================================================
# SYNTHESIS OS - PRE-INSTALL & LAUNCHER
# =====================================================

clear
echo "====================================================="
echo "       SYNTHESIS OS - STAGE 1 (PRE-INSTALLER)        "
echo "====================================================="

# 1. Update system clock for accurate HTTPS/Pacman signatures
echo "[*] Synchronizing system clock (NTP)..."
timedatectl set-ntp true

# 2. Ensure Python and dependencies are present on the Live ISO
echo "[*] Syncing pacman databases and installing Python..."
pacman -Sy --noconfirm python git curl wget

# 3. Optional Pause for Partitioning
echo ""
echo "====================================================="
lsblk -o NAME,SIZE,TYPE | grep -E 'disk|part'
echo "====================================================="
echo "If you have not partitioned your drive yet, press Ctrl+C now,"
echo "run 'cfdisk /dev/nvme0n1' (or your drive), and restart this script."
echo "Press ENTER to continue to the Python Installer..."
read -r

# 4. Generate the Python Installer Script
echo "[*] Generating Synthesis OS Python Installer..."

cat << 'EOF' > synthesis_installer.py
import os
import subprocess
import sys

def clear_screen():
    os.system('clear')

def print_banner():
    print("=====================================================")
    print("                SYNTHESIS OS INSTALLER                ")
    print("=====================================================")
    print(" ThinkPad | macOS UI | Hybrid AI | Cyber | Audio     ")
    print("=====================================================\n")

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def check_network():
    print("Verifying network connection...")
    response = subprocess.run("ping -c 1 archlinux.org", shell=True, capture_output=True)
    if response.returncode != 0:
        clear_screen()
        print("--- NETWORK ERROR ---")
        print("Connect to Wi-Fi via 'iwctl' before running.")
        sys.exit(1)
    print("Network connection confirmed.\n")

def get_drives():
    return run_command("lsblk -o NAME,SIZE,TYPE | grep -E 'disk|part'")

def create_setup_script(username, password, hostname, gpu_choice, cpu_choice, kbd_layout):
    if gpu_choice == "1":
        gpu_pkgs = '"nvidia", "nvidia-utils", "egl-wayland", "cuda", "cudnn"'
        nvidia_grub = "run(\"sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\\\"/GRUB_CMDLINE_LINUX_DEFAULT=\\\"nvidia_drm.modeset=1 /' /etc/default/grub\")"
    else:
        gpu_pkgs = '"mesa", "vulkan-radeon", "intel-media-driver", "libva-intel-driver", "opencl-icd-loader"'
        nvidia_grub = "# No NVIDIA parameter needed"

    cpu_pkg = "intel-ucode" if cpu_choice == "1" else "amd-ucode"

    setup_script_content = f"""#!/usr/bin/env python3
import os
import subprocess

USERNAME = "{username}"
PASSWORD = "{password}"
HOSTNAME = "{hostname}"
KBD = "{kbd_layout}"

OFFICIAL_PACKAGES = [
    "plasma-meta", "sddm", "konsole", "dolphin", "zsh", "zsh-completions", "starship",
    "pipewire", "pipewire-jack", "pipewire-pulse", "pipewire-alsa", "wireplumber", "pavucontrol",
    "kaccounts-providers", "kio-gdrive", "discord", "timeshift", "ufw", "gufw", "gnome-keyring",
    "tlp", "tlp-rdw", "sof-firmware", "acpi", "fprintd", "bluez", "bluez-utils",
    "reflector", "zram-generator", "{cpu_pkg}",
    "docker", "docker-compose", "neovim", "nmap", "wireshark-qt", "tor", "nyx", "torbrowser-launcher",
    "virt-manager", "qemu-desktop", "libvirt", "edk2-ovmf", "dnsmasq", "iptables-nft",
    "krita", "inkscape", "ardour", "guitarix", "lsp-plugins", "calf", "dragonfly-reverb",
    "jupyterlab", "ollama", "focuswriter", "obsidian",
    "steam", "lutris", "wine-staging", "grub", "efibootmgr", "base-devel", "git",
    {gpu_pkgs}
]

AUR_PACKAGES = [
    "whitesur-kde-theme-git", "whitesur-icon-theme-git", "whitesur-cursor-theme-git",
    "apple-fonts", "ttf-ms-fonts", "polonium", "mullvad-vpn-bin", "chatbox-bin", 
    "google-chrome", "1password", "visual-studio-code-bin", "reaper-bin", "yabridge-bin", "vital-synth"
]

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    run("ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime")
    run("hwclock --systohc")
    with open("/etc/locale.gen", "a") as f: f.write("en_US.UTF-8 UTF-8\\n")
    run("locale-gen")
    with open("/etc/locale.conf", "w") as f: f.write("LANG=en_US.UTF-8\\n")
    with open("/etc/vconsole.conf", "w") as f: f.write(f"KEYMAP={{KBD}}\\n")
    with open("/etc/hostname", "w") as f: f.write(HOSTNAME + "\\n")
    
    with open("/etc/systemd/zram-generator.conf", "w") as f:
        f.write("[zram0]\\nzram-size = min(ram / 2, 4096)\\ncompression-algorithm = zstd\\n")

    with open("/etc/security/limits.d/99-realtime.conf", "w") as f:
        f.write("@realtime - rtprio 98\\n@realtime - memlock unlimited\\n")
    run("groupadd realtime || true")

    with open("/etc/pacman.conf", "r") as f: lines = f.readlines()
    with open("/etc/pacman.conf", "w") as f:
        enable_m = False
        for line in lines:
            if line.startswith("#[multilib]"): f.write("[multilib]\\n"); enable_m = True
            elif enable_m and line.startswith("#Include"): f.write("Include = /etc/pacman.d/mirrorlist\\