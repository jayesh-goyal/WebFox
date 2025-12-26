import requests
import re
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Parsing JavaScript files for hidden endpoints on {domain}...")
    try:
        url = f"http://{domain}"
        text = requests.get(url, timeout=15).text
        js_files = re.findall(r'src=["\'](.*?\.js)["\']', text)
        unique_js = list(set(js_files))
        
        print(Fore.BLUE + f"    > Found {len(unique_js)} unique JS files. Starting deep scan...")
        
        found_urls = set()
        
        for js in unique_js:
            if js.startswith("//"):
                js_url = "http:" + js
            elif js.startswith("/"):
                js_url = f"{url}{js}"
            elif not js.startswith("http"):
                js_url = f"{url}/{js}"
            else:
                js_url = js
            
            try:
                js_name = js_url.split('/')[-1][:40]
                print(Fore.BLUE + f"    > Scanning: {js_name}")
                
                content = requests.get(js_url, timeout=10).text
                
                links = re.findall(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s"\'<>]*', content)
                for l in links:
                    found_urls.add(l)
            except:
                pass
            
        with open(f"{save_path}/js_urls.txt", "w") as f:
            for link in found_urls:
                f.write(link + "\n")
            
        print(Fore.GREEN + f"[+] JS Scan successful. Extracted {len(found_urls)} unique URLs.")

    except Exception as e:
        print(Fore.RED + f"[-] JS Scan failed: {e}")
