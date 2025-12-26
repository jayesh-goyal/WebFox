import ssl
import socket
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Analyzing SSL certificate for {domain}...")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as s:
            with ctx.wrap_socket(s, server_hostname=domain) as ss:
                c = ss.getpeercert()
                
                issuer = dict(x[0] for x in c['issuer']).get('organizationName', 'Unknown')
                subject = dict(x[0] for x in c['subject']).get('commonName', 'Unknown')
                
                issued_on = c.get('notBefore')
                expires_on = c.get('notAfter')
                
                with open(f"{save_path}/ssl_info.txt", "w") as f:
                    f.write(f"Issued To    : {subject}\n")
                    f.write(f"Issued By    : {issuer}\n")
                    f.write(f"Issued Date: {issued_on}\n")
                    f.write(f"Expiry Date  : {expires_on}\n")
                    f.write(f"Serial Number: {c.get('serialNumber')}\n")
                    f.write(f"Version      : {c.get('version')}\n")

        print(Fore.GREEN + f"[+] SSL scan successful for {domain}")
    except:
        pass
