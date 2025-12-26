"""import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from colorama import Fore

def capture(domain, save_path):
    print(Fore.CYAN + f"[*]  Capturing snapshots from target...")
    
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
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

        candidates = set()
        base_url = f"http://{domain}"
        candidates.add(base_url)

        try:
            r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
            if r.status_code == 200:
                for entry in r.json()[:50]: 
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
            "admin": 50, "login": 40, "dashboard": 30, 
            "portal": 30, "vpn": 25, "conf": 20, 
            "panel": 20, "account": 15, "upload": 10
        }

        for url in candidates:
            score = 1 
            for word, points in keywords.items():
                if word in url.lower():
                    score += points
            scored_urls.append((score, url))

        scored_urls.sort(key=lambda x: x[0], reverse=True)
        top_targets = [x[1] for x in scored_urls[:5]]

        print(Fore.BLUE + f"    > Identified {len(candidates)} pages. Selecting Top {len(top_targets)} important ones.")

        for i, url in enumerate(top_targets):
            try:
                driver.get(url)
                time.sleep(2)
                
                clean_name = url.replace("http://","").replace("https://","").replace("/","_").replace(":","")[:40]
                filename = f"{save_path}/priority_{i+1}_{clean_name}.png"
                
                driver.save_screenshot(filename)
                print(Fore.GREEN + f"    > [{i+1}/5] Captured: {clean_name}.png")
            except:
                pass

        print(Fore.GREEN + f"[+] Snapshot Captured Successfully.")

    except Exception as e:
        print(Fore.RED + f"[-] Screenshot module error: {e}")

    finally:
        if driver:
            driver.quit()"""
            






import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from colorama import Fore

def capture(domain, save_path):
    print(Fore.CYAN + f"[*] Capturing key targets (Home, Login, Contact, About)...")
    
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
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

        candidates = set()
        base_url = f"http://{domain}"
        candidates.add(base_url)

        try:
            r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
            if r.status_code == 200:
                for entry in r.json()[:50]: 
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
        
        # Updated Priority Dictionary based on your request
        keywords = {
            "login": 50, "signin": 50, "sign-in": 50, "auth": 50,      # Login
            "register": 50, "signup": 50, "join": 50,                  # Registration
            "contact": 40, "support": 40, "feedback": 40,              # Contact
            "about": 35, "team": 35, "company": 35, "mission": 35,     # About Us
            "index": 30, "home": 30, "main": 30                        # Explicit Home
        }

        base_clean = base_url.rstrip("/")

        for url in candidates:
            score = 1 
            url_lower = url.lower()
            
            # Critical: Always prioritize the Main Homepage highest
            if url.rstrip("/") == base_clean:
                score = 100 
            else:
                for word, points in keywords.items():
                    if word in url_lower:
                        score += points
            
            scored_urls.append((score, url))

        scored_urls.sort(key=lambda x: x[0], reverse=True)
        top_targets = [x[1] for x in scored_urls[:5]]

        print(Fore.BLUE + f"    > Identified {len(candidates)} pages. Selecting Top {len(top_targets)} based on priority.")

        for i, url in enumerate(top_targets):
            try:
                driver.get(url)
                time.sleep(2)
                
                clean_name = url.replace("http://","").replace("https://","").replace("/","_").replace(":","")[:40]
                if "priority_1_" in f"priority_{i+1}":
                     clean_name = "Homepage_Index" 

                filename = f"{save_path}/priority_{i+1}_{clean_name}.png"
                
                driver.save_screenshot(filename)
                print(Fore.GREEN + f"    > [{i+1}/5] Captured: {clean_name}.png")
            except:
                pass

        print(Fore.GREEN + f"[+] Snapshot Captured Successfully.")

    except Exception as e:
        print(Fore.RED + f"[-] Screenshot module error: {e}")

    finally:
        if driver:
            driver.quit()
