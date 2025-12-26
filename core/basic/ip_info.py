import socket
import requests
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Fetching IP geolocation and network details for {domain}...")
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        
        city = r.get('city', 'Unknown')
        region = r.get('regionName', 'Unknown')
        country = r.get('country', 'Unknown')
        zip_code = r.get('zip', 'Unknown')
        isp = r.get('isp', 'Unknown')
        org = r.get('org', 'Unknown')
        asn = r.get('as', 'Unknown')
        timezone = r.get('timezone', 'Unknown')
        lat = r.get('lat', 'Unknown')
        lon = r.get('lon', 'Unknown')
        
        with open(f"{save_path}/ip_location.txt", "w") as f:
            f.write(f"IP Address   : {ip}\n")
            f.write(f"City         : {city}\n")
            f.write(f"Region       : {region}\n")
            f.write(f"Country      : {country}\n")
            f.write(f"Zip Code     : {zip_code}\n")
            f.write(f"Timezone     : {timezone}\n")
            f.write(f"ISP          : {isp}\n")
            f.write(f"Organization : {org}\n")
            f.write(f"ASN          : {asn}\n")
            f.write(f"Latitude     : {lat}\n")
            f.write(f"Longitude    : {lon}\n")
            
        print(Fore.GREEN + f"[+] IP Scan successful. Location: {city}, {country}")
        
    except Exception as e:
        print(Fore.RED + f"[-] IP Scan Error: {e}")
