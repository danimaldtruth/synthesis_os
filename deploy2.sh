#!/bin/bash

# =====================================================
# SYNTHESIS OS - MASTER DEPLOYMENT SCRIPT
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
echo "run 'cfdisk /dev/nvme0n1' (or your target drive), and restart this script."
echo "Press ENTER to continue to the Python Installer..."
read -r

# 4. Generate the Python Installer Script
echo "[*] Generating Synthesis OS Python Payload..."

cat << 'EOF' > synthesis_install.py
import os
import subprocess
import sys

def clear_screen():
    os.system('clear')

def print_banner():
    print("=====================================================")
    print("               SYNTHESIS OS INSTALLER                ")
    print("=====================================================")
    print(" Zsh | ThinkPad | macOS UI | Hybrid AI | Whonix      ")
    print("=====================================================\n")

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def check_network():
    print("Verifying network connection...")
    response = subprocess.run("ping -c 1 archlinux.org", shell=True, capture_output=True)
    if response.returncode != 0:
        clear_screen()
        print("=====================================================")
        print("                 NETWORK ERROR                       ")
        print("=====================================================")
        print("You are not connected to the internet.")
        print("\nFix: iwctl -> station wlan0 scan -> connect 'Name'")
        sys.exit(1)
    print("Network connection confirmed.\n")

def get_drives():
    return run_command("lsblk -o NAME,SIZE,TYPE | grep -E 'disk|part'")

def create_setup_script(username, password, gpu_choice, cpu_choice):
    # Determine Graphics and CPU Microcode
    if gpu_choice == "1":
        gpu_pkgs = '"nvidia", "nvidia-utils", "egl-wayland", "cuda", "cudnn"'
    else:
        gpu_pkgs = '"mesa", "vulkan-radeon", "intel-media-driver", "libva-intel-driver", "opencl-icd-loader"'
    
    cpu_pkg = '"intel-ucode"' if cpu_choice == "1" else '"amd-ucode"'

    setup_script_content = f"""#!/usr/bin/env python3
import os
import subprocess

USERNAME = "{username}"
PASSWORD = "{password}"
HOSTNAME = "synthesis-os"

OFFICIAL_PACKAGES = [
    # Desktop & UI (macOS Style)
    "plasma-meta", "