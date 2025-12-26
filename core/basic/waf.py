import requests
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Detecting Firewall configuration for {domain}...")
    
    sigs = {
        "Cloudflare": "cf-ray",
        "Akamai": "akamai",
        "AWS WAF": "awselb",
        "Imperva": "incap-ses",
        "F5 BigIP": "bigip",
        "Google Cloud Armor": "google-cloud-armor",
        "Citrix NetScaler": "ns-server",
        "Sucuri": "sucuri",
        "ModSecurity": "mod_security",
        "Barracuda": "barra",
        "Fortinet": "fortigate",
        "SonicWall": "sonicwall",
        "Palo Alto": "pan-os",
        "Sophos": "sophos",
        "ArvanCloud": "arvancloud",
        "StackPath": "stackpath"
    }

    generic_keywords = ["firewall", "waf", "shield", "security", "protection", "filter"]

    try:
        url = f"http://{domain}"
        try:
            r = requests.get(url, timeout=30)
        except:
            url = f"https://{domain}"
            r = requests.get(url, timeout=30)

        headers = str(r.headers).lower()
        cookies = str(r.cookies.get_dict()).lower()
        
        detected = []

        for name, key in sigs.items():
            if key in headers or key in cookies:
                detected.append(name)

        if not detected:
            for keyword in generic_keywords:
                if keyword in headers:
                    detected.append(f"Generic/Unknown ({keyword})")
                    break

        res = ", ".join(list(set(detected))) if detected else "None Detected"

        with open(f"{save_path}/waf.txt", "w") as f:
            f.write(f"Target: {domain}\n")
            f.write(f"WAF Status: {res}\n")
            f.write(f"Raw Headers: {r.headers}\n")
        
        print(Fore.GREEN + f"[+] Firewall scan successful for {domain}")

    except:
        pass
