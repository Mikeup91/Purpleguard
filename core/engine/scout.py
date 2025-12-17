import requests
from bs4 import BeautifulSoup
import sys
import json
from urllib.parse import urljoin, urlparse

def scout_target(url):
    print(f"[!] Scouting: {url}")
    try:
        # User-Agent makes the request look like a real browser
        headers = {'User-Agent': 'Mozilla/5.0 (PurpleGuard/3.2)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        base_domain = urlparse(url).netloc
        found_urls = set()

        for a in soup.find_all('a', href=True):
            link = a['href']
            # Join relative paths to the base URL
            full_url = urljoin(url, link)
            
            # Only keep links that stay on the same target domain
            if urlparse(full_url).netloc == base_domain:
                found_urls.add(full_url)
        
        print(f"[+] Found {len(found_urls)} internal links.")

        # Update metadata.json
        if os.path.exists("public/metadata.json"):
            with open("public/metadata.json", "r+") as f:
                data = json.load(f)
                # Ensure 'findings' list exists
                if 'findings' not in data: data['findings'] = []
                
                new_count = 0
                for target in found_urls:
                    # Avoid duplicates
                    if not any(f['target'] == target for f in data['findings']):
                        data['findings'].append({"type": "SCOUTED", "target": target})
                        new_count += 1
                
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print(f"[+] Added {new_count} new targets to Nexus.")
        else:
            print("[-] Error: public/metadata.json not found.")
            
    except Exception as e:
        print(f"[-] Scout Error: {e}")

if __name__ == "__main__":
    import os
    if len(sys.argv) > 1:
        scout_target(sys.argv[1])
