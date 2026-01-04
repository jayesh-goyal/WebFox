import requests
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Searching for robots.txt on {domain}...")
    
    found = False
    content = ""
    protocols = ["https", "http"]
    
    for proto in protocols:
        try:
            url = f"{proto}://{domain}/robots.txt"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200 and "User-agent" in r.text:
                print(Fore.GREEN + f"    > Found: {url}")
                content = r.text
                found = True
                break
        except:
            continue

    if found:
        with open(f"{save_path}/robots.txt", "w") as f:
            f.write(content)
        print(Fore.GREEN + f"[+] Robots.txt saved successfully.")
    else:
        print(Fore.YELLOW + f"[-] Robots.txt not found.")
