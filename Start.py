import os
import getpass
import subprocess
import time
import sys
import random
from termcolor import colored

LOCKFILE = "/var/tmp/.cache_sys_zer0fox.lock"
LOCK_DURATION = 300  # 5 menit

QUOTES = [
    "Hidup kena select, kiri dengki, kanan lawan, belakang tikam, depan berlakon.",
    "Cybersecurity bukan hanya skill, tapi juga mindset.",
    "Informasi adalah senjata. Gunakan dengan bijak.",
    "Kamu tidak bisa mengamankan sesuatu yang tidak kamu mengerti.",
    "Setiap sistem punya celah, tugas kita menemukannya sebelum orang lain.",
    "0Zer0Scanner – Only the best survives in the game.",
    "Think like a hacker, act like a professional."
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            os.remove(LOCKFILE)  

def animate_verification():
    sys.stdout.write(colored("Verifying password", "cyan"))
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(1)
        sys.stdout.write(colored(".", "cyan"))
        sys.stdout.flush()
    print(colored(" Done!", "green"))
    time.sleep(1)

def login():
    check_lock()
    password = "TheOwner"
    attempts = 3

    while attempts > 0:
        user_input = getpass.getpass(colored("Masukkan Password: ", "yellow"))
        if user_input == password:
            animate_verification()
            time.sleep(5)  # Delay 5 detik setelah verifikasi
            print(colored("Verification successful! Welcome home, sir", "cyan"))
            time.sleep(2)  # Tambahin delay sebelum clear_screen()
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

def run_command(command):
    subprocess.run(command, shell=True)

def scan():
    clear_screen()
    print(colored("""
   _______                       _______ __________                            
\   _  \ ________ ___________ \   _  \\______   \ ____   ____  ____   ____  
/  /_\  \\___   // __ \_  __ \/  /_\  \|       _// __ \_/ ___\/  _ \ /    \ 
\  \_/   \/    /\  ___/|  | \/\  \_/   \    |   \  ___/\  \__(  <_> )   |  \
 \_____  /_____ \\___  >__|    \_____  /____|_  /\___  >\___  >____/|___|  /
       \/      \/    \/              \/       \/     \/     \/           \/ 
    
    WARNING: This tool is intended for educational purposes only.
    Unauthorized use for hacking or illegal activities is strictly prohibited.
    The developer is not responsible for any misuse of this tool.
    Use this tool responsibly and ethically.
    """, "cyan"))
    
    domain = input(colored("Masukkan Domain Target: ", "yellow"))
    folder_path = os.path.join(os.getcwd(), domain)
    os.makedirs(folder_path, exist_ok=True)

    print(colored("Pilih jenis scanning:", "yellow"))
    print(colored("1. Subdomain Recon", "cyan"))
    print(colored("2. Web Recon & Crawling", "cyan"))
    print(colored("3. Port Scanning", "cyan"))
    print(colored("4. Fuzzing & Bruteforce", "cyan"))
    print(colored("5. Vulnerability Scanning", "cyan"))
    print(colored("6. WordPress Scan (WPScan)", "cyan"))
    print(colored("7. WAF Detection", "cyan"))
    print(colored("8. Full Scan (Semua Mode)", "cyan"))

    choice = input(colored("Pilih mode (1-8): ", "yellow"))
    
    if choice == "1":
        run_command(f"subfinder -d {domain} -o {folder_path}/subdomains.txt")
    elif choice == "2":
        run_command(f"gobuster dir -u {domain} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {folder_path}/web_recon.txt")
    elif choice == "3":
        run_command(f"nmap -sV -oN {folder_path}/port_scan.txt {domain}")
    elif choice == "4":
        run_command(f"ffuf -u http://{domain}/FUZZ -w /usr/share/wordlists/rockyou.txt -o {folder_path}/fuzzing.txt")
    elif choice == "5":
        run_command(f"nikto -h {domain} -o {folder_path}/vulnerability_scan.txt")
    elif choice == "6":
        run_command(f"wpscan --url {domain} --enumerate vp -o {folder_path}/wordpress_scan.txt")
    elif choice == "7":
        run_command(f"wafw00f {domain} -o {folder_path}/waf_detection.txt")
    elif choice == "8":
        run_command(f"subfinder -d {domain} -o {folder_path}/subdomains.txt")
        run_command(f"gobuster dir -u {domain} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {folder_path}/web_recon.txt")
        run_command(f"nmap -sV -oN {folder_path}/port_scan.txt {domain}")
        run_command(f"ffuf -u http://{domain}/FUZZ -w /usr/share/wordlists/rockyou.txt -o {folder_path}/fuzzing.txt")
        run_command(f"nikto -h {domain} -o {folder_path}/vulnerability_scan.txt")
        run_command(f"wpscan --url {domain} --enumerate vp -o {folder_path}/wordpress_scan.txt")
        run_command(f"wafw00f {domain} -o {folder_path}/waf_detection.txt")
    else:
        print(colored("[!] Mode belum tersedia!", "red"))

    print(colored(f"[+] Scan selesai! Hasil disimpan di {folder_path}", "green"))

def main():
    clear_screen()
    print(colored("""
    ======================================
    ||       0Zer0Scanner Login Page   ||
    ======================================
    ||        0Zer0 Fox Scanner        ||
    ||     Everything Can Be Hacked    ||
    ======================================
    """, "magenta"))
    print(colored(f'"{random.choice(QUOTES)}"', "cyan"))
    time.sleep(2)
    login()
    scan()

if __name__ == "__main__":
    main()
