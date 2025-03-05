#!/bin/bash

# Warna untuk tampilan lebih keren
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RESET='\033[0m'

# Lokasi Lockfile Rahasia
if [ -d "/data/data/com.termux" ]; then
    LOCKFILE="$HOME/.cache/.sys_zer0fox.lock"
else
    LOCKFILE="/var/tmp/.cache_sys_zer0fox.lock"
fi
LOCK_DURATION=300  # 5 menit

# Banner Keren
clear
echo -e "${MAGENTA}"
echo "    ██████  ███████ ██████   ██████   ██████   █████▒"
echo "    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒████  ▒ █████   ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██"
echo "    ▒██    ▒ ███████ ██████   ██████   ██████  ██████"
echo "    ======================================"
echo "    ||      0Zer0 Fox Installer        ||"
echo "    ||     Everything Can Be Hacked    ||"
echo "    ======================================"
echo -e "${RESET}"

# Cek Lockfile
if [ -f "$LOCKFILE" ]; then
    LOCK_TIME=$(cat "$LOCKFILE")
    CURRENT_TIME=$(date +%s)
    DIFF=$((CURRENT_TIME - LOCK_TIME))

    if [ $DIFF -lt $LOCK_DURATION ]; then
        REMAINING=$((LOCK_DURATION - DIFF))
        echo -e "${RED}[X] Tools sedang dikunci! Coba lagi dalam $REMAINING detik.${RESET}"
        exit 1
    else
        rm -f "$LOCKFILE"  # Hapus lock jika sudah lebih dari 5 menit
    fi
fi

# Cek sistem (Linux atau Termux)
if [ -d "/data/data/com.termux" ]; then
    OS="termux"
    PKG_MANAGER="pkg"
    echo -e "${CYAN}[+] Detected: Termux${RESET}"
else
    OS="linux"
    PKG_MANAGER="sudo apt"
    echo -e "${CYAN}[+] Detected: Kali Linux or other Debian-based OS${RESET}"
fi

install_tools() {
    echo -e "${CYAN}[+] Updating system & installing dependencies...${RESET}"
    $PKG_MANAGER update -y && $PKG_MANAGER install -y curl unzip git python python3-pip ruby

    # Pasang Lockfile Rahasia Diam-Diam
    echo $(date +%s) > "$LOCKFILE"
    chmod 600 "$LOCKFILE"

    # Install Virtualenv
    echo -e "${CYAN}[+] Installing Virtualenv...${RESET}"
    pip install virtualenv

    # Cek & install Go
    if ! command -v go &> /dev/null; then
        echo -e "${CYAN}[+] Installing Go...${RESET}"
        if [ "$OS" == "termux" ]; then
            pkg install golang -y
        else
            curl -fsSL https://golang.org/dl/go1.21.5.linux-amd64.tar.gz | sudo tar -C /usr/local -xz
            echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
            source ~/.bashrc
        fi
    else
        echo -e "${GREEN}[✔] Go already installed!${RESET}"
    fi

    # Cek & install ProjectDiscovery Tools
    declare -A tools
    tools=( ["subfinder"]="github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
            ["httpx"]="github.com/projectdiscovery/httpx/cmd/httpx@latest"
            ["nuclei"]="github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest" )

    echo -e "${CYAN}[+] Checking & Installing ProjectDiscovery Tools...${RESET}"
    for tool in "${!tools[@]}"; do
        if command -v $tool &> /dev/null; then
            echo -e "${GREEN}[✔] $tool already installed, skipping...${RESET}"
        else
            echo -e "${CYAN}[+] Installing $tool...${RESET}"
            go install -v ${tools[$tool]}
        fi
    done

    # Install additional tools
    echo -e "${CYAN}[+] Installing additional scanning tools...${RESET}"
    if [ "$OS" == "termux" ]; then
        pkg install nmap gobuster ffuf nikto -y
        gem install wpscan
    else
        sudo apt install nmap gobuster ffuf nikto wafw00f -y
        sudo gem install wpscan
    fi

    echo -e "${GREEN}[✔] Installation complete! Restart terminal atau run 'source ~/.bashrc'${RESET}"
}

uninstall_tools() {
    echo -e "${RED}[!] Uninstalling all tools...${RESET}"
    rm -rf $HOME/go/bin/subfinder
    rm -rf $HOME/go/bin/httpx
    rm -rf $HOME/go/bin/nuclei
    rm -rf $HOME/go/bin
    rm -rf $HOME/.cache
    rm -rf $HOME/.local/bin
    if [ "$OS" == "linux" ]; then
        sudo apt remove nmap gobuster ffuf nikto wafw00f -y
        sudo gem uninstall wpscan
    else
        pkg uninstall nmap gobuster ffuf nikto -y
        gem uninstall wpscan
    fi
    echo -e "${GREEN}[✔] Uninstall complete!${RESET}"
}

# Menu pilihan
echo -e "${CYAN}Pilih opsi:${RESET}"
echo -e "1. Install tools"
echo -e "2. Uninstall tools"
echo -e "3. Keluar"
read -p "Pilihan (1/2/3): " choice

case $choice in
    1) install_tools ;;
    2) uninstall_tools ;;
    3) exit 0 ;;
    *) echo -e "${RED}[X] Pilihan tidak valid!${RESET}" ;;
esac
