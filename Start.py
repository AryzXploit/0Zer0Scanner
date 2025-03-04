import hashlib
import os
import sys
from colorama import Fore, Style, init

# Inisialisasi Colorama
init(autoreset=True)

# Hardcoded password (SHA-256 hash dari "admin123")
PASSWORD_HASH = "ef92b778bafe771e89245b89ecbc1927c5b5b82e1e4a5d14282f3e5a0e3a448a"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    print(Fore.CYAN + "[0Zer0 Fox] Login Required")
    password = input(Fore.YELLOW + "Enter Password: ")
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    if hashed_input == PASSWORD_HASH:
        print(Fore.GREEN + "Login successful!\n")
        clear_screen()
    else:
        print(Fore.RED + "Wrong password!")
        sys.exit()

def banner():
    print(Fore.MAGENTA + """
    ██████  ███████ ██████   ██████   ██████   █████▒
    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██
    ▒████  ▒ █████   ██   ██ ██    ██ ██    ██ ██   ██
    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██
    ▒██    ▒ ███████ ██████   ██████   ██████  ██████
    """ + Style.RESET_ALL)
    print(Fore.CYAN + "[ Vulnerability Scanner ]\n")

def main():
    login()
    banner()
    print(Fore.YELLOW + "[+] Masukkan domain target: ", end="")
    target = input()
    print(Fore.GREEN + f"[+] Scanning {target}...")
    # Placeholder untuk fitur scanning nanti
    print(Fore.RED + "[!] Fitur scanning belum ditambahkan!")

if __name__ == "__main__":
    main()
