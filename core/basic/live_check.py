import requests
from colorama import Fore

def check(domain):
    print(Fore.CYAN + f"[*] Checking connection status for {domain}...")
    try:
        r = requests.get(f"http://{domain}", timeout=15)
        print(Fore.GREEN + f"[+] {domain} is Online (Status: {r.status_code}, Latency: {r.elapsed.total_seconds()}s)")
        return True
    except:
        print(Fore.RED + f"[-] {domain} is DOWN or Unreachable.")
        return False
