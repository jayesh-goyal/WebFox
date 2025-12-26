import requests
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Searching for sitemap configuration on {domain}...")
    
    common_names = [
        "sitemap.xml", 
        "sitemap_index.xml", 
        "wp-sitemap.xml", 
        "sitemap.txt", 
        "sitemap.php"
    ]
    
    found = False
    
    for name in common_names:
        try:
            url = f"http://{domain}/{name}"
            r = requests.get(url, timeout=10)
            
            if r.status_code != 200:
                url = f"https://{domain}/{name}"
                r = requests.get(url, timeout=10)

            if r.status_code == 200 and len(r.content) > 0:
                print(Fore.GREEN + f"    > Found: {url}")
                
                with open(f"{save_path}/{name}", "w", encoding="utf-8") as f:
                    f.write(r.text)
                
                found = True
                break 
        except:
            continue

    if found:
        print(Fore.GREEN + f"[+] Sitemap detected and saved successfully.")
    else:
        print(Fore.YELLOW + f"[-] No standard sitemap found.")
