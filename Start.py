import os
import getpass
import subprocess
from termcolor import colored

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    password = "TheOwner"
    while True:
        user_input = getpass.getpass(colored("Masukkan Password: ", "yellow"))
        if user_input == password:
            print(colored("Login Berhasil!", "green"))
            break
        else:
            print(colored("Password salah, coba lagi!", "red"))

    clear_screen()

def scan(mode, output_file):
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

    print(colored("[+] Mencari subdomain...", "cyan"))
    subprocess.run(["subfinder", "-d", domain, "-all", "-o", "subdomains.txt"])

    print(colored("[+] Mengecek informasi domain...", "cyan"))
    subprocess.run(["cat", "subdomains.txt", "|", "httpx", "-td", "-title", "-sc", "-ip", "-o", f"info-{domain}.txt"], shell=True)

    print(colored("[+] Mengecek live host dengan port scanning...", "cyan"))
    subprocess.run(["httpx", "-ports", "80,443,8080,8443,8000,8888,8081,8181,3306,5432,6379,27017,15672,10000,9090,5900", "-threads", "80", "-o", f"alive-{domain}.txt"])

    print(colored("[+] Menjalankan Nuclei untuk scanning vulnerability...", "cyan"))
    subprocess.run(["nuclei", "-l", f"alive-{domain}.txt", "-t", "nuclei-templates-alt", "-o", output_file])

    print(colored(f"[+] Scan selesai! Hasil disimpan di {output_file}", "green"))

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

    output_file = input(colored("Masukkan nama output file (contoh: hasil_scan.txt): ", "yellow"))

    scan(mode, output_file)

if __name__ == "__main__":
    main()
