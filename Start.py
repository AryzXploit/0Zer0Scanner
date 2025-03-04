import os
import getpass
import subprocess
import time
from termcolor import colored

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
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
                print(colored("Terlalu banyak percobaan! Tunggu 5 menit sebelum mencoba lagi.", "red"))
                time.sleep(300)  # Blokir 5 menit
                attempts = 3
    clear_screen()

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
