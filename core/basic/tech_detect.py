import builtwith
import subprocess
import re
import os
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Detecting Technologies & OS for {domain}...")
    
    tech_data = {}
    os_guess = "Unknown"

    try:
        tech_data = builtwith.parse(f"http://{domain}")
    except:
        pass

    try:
        param = '-n' if os.name == 'nt' else '-c'
        cmd = ['ping', param, '1', domain]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        
        ttl_match = re.search(r'ttl=(\d+)', out.decode('utf-8', errors='ignore'), re.IGNORECASE)
        if ttl_match:
            ttl = int(ttl_match.group(1))
            if ttl <= 64:
                os_guess = "Linux / Unix"
            elif ttl <= 128:
                os_guess = "Windows Server"
            else:
                os_guess = "Solaris / Network Device"
    except:
        pass

    if 'web-servers' in tech_data:
        headers = str(tech_data['web-servers']).lower()
        if 'iis' in headers or 'microsoft' in headers:
            os_guess = "Windows Server (Confirmed by Headers)"
        elif 'ubuntu' in headers or 'debian' in headers:
            os_guess = "Linux (Confirmed by Headers)"

    with open(f"{save_path}/technologies.txt", "w") as f:
        f.write(f"OPERATING SYSTEM: {os_guess}\n")
        f.write("="*30 + "\n")
        if not tech_data:
            f.write("No specific technologies detected.\n")
        else:
            for cat, tools in tech_data.items():
                f.write(f"{cat}: {', '.join(tools)}\n")

    print(Fore.GREEN + f"[+] Tech & OS detection successful for {domain}")
