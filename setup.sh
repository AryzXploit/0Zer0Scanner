#!/bin/bash

# Warna buat tampilan lebih keren
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RESET='\033[0m'

# Banner keren
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
    $PKG_MANAGER update && $PKG_MANAGER install -y curl unzip git

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
        echo -e "${GREEN}[+] Go already installed!${RESET}"
    fi

    # Install ProjectDiscovery Tools
    echo -e "${CYAN}[+] Installing ProjectDiscovery Tools...${RESET}"
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

    echo -e "${GREEN}[✔] Installation complete! Restart terminal or run 'source ~/.bashrc'${RESET}"
}

uninstall_tools() {
    echo -e "${RED}[!] Uninstalling ProjectDiscovery tools...${RESET}"
    rm -rf $HOME/go/bin/subfinder
    rm -rf $HOME/go/bin/httpx
    rm -rf $HOME/go/bin/nuclei
    echo -e "${GREEN}[✔] Uninstall complete!${RESET}"
}

# Menu pilihan
echo -e "${YELLOW}Pilih opsi:${RESET}"
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
