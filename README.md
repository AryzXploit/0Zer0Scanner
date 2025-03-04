# 0Zer0 Fox Scanner 🦊

**Everything Can Be Hacked**

## 🔥 Overview
0Zer0 Fox Scanner adalah alat otomatisasi reconnaissance dan scanning untuk bug bounty hunter & pentester. Tools ini bisa mencari subdomain, mengecek host yang hidup, serta scanning vulnerability dengan Nuclei.

## 🚀 Features
- **Subdomain Enumeration** dengan `subfinder -all`
- **Live Host Checking** dengan `httpx`
- **Port Scanning** dengan HTTPX (`-ports 80,443,8080,8443,...`)
- **Vulnerability Scanning** menggunakan **Nuclei**
- **Multi-Mode Scanning**: Silent, Normal, Brute
- **Fancy CLI Interface** 😎

## 🛠 Installation
Pastikan lo udah install **subfinder, httpx, nuclei**, dan **Python 3**.

```bash
git clone https://github.com/AryzXploit/Tools-Recon.git
cd Tools-Recon
pip install -r requirements.txt
```

## 💻 Usage
Jalankan tools dengan:

```bash
python3 recon.py
```

Lalu ikuti instruksi yang muncul di layar.

## 🐝 Modes
1. **Silent (Stealth Mode)** - Scan dengan request seminimal mungkin.
2. **Normal (Standard Scan)** - Scan dengan kecepatan dan request standar.
3. **Brute (Max Request)** - Scan dengan request maksimum.

## 👤 Author
Developed by **AryzXploit**

## 📚 License
[MIT License](LICENSE)

