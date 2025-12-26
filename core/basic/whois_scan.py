import whois
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Fetching domain information for {domain}...")
    try:
        w = whois.whois(domain)

        with open(f"{save_path}/whois_basic.txt", "w") as f:
            f.write(f"Organization : {w.org}\n")
            f.write(f"City         : {w.city}\n")
            f.write(f"Country      : {w.country}\n")
            f.write(f"Registrar    : {w.registrar}\n")
            f.write(f"Creation Date: {w.creation_date}\n")
            f.write(f"Expiry Date  : {w.expiration_date}\n")
            f.write(f"Updated Date : {w.updated_date}\n")
            f.write(f"Name Servers : {w.name_servers}\n")
            f.write(f"Emails       : {w.emails}\n")

        print(Fore.GREEN + f"[+] Whois scan successful for {domain}")
    except:
        pass
