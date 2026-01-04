import requests
import socket
import concurrent.futures
import re
from colorama import Fore

def enumerate(domain, save_path):
    print(Fore.CYAN + f"[*] Launching Multi-Source Subdomain Scan for {domain}...")
    
    unique_subs = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    def fetch_crtsh():
        try:
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200:
                data = r.json()
                local_subs = set()
                for entry in data:
                    name_value = entry['name_value']
                    for sub in name_value.split("\n"):
                        if "*" in sub: sub = sub.replace("*.", "")
                        local_subs.add(sub.lower())
                print(Fore.BLUE + f"    > crt.sh: Found {len(local_subs)}")
                return local_subs
        except: return set()

    def fetch_hackertarget():
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            r = requests.get(url, headers=headers, timeout=20)
            local_subs = set()
            if r.status_code == 200:
                for line in r.text.split("\n"):
                    if "," in line:
                        sub = line.split(",")[0]
                        local_subs.add(sub.lower())
            print(Fore.BLUE + f"    > HackerTarget: Found {len(local_subs)}")
            return local_subs
        except: return set()

    def fetch_alienvault():
        try:
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
            r = requests.get(url, headers=headers, timeout=20)
            local_subs = set()
            if r.status_code == 200:
                data = r.json()
                for entry in data.get('passive_dns', []):
                    sub = entry.get('hostname')
                    if sub: local_subs.add(sub.lower())
            print(Fore.BLUE + f"    > AlienVault: Found {len(local_subs)}")
            return local_subs
        except: return set()

    def fetch_rapiddns():
        try:
            url = f"https://rapiddns.io/subdomain/{domain}?full=1"
            r = requests.get(url, headers=headers, timeout=20)
            local_subs = set()
            if r.status_code == 200:
                pattern = r'<td><a target="_blank" href="http://(.*?)"'
                found = re.findall(pattern, r.text)
                for sub in found:
                    local_subs.add(sub.lower())
            print(Fore.BLUE + f"    > RapidDNS: Found {len(local_subs)}")
            return local_subs
        except: return set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(fetch_crtsh),
            executor.submit(fetch_hackertarget),
            executor.submit(fetch_alienvault),
            executor.submit(fetch_rapiddns)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result: unique_subs.update(result)
            except: pass

    final_subs = {s for s in unique_subs if domain in s}
    print(Fore.YELLOW + f"[*] Total Unique Candidates: {len(final_subs)}. Verifying active status...")

    live_subs = []
    
    def check_live(sub):
        try:
            socket.gethostbyname(sub)
            return sub
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(check_live, final_subs)
        for result in results:
            if result:
                live_subs.append(result)

    try:
        with open(f"{save_path}/subdomains_all.txt", "w") as f:
            for s in final_subs: f.write(s + "\n")

        with open(f"{save_path}/subdomains_live.txt", "w") as f:
            for s in live_subs: f.write(s + "\n")
    except Exception as e:
        print(Fore.RED + f"[-] Error saving files: {e}")
            
    print(Fore.GREEN + f"[+] Scan Complete. Found {len(final_subs)} candidates, {len(live_subs)} active.")
