Synthesis OS 💽ThinkPad | macOS UI | Hybrid AI | Cyber | AudioA fully automated, hardened, and tuned Arch Linux deployment script.Synthesis OS is a custom Arch Linux forge designed specifically for high-performance development, low-latency audio production, and cybersecurity homelab environments. It transforms a standard Arch Live USB into a fully configured KDE Plasma 6 environment with a macOS-inspired (WhiteSur) aesthetic out of the box.⚡ System HighlightsPro Audio Ready: Uses the linux-zen kernel, ZRAM, and pre-configured @realtime privileges for glitch-free tracking in Ardour/Guitarix.Cyber Hardened: Ships with UFW (default deny), Tor, Wireshark, Docker, and QEMU/KVM virtualization.ThinkPad Optimized: Integrates tlp with an 80% battery charge threshold to preserve battery health, plus fstrim for SSD longevity.macOS Aesthetic: Pre-loads the WhiteSur theme suite, Apple fonts, and dynamic tiling via Polonium.🛠 Pre-Flight ChecklistBefore running the deployment script, you must boot into the Arch Linux Live USB and prepare your network and disk.Connect to Wi-Fi:If you aren't on Ethernet, use iwctl to connect to your network.Bashiwctl
[iwd]# station wlan0 scan
[iwd]# station wlan0 get-networks
[iwd]# station wlan0 connect YOUR_SSID
Partition Your Drive:The script requires you to have your boot (FAT32/EFI) and root (EXT4 or BTRFS) partitions already created.Bashcfdisk /dev/nvme0n1  # Or /dev/sda
🚀 Quick Start (The Forge)Once your partitions are ready and you have an internet connection, pull the master deployment script and run it.Bash# 1. Download the deployment script
curl -O https://raw.githubusercontent.com/danimaldtruth/Synthesis-OS/main/deploy.sh

# 2. Make it executable
chmod +x deploy.sh

# 3. Execute the forge
./deploy.sh
What deploy.sh does:Syncs the system clock (NTP) to prevent SSL/Pacman signature errors.Installs Python and Git to the live USB environment.Generates the synthesis_installer.py payload.Executes the Python installer to handle the pacstrap, chroot, and system configuration.📦 The StackCategoryTools IncludedAudioPipewire (Jack/Pulse/Alsa), Ardour, Guitarix, LSP Plugins, Vital Synth, ReaperCyber/NetDocker, Nmap, Wireshark, Tor, Mullvad VPN, UFW, DNSMasqDevelopmentZsh, Starship, Neovim, VS Code, Git, Python, JupyterLabVirtualizationQEMU, KVM, Virt-Manager, Docker ComposeCreative/AIKrita, Inkscape, Obsidian, Ollama, FocusWriter🔧 Post-Installation TasksAfter the script finishes, reboot into your new system.Apply the WhiteSur Theme: Open KDE Settings and apply the global WhiteSur theme, icons, and cursors downloaded by the script.Configure Yabridge: If using Windows VSTs in Ardour/Reaper, sync your directories:Bashyabridgectl add ~/.wine/drive_c/Program\ Files/VstPlugins
yabridgectl sync
Set Up SSH: Your Ed25519 key was generated automatically. Copy the public key to your GitHub account:Bashcat ~/.ssh/id_ed25519.pub
