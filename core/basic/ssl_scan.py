import ssl
import socket
from datetime import datetime
from colorama import Fore

def scan(domain, save_path):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as s:
            with ctx.wrap_socket(s, server_hostname=domain) as ss:
                c = ss.getpeercert()
                
                subject = dict(x[0] for x in c['subject']).get('commonName', 'Unknown')
                issuer = dict(x[0] for x in c['issuer']).get('organizationName', 'Unknown')
                
                start_date_str = c.get('notBefore')
                end_date_str = c.get('notAfter')
                
                fmt = r'%b %d %H:%M:%S %Y %Z'
                try:
                    end_date_obj = datetime.strptime(end_date_str, fmt)
                    days_left = (end_date_obj - datetime.utcnow()).days
                except:
                    days_left = "Unknown"

                sans = []
                if 'subjectAltName' in c:
                    for item in c['subjectAltName']:
                        if item[0] == 'DNS':
                            sans.append(item[1])

                with open(f"{save_path}/ssl_info.txt", "w") as f:
                    f.write(f"SSL CERTIFICATE REPORT: {domain}\n")
                    f.write("="*40 + "\n")
                    f.write(f"Issued To    : {subject}\n")
                    f.write(f"Issued By    : {issuer}\n")
                    f.write(f"Valid From   : {start_date_str}\n")
                    f.write(f"Valid Until  : {end_date_str}\n")
                    f.write(f"Days Left    : {days_left}\n")
                    f.write(f"Serial Number: {c.get('serialNumber')}\n")
                    f.write(f"Version      : {c.get('version')}\n\n")
                    
                    f.write("SUBJECT ALTERNATIVE NAMES (SANs):\n")
                    f.write("-" * 30 + "\n")
                    for san in sans:
                        f.write(f"- {san}\n")

    except Exception as e:
        print(Fore.RED + f"[-] SSL Scan Failed: {e}")
