import os
import getpass
import subprocess
import time
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

def login():
    check_lock()
    password = "TheOwner"
    attempts = 3

    while attempts > 0:
        user_input = getpass.getpass(colored("Masukkan Password: ", "yellow"))
        if user_input == password:
            print(colored("Login Berhasil!", "green"))
            time.sleep(5)  # Tambahin delay 5 detik
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

def subdomain_recon(domain, folder_path):
    print(colored("[+] Mencari subdomain...", "cyan"))
    run_command(f"subfinder -d {domain} -o {folder_path}/subdomains.txt")
    run_command(f"assetfinder --subs-only {domain} >> {folder_path}/subdomains.txt")

def web_recon(domain, folder_path):
    print(colored("[+] Mengecek informasi domain...", "cyan"))
    run_command(f"cat {folder_path}/subdomains.txt | httpx -td -title -sc -ip -o {folder_path}/info.txt")
    print(colored("[+] Crawling website...", "cyan"))
    run_command(f"katana -u https://{domain} -d 2 -o {folder_path}/crawl.txt")

def port_scan(domain, folder_path):
    print(colored("[+] Melakukan port scanning...", "cyan"))
    run_command(f"nmap -p- {domain} -oN {folder_path}/nmap_scan.txt")

def fuzzing_brute(domain, folder_path):
    print(colored("[+] Menjalankan FFUF untuk directory fuzzing...", "cyan"))
    run_command(f"ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u https://{domain}/FUZZ -o {folder_path}/ffuf_result.txt")
    print(colored("[+] Menjalankan Dirsearch...", "cyan"))
    run_command(f"dirsearch -u https://{domain} -e php,html,js -o {folder_path}/dirsearch_result.txt")

def vuln_scan(domain, folder_path):
    print(colored("[+] Menjalankan Nuclei...", "cyan"))
    run_command(f"nuclei -l {folder_path}/subdomains.txt -t nuclei-templates -o {folder_path}/nuclei_result.txt")
    print(colored("[+] Menjalankan SQLmap...", "cyan"))
    run_command(f"sqlmap -u https://{domain} --batch --dbs > {folder_path}/sqlmap_result.txt")
    print(colored("[+] Menjalankan Arjun (parameter fuzzing)...", "cyan"))
    run_command(f"arjun -u https://{domain} -o {folder_path}/arjun_result.txt")

def wpscan(domain, folder_path):
    print(colored("[+] Menjalankan WPScan untuk WordPress vulnerability scanning...", "cyan"))
    with open("wp-api.txt", "r") as f:
        api_key = f.read().strip()
    enum_options = input(colored("Masukkan opsi enumerate (contoh: u,vt,vp atau all): ", "yellow"))
    if enum_options.lower() == "all":
        enum_options = "u,vt,vp,tt,cb,ap"  # Semua opsi WPScan
    run_command(f"wpscan --url https://{domain} --api-token {api_key} --enumerate {enum_options} -o {folder_path}/wpscan_result.txt")

def waf_scan(domain, folder_path):
    print(colored("[+] Menjalankan WAF Scanner...", "cyan"))
    run_command(f"whatweb {domain} > {folder_path}/whatweb_result.txt")
    run_command(f"wafw00f -a {domain} > {folder_path}/wafw00f_result.txt")

def scan():
    clear_screen()
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
        subdomain_recon(domain, folder_path)
    elif choice == "2":
        web_recon(domain, folder_path)
    elif choice == "3":
        port_scan(domain, folder_path)
    elif choice == "4":
        fuzzing_brute(domain, folder_path)
    elif choice == "5":
        vuln_scan(domain, folder_path)
    elif choice == "6":
        wpscan(domain, folder_path)
    elif choice == "7":
        waf_scan(domain, folder_path)
    elif choice == "8":
        subdomain_recon(domain, folder_path)
        web_recon(domain, folder_path)
        port_scan(domain, folder_path)
        fuzzing_brute(domain, folder_path)
        vuln_scan(domain, folder_path)
        wpscan(domain, folder_path)
        waf_scan(domain, folder_path)
    else:
        print(colored("Pilihan tidak valid!", "red"))
    
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
