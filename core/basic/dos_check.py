import socket
from colorama import Fore
def scan(domain, save_path):
    print(Fore.YELLOW + "[*] Checking DoS Vulnerability...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((domain, 80))
        s.send(f"GET / HTTP/1.1\r\nHost: {domain}\r\n".encode('utf-8'))
        try:
            s.recv(1024)
            res = "Secure"
        except socket.timeout:
            res = "VULNERABLE FOR DOS/DDOS ATTACK!"
            print(Fore.RED + f"    [!] {res}")
        s.close()
        with open(f"{save_path}/dos_vuln.txt", "w") as f: f.write(res)
    except: pass
