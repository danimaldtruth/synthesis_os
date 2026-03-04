# Synthesis OS 

> **A hyper-optimized, automated Arch Linux forge for the ThinkPad T14 Gen 2.**

Synthesis OS is not just a distribution; it is a **Technical Manifesto** expressed through code. It bridges the gap between the polished user experience of macOS/ChromeOS and the uncompromising power of an Ethical Hacking & AI Development workstation.



## 🛠 Core Architecture

- **Base:** Arch Linux (EndeavourOS-accelerated mirror logic)
- **Desktop:** KDE Plasma 6 + WhiteSur Global Theme + Polonium Dynamic Tiling
- **Kernel:** Zen-tuned for low-latency audio and high-performance virtualization
- **Shell:** Zsh + Starship Prompt + Custom Workspace Scaffolding
- **Hardware Target:** Lenovo ThinkPad T14 Gen 2 (Intel/AMD)

## 🧠 Integrated Capabilities

### 1. Hybrid AI Engine
Synthesis OS treats AI as a local utility. It ships with a pre-configured **Ollama** backend running **Phi-3** (Small Language Model) for offline intelligence, integrated into a unified desktop UI (**Chatbox**) that connects via API to Gemini, ChatGPT, and Grok.

### 2. Cybersecurity & Privacy
- **Network Isolation:** Hardened UFW firewall and Mullvad VPN daemon integration.
- **Anonymity:** Built-in Tor relay (Nyx) and native support for Whonix VMs via QEMU/KVM.
- **Tooling:** Docker-first workflow with Lazydocker, BurpSuite, and Wireshark.

### 3. Pro-Audio & Creative Suite
Configured for **PipeWire** (PulseAudio/JACK/ALSA) with zero-latency overhead. Includes a flagship native VST stack (LSP, Calf, Surge XT, Vital) and **Yabridge** for seamless Windows VST translation.

## 🚀 Deployment

Synthesis OS is "Infrastructure as Code." It is deployed via a single-file Python installer that handles disk partitioning, hardware-specific driver injection (Intel/AMD/NVIDIA), and Google Account cloud mounting.

### One-Line Install (Live USB)
```bash
curl -L [https://raw.githubusercontent.com/your-username/synthesis-os/main/synthesis_install.py](https://raw.githubusercontent.com/your-username/synthesis-os/main/synthesis_install.py) -o synthesis.py && python synthesis.py