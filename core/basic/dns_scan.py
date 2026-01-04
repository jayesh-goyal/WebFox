import dns.resolver
from colorama import Fore

def scan(domain, save_path):
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
                        f.write(line + "\n")
                except:
                    pass
            
            f.write("\nEMAIL SECURITY CONFIGURATION:\n")
            f.write("-" * 40 + "\n")
            
            spf_found = False
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt = rdata.to_text()
                    if "v=spf1" in txt:
                        f.write(f"SPF   : FOUND ({txt})\n")
                        spf_found = True
            except: pass
            if not spf_found: 
                f.write("SPF   : MISSING (Vulnerable to Spoofing)\n")

            dmarc_found = False
            try:
                answers = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
                for rdata in answers:
                    txt = rdata.to_text()
                    if "v=DMARC1" in txt:
                        f.write(f"DMARC : FOUND ({txt})\n")
                        dmarc_found = True
            except: pass
            if not dmarc_found: 
                f.write("DMARC : MISSING (Vulnerable to Spoofing)\n")
        
    except Exception as e:
        print(Fore.RED + f"[-] DNS Scan Error: {e}")
