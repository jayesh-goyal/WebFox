import socket
from colorama import Fore

def scan(domain, save_path):
    print(Fore.YELLOW + "[*] Checking DoS/Slowloris Resistance...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((domain, 80))
        
        payload = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
        
        s.send(payload.encode('utf-8'))
        
        try:
            s.recv(1024)
            res = "Secure (Server is responsive)"
            print(Fore.GREEN + f"    > {res}")
        except socket.timeout:
            res = "VULNERABLE (Server unresponsive/Slow)"
            print(Fore.RED + f"    [!] {res}")
            
        s.close()
        
        with open(f"{save_path}/dos_vuln.txt", "w") as f: 
            f.write(res)
            
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")
