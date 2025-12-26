import dns.resolver
from colorama import Fore

def scan(domain, save_path):
    print(Fore.CYAN + f"[*] Dumping DNS Zone records for {domain}...")
    
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    
    try:
        with open(f"{save_path}/dns.txt", "w") as f:
            f.write(f"DNS RECORDS: {domain}\n")
            f.write("="*40 + "\n")
            
            for r_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, r_type)
                    for rdata in answers:
                        line = f"{r_type:<5}: {rdata.to_text()}"
                        print(Fore.GREEN + f"    > {line}")
                        f.write(line + "\n")
                except:
                    pass

        print(Fore.GREEN + f"[+] DNS enumeration successful.")
        
    except Exception as e:
        print(Fore.RED + f"[-] DNS Scan Error: {e}")
