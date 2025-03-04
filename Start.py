import os
import getpass
import subprocess
import time
from termcolor import colored

# Lokasi Lockfile Rahasia
if "com.termux" in os.getcwd():
    LOCKFILE = os.path.expanduser("~/.cache/.sys_zer0fox.lock")
else:
    LOCKFILE = "/var/tmp/.cache_sys_zer0fox.lock"
LOCK_DURATION = 300  # 5 menit

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Cek lockfile sebelum login
def check_lock():
    if os.path.exists(LOCKFILE):
        with open(LOCKFILE, "r") as f:
            lock_time = int(f.read().strip())
        current_time = int(time.time())

        if current_time - lock_time < LOCK_DURATION:
            remaining = LOCK_DURATION - (current_time - lock_time)
            print(colored(f"[X] Tools terkunci! Tunggu {remaining} detik.", "red"))
            exit(1)
        else:
            os.remove(LOCKFILE)  # Hapus lock setelah 5 menit

# Fungsi login
def login():
    check_lock()
    password = "TheOwner"
    attempts = 3

    while attempts > 0:
        user_input = getpass.getpass(colored("Masukkan Password: ", "yellow"))
        if user_input == password:
            print(colored("Login Berhasil!", "green"))
            break
        else:
            attempts -= 1
            print(colored(f"Password salah! Kesempatan tersisa: {attempts}", "red"))
            if attempts == 0:
                print(colored("Terlalu banyak percobaan! Tools terkunci 5 menit!", "red"))
                with open(LOCKFILE, "w") as f:
                    f.write(str(int(time.time())))
                exit(1)
    clear_screen()

# Fungsi scanning
def scan(mode):
    clear_screen()
    print(colored("""
    ██████  ███████ ██████   ██████   ██████   █████▒
    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██
    ▒████  ▒ █████   ██   ██ ██    ██ ██    ██ ██   ██
    ▒██    ▒ ██      ██   ██ ██    ██ ██    ██ ██   ██
    ▒██    ▒ ███████ ██████   ██████   ██████  ██████
    =====================================
    ||        0Zer0 Fox Scanner        ||
    ||     Everything Can Be Hacked    ||
    =====================================
    """, "magenta"))

    print(colored(f"Scanning mode: {mode}", "blue"))
    domain = input(colored("Masukkan Domain Target: ", "yellow"))
    folder_path = os.path.join(os.getcwd(), domain)
    os.makedirs(folder_path, exist_ok=True)

    print(colored("[+] Mencari subdomain...", "cyan"))
    subprocess.run(["subfinder", "-d", domain, "-all", "-o", os.path.join(folder_path, "subdomains.txt")])

    print(colored("[+] Mengecek informasi domain...", "cyan"))
    subprocess.run(f"cat {folder_path}/subdomains.txt | httpx -td -title -sc -ip -o {folder_path}/info.txt", shell=True)

    print(colored("[+] Mengecek live host dengan port scanning...", "cyan"))
    subprocess.run(["httpx", "-ports", "80,443,8080,8443,8000,8888,8081,8181,3306,5432,6379,27017,15672,10000,9090,5900", "-threads", "80", "-o", os.path.join(folder_path, "alive.txt")])

    print(colored("[+] Menjalankan Nuclei untuk scanning vulnerability...", "cyan"))
    subprocess.run(["nuclei", "-l", os.path.join(folder_path, "alive.txt"), "-t", "nuclei-templates-alt", "-o", os.path.join(folder_path, "nuclei-result.txt")])

    print(colored(f"[+] Scan selesai! Hasil disimpan di {folder_path}", "green"))

# Menu utama
def main():
    clear_screen()
    print(colored("""
    ======================================
    ||        0Zer0 Fox Scanner        ||
    ||     Everything Can Be Hacked    ||
    ======================================
    """, "magenta"))

    login()

    print(colored("Pilih mode scanning:", "yellow"))
    print(colored("1. Silent (Stealth Mode)", "cyan"))
    print(colored("2. Normal (Standar Scan)", "cyan"))
    print(colored("3. Brute (Max Request)", "cyan"))

    mode_choice = input(colored("Pilih mode (1/2/3): ", "yellow"))
    mode_dict = {"1": "silent", "2": "normal", "3": "brute"}
    mode = mode_dict.get(mode_choice, "normal")

    scan(mode)

if __name__ == "__main__":
    main()
