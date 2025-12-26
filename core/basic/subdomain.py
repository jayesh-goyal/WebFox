"""import requests
import socket
import concurrent.futures
from colorama import Fore

def enumerate(domain, save_path):
    print(Fore.CYAN + f"[*] Enumerating and checking subdomains for {domain}...")
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        data = requests.get(url, timeout=40).json()
        
        subs = set()
        for entry in data:
            name_value = entry['name_value']
            if "\n" in name_value:
                subs.update(name_value.split("\n"))
            else:
                subs.add(name_value)

        live_subs = []
        
        def check_live(sub):
            try:
                socket.gethostbyname(sub)
                return sub
            except:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_live, subs)
            for result in results:
                if result:
                    live_subs.append(result)

        with open(f"{save_path}/subdomains_all.txt", "w") as f:
            for s in subs:
                f.write(s + "\n")

        with open(f"{save_path}/subdomains_live.txt", "w") as f:
            for s in live_subs:
                f.write(s + "\n")
                
        print(Fore.GREEN + f"[+] Found {len(subs)} total subdomains ({len(live_subs)} active)")

    except:
        pass
"""




import requests
import socket
import concurrent.futures
from colorama import Fore

def enumerate(domain, save_path):
    print(Fore.CYAN + f"[*] Enumerating and checking subdomains for {domain}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        
        r = requests.get(url, headers=headers, timeout=100)
        if r.status_code != 200:
            print(Fore.RED + f"[-] crt.sh returned status {r.status_code}")
            return

        try:
            data = r.json()
        except ValueError:
            print(Fore.RED + "[-] crt.sh returned invalid JSON (Service might be down)")
            return
        
        subs = set()
        for entry in data:
            name_value = entry['name_value']
            sub_entries = name_value.split("\n")
            for sub in sub_entries:
                if "*" in sub:
                    sub = sub.replace("*.", "")
                subs.add(sub)

        live_subs = []
        
        def check_live(sub):
            try:
                socket.gethostbyname(sub)
                return sub
            except:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_live, subs)
            for result in results:
                if result:
                    live_subs.append(result)

        with open(f"{save_path}/subdomains_all.txt", "w") as f:
            for s in subs:
                f.write(s + "\n")

        with open(f"{save_path}/subdomains_live.txt", "w") as f:
            for s in live_subs:
                f.write(s + "\n")
                
        print(Fore.GREEN + f"[+] Found {len(subs)} total subdomains ({len(live_subs)} active)")

    except Exception as e:
        print(Fore.RED + f"[-] Subdomain scan error: {e}")
