import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from colorama import Fore

def capture(domain, save_path):
    print(Fore.CYAN + f"[*] Capturing high-value targets (Max 5)...")
    
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        if os.path.exists("/usr/bin/firefox-esr"):
            options.binary_location = "/usr/bin/firefox-esr"
        elif os.path.exists("/usr/bin/firefox"):
            options.binary_location = "/usr/bin/firefox"

        service_path = None
        possible_paths = ["/usr/bin/geckodriver", "/usr/local/bin/geckodriver", "./geckodriver"]
        for p in possible_paths:
            if os.path.exists(p):
                service_path = p
                break
        
        if service_path:
            service = Service(service_path)
            driver = webdriver.Firefox(options=options, service=service)
        else:
            driver = webdriver.Firefox(options=options)

        driver.set_page_load_timeout(30)

        base_url = f"http://{domain}"
        candidates = set()
        candidates.add(base_url)

        try:
            r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
            if r.status_code == 200:
                for entry in r.json()[:30]: 
                    sub = entry['name_value'].split('\n')[0]
                    if not "*" in sub:
                        candidates.add(f"http://{sub}")
        except: pass

        try:
            html = requests.get(base_url, timeout=5).text
            links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
            for l in links:
                if domain in l:
                    candidates.add(l)
        except: pass

        scored_urls = []
        
        keywords = {
            "login": 50, "signin": 50, "sign-in": 50, "portal": 50,
            "register": 45, "signup": 45, "join": 45, 
            "contact": 40, "support": 40, 
            "about": 35, "company": 35, "team": 35,
            "admin": 30
        }

        base_clean = base_url.rstrip("/")

        for url in candidates:
            score = 0
            url_lower = url.lower()
            
            if url.rstrip("/") == base_clean:
                score = 100
            else:
                for word, points in keywords.items():
                    if word in url_lower:
                        score = points
                        break
            
            if score > 0:
                scored_urls.append((score, url))

        scored_urls.sort(key=lambda x: x[0], reverse=True)
        final_targets = [x[1] for x in scored_urls[:5]]

        print(Fore.BLUE + f"    > Scanned {len(candidates)} links. Found {len(final_targets)} important targets.")

        for i, url in enumerate(final_targets):
            try:
                driver.get(url)
                time.sleep(2)
                
                if url.rstrip("/") == base_clean:
                    name = "Homepage"
                else:
                    name = "Unknown"
                    for k in keywords:
                        if k in url.lower():
                            name = k.capitalize()
                            break
                    if name == "Unknown": name = f"Target_{i+1}"

                filename = f"{save_path}/Evidence_{i+1}_{name}.png"
                
                driver.save_screenshot(filename)
                print(Fore.GREEN + f"    > [{i+1}/{len(final_targets)}] Captured: {name} ({url})")
            except:
                pass

        print(Fore.GREEN + f"[+] Visual surveillance completed.")

    except Exception as e:
        print(Fore.RED + f"[-] Screenshot error: {e}")

    finally:
        if driver:
            driver.quit()
