import requests
import re
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Parsing JavaScript files for hidden endpoints & secrets on {domain}...")
    try:
        url = f"http://{domain}"
        text = requests.get(url, timeout=15).text
        js_files = re.findall(r'src=["\'](.*?\.js)["\']', text)
        unique_js = list(set(js_files))
        
        print(Fore.BLUE + f"    > Found {len(unique_js)} unique JS files. Starting deep scan...")
        
        found_urls = set()
        found_secrets = set()

        secret_patterns = {
            "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "Stripe Key": r"pk_live_[0-9a-zA-Z]{24}",
            "Facebook Token": r"EAACEdEose0cBA[0-9A-Za-z]+",
            "Mailchimp API": r"[0-9a-f]{32}-us[0-9]{1,2}",
            "Generic Secret": r"(?:api_key|apikey|secret|token|password)\s*[:=]\s*['\"]([a-zA-Z0-9-_]{20,})['\"]"
        }
        
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
                content = requests.get(js_url, timeout=10).text
                
                links = re.findall(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s"\'<>]*', content)
                for l in links:
                    found_urls.add(l)

                for name, pattern in secret_patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if isinstance(match, tuple): match = match[0]
                        secret_info = f"TYPE: {name} | KEY: {match} | SOURCE: {js_name}"
                        found_secrets.add(secret_info)
                        print(Fore.RED + f"    > [!] SENSITIVE DATA: {secret_info}")

            except:
                pass
            
        with open(f"{save_path}/js_analysis.txt", "w") as f:
            f.write(f"JAVASCRIPT ANALYSIS FOR {domain}\n")
            f.write("="*50 + "\n\n")
            
            f.write("[!] DETECTED SECRETS\n")
            f.write("-" * 20 + "\n")
            if found_secrets:
                for s in found_secrets: f.write(s + "\n")
            else:
                f.write("No explicit secrets found.\n")
            
            f.write("\n[+] EXTRACTED URLS\n")
            f.write("-" * 20 + "\n")
            for link in found_urls:
                f.write(link + "\n")

        print(Fore.GREEN + f"[+] JS Analysis Done. Saved to js_analysis.txt")

    except Exception as e:
        print(Fore.RED + f"[-] JS Scan failed: {e}")
