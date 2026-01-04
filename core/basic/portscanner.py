import socket
import threading
from urllib.parse import urlparse
from colorama import Fore, init

init(autoreset=True)

def get_clean_ip(target):
    try:
        if "://" not in target:
            target = "http://" + target
        
        parsed = urlparse(target)
        hostname = parsed.netloc
        
        if ":" in hostname:
            hostname = hostname.split(":")[0]

        ip = socket.gethostbyname(hostname)
        return ip, hostname
    except:
        return None, None

def scan(domain, threads, save_path):
    target_ip, clean_hostname = get_clean_ip(domain)
    
    if not target_ip:
        print(Fore.RED + f"[-] Could not resolve domain: {domain}")
        return

    print(Fore.CYAN + f"[*] Scanning IP: {target_ip} ({clean_hostname})...")
    
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5900, 8000, 8080, 8443]
    results = []
    results_lock = threading.Lock()

    def check(p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            result = s.connect_ex((target_ip, p))
            if result == 0:
                try:
                    service = socket.getservbyport(p, 'tcp')
                except:
                    service = "Unknown"
                
                output_line = f"Port {p:<5} : OPEN ({service})"
                
                with results_lock:
                    results.append(output_line)
        except:
            pass
        finally:
            s.close()

    ts = [threading.Thread(target=check, args=(p,)) for p in ports]
    for t in ts: t.start()
    for t in ts: t.join()

    try:
        with open(f"{save_path}/ports.txt", "w") as f:
            f.write(f"Scan Results for {clean_hostname} ({target_ip})\n")
            f.write("="*40 + "\n")
            f.write("\n".join(results))
    except Exception as e:
        print(Fore.RED + f"[-] Error saving file: {e}")

    print(Fore.GREEN + f"[+] Port scan completed. Found {len(results)} open ports.")
