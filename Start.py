import os
import getpass
import subprocess
import time
import sys
from termcolor import colored

LOCKFILE = "/var/tmp/.cache_sys_zer0fox.lock"
LOCK_DURATION = 300  # 5 menit

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
            print(colored("Login Berhasil!", "green"))
            time.sleep(2)  # Tambahin delay
            print(colored("Verification successful! Welcome home, sir", "cyan"))
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
    ======================================
    ||        0Zer0 Fox Scanner        ||
    ||     Everything Can Be Hacked    ||
    ======================================
     ______ ______ _____   ___  _____   ___  
    |  ____|  ____|  __ \ / _ \|  __ \ / _ \ 
    | |__  | |__  | |  | | | | | |  | | | | |
    |  __| |  __| | |  | | | | | |  | | | | |
    | |    | |____| |__| | |_| | |__| | |_| |
    |_|    |______|_____/ \___/|_____/ \___/ 
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
    
    # Tambahkan fungsi scan di sini

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
    scan()

if __name__ == "__main__":
    main()
