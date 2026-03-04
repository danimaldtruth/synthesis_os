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
    "plasma-meta", "sddm", "konsole", "dolphin", "remmina",
    "merkuro", "thunderbird", "vlc", "zsh", "zsh-completions", "starship",
    "pipewire", "pipewire-jack", "pipewire-pulse", "pipewire-alsa", "wireplumber",
    # System Integration & Security
    "kaccounts-providers", "kio-gdrive", "discord", "timeshift", "ufw", "gufw", "gnome-keyring",
    # Laptop Hardware (ThinkPad T14 Gen 2)
    "sof-firmware", "power-profiles-daemon", "acpi", "fprintd", "bluez", "bluez-utils",
    # EndeavourOS speed tweaks & Hardware support
    "reflector", {cpu_pkg},
    # Cyber, Networking & Tor
    "docker", "docker-compose", "neovim", "nmap", "wireshark-qt", "tor", "nyx", "torbrowser-launcher",
    # Virtualization (Whonix Support)
    "virt-manager", "qemu-desktop", "libvirt", "edk2-ovmf", "dnsmasq", "iptables-nft",
    # AI Engine & Writing
    "ollama", "chatbox-bin", "obsidian", "focuswriter", "jupyterlab",
    # Pro-Audio (Native VST stack)
    "ardour", "guitarix", "lsp-plugins", "calf", "dragonfly-reverb", "x42-plugins", "geonkick", "drumgizmo",
    # Art & Media
    "krita", "inkscape",
    # Core & Gaming
    "steam", "lutris", "wine-staging", "grub", "efibootmgr", "base-devel", "git", "fwupd",
    {gpu_pkgs}
]

AUR_PACKAGES = [
    "whitesur-kde-theme-git", "whitesur-icon-theme-git", "whitesur-cursor-theme-git",
    "apple-fonts", "ttf-ms-fonts", "polonium", "mullvad-vpn-bin", 
    "google-chrome", "1password", "visual-studio-code-bin", "postman-bin", 
    "lazydocker-bin", "burpsuite", "reaper-bin", "yabridge-bin", "spotify", "vital-synth", "surge-xt"
]

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def configure_pacman():
    with open("/etc/pacman.conf", "r") as f:
        lines = f.readlines()
    with open("/etc/pacman.conf", "w") as f:
        enable_m = False
        for line in lines:
            if line.startswith("#[multilib]"):
                f.write("[multilib]\\n")
                enable_m = True
            elif enable_m and line.startswith("#Include = /etc/pacman.d/mirrorlist"):
                f.write("Include = /etc/pacman.d/mirrorlist\\n")
                enable_m = False
            elif line.startswith("#ParallelDownloads"):
                f.write("ParallelDownloads = 10\\n")
            elif line.startswith("#Color"):
                f.write("Color\\nILoveCandy\\n")
            else:
                f.write(line)

def main():
    # Base OS Config
    run("ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime")
    run("hwclock --systohc")
    with open("/etc/locale.gen", "a") as f: f.write("en_US.UTF-8 UTF-8\\n")
    run("locale-gen")
    with open("/etc/locale.conf", "w") as f: f.write("LANG=en_US.UTF-8\\n")
    with open("/etc/hostname", "w") as f: f.write(HOSTNAME + "\\n")
    
    # Enable Daemons
    run("systemctl enable NetworkManager sddm docker tor libvirtd ufw power-profiles-daemon fprintd bluetooth reflector.timer")
    
    # Create User with Zsh as default shell
    run(f"useradd -m -G wheel,wireshark,docker,libvirt,kvm -s /bin/zsh {{USERNAME}}")
    run(f"echo '{{USERNAME}}:{{PASSWORD}}' | chpasswd")
    with open("/etc/sudoers.d/wheel", "w") as f: f.write("%wheel ALL=(ALL:ALL) NOPASSWD: ALL\\n")

    configure_pacman()
    run("pacman -Sy --noconfirm")
    
    # Fast Mirror Ranking
    run("reflector --latest 15 --protocol https --sort rate --save /etc/pacman.d/mirrorlist")
    run("pacman -S --noconfirm " + " ".join(OFFICIAL_PACKAGES))

    # Bootloader (UEFI)
    run("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB")
    run("grub-mkconfig -o /boot/grub/grub.cfg")

    # AUR Helper (Yay)
    run(f"su - {{USERNAME}} -c 'git clone https://aur.archlinux.org/yay.git /tmp/yay && cd /tmp/yay && makepkg -si --noconfirm'")
    run(f"su - {{USERNAME}} -c 'yay -S --noconfirm " + " ".join(AUR_PACKAGES) + "'")
    
    run("systemctl enable mullvad-daemon")

    # Workspace Scaffolding
    run(f"su - {{USERNAME}} -c 'ssh-keygen -t ed25519 -C \"danimaldtruth\" -f ~/.ssh/id_ed25519 -N \"\"'")
    for p in ["Serotonin_Social", "Justice_Toolkit", "Project_2025_Reversal"]:
        run(f"su - {{USERNAME}} -c 'mkdir -p ~/Projects/{{p}}'")
    
    # Shell Configuration (Starship & Aliases)
    zshrc = f"/home/{{USERNAME}}/.zshrc"
    with open(zshrc, "a") as f:
        f.write('\\neval "$(starship init zsh)"\\nalias update="yay -Syu"\\nalias d="docker"\\nalias dc="docker-compose"\\nalias vpn="mullvad"\\nalias proxmox="ssh root@YOUR_PROXMOX_IP"\\n')

    # Security: Re-enable Sudo password
    with open("/etc/sudoers.d/wheel", "w") as f: f.write("%wheel ALL=(ALL:ALL) ALL\\n")

if __name__ == '__main__':
    main()
"""
    with open("/mnt/root/setup.py", "w") as f:
        f.write(setup_script_content)

def main():
    clear_screen()
    check_network()
    print_banner()
    print("Detected Storage Hardware:")
    print(get_drives())
    
    boot_p = input("\\nEnter BOOT partition (e.g., /dev/nvme0n1p1): ").strip()
    root_p = input("Enter ROOT partition (e.g., /dev/nvme0n1p2): ").strip()
    cpu_c = input("ThinkPad CPU? (1: Intel, 2: AMD): ").strip()
    gpu_c = input("ThinkPad GPU? (1: NVIDIA, 2: Intel/AMD Only): ").strip()
    user = input("Set Username: ").strip()
    pw = input("Set Password: ").strip()

    print("\\n[1/4] Formatting Partitions...")
    os.system(f"mkfs.fat -F32 {boot_p}")
    os.system(f"mkfs.ext4 -F {root_p}")
    
    print("[2/4] Mounting Filesystem...")
    os.system(f"mount {root_p} /mnt")
    os.system(f"mount --mkdir {boot_p} /mnt/boot")
    
    print("[3/4] Bootstrapping Base System (Pacman Accelerated)...")
    os.system("sed -i 's/#ParallelDownloads = 5/ParallelDownloads = 10/' /etc/pacman.conf")
    os.system("pacstrap -K /mnt base linux linux-firmware networkmanager nano python git sudo")
    os.system("genfstab -U /mnt >> /mnt/etc/fstab")
    
    print("[4/4] Finalizing Synthesis OS Configuration...")
    create_setup_script(user, pw, gpu_c, cpu_c)
    os.system("arch-chroot /mnt /usr/bin/env python /root/setup.py")
    
    print("\\n=====================================================")
    print("FORGE COMPLETE. Pull USB and type 'reboot'.")
    print("=====================================================")

if __name__ == "__main__":
    main()