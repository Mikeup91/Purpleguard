import sys
import time
import random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from evolution.nexus import Nexus
from core.spider import DeepSpider
from core.mutator import MutationLab
from modules.vectors import VectorSQLi, VectorXSS, VectorLFI, VectorSSRF
from modules.reporter import AuditReporter

class OmnibusEngine:
    def __init__(self, targets, max_threads=10):
        self.targets = targets if isinstance(targets, list) else [targets]
        self.nexus = Nexus()
        self.spider = DeepSpider(self.nexus)
        self.mutator = MutationLab()
        self.session = requests.Session()
        self.max_threads = max_threads
        self.vectors = [VectorSQLi(), VectorXSS(), VectorLFI(), VectorSSRF()]
        self.reporter = AuditReporter(self.nexus)

    def engage(self):
        print("\n[!] SWARM STARTING - AGGRESSIVE MODE")
        for target in self.targets:
            print(f"[*] Targeting: {target}")
            endpoints = self.spider.crawl(target)
            if not endpoints: continue
            
            tasks = []
            for ep in endpoints:
                for vector in self.vectors:
                    payloads = vector.payloads(self.nexus)
                    for raw_pl in payloads:
                        variants = self.mutator.generate_variants(raw_pl, vector.name())
                        for final_pl in variants[:2]:
                            param = ep.get('params', ['id'])[0] if ep.get('params') else 'id'
                            tasks.append((ep, param, final_pl, vector.name()))
            
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = [executor.submit(self._fire, e, p, pl, v) for e, p, pl, v in tasks]
                for f in as_completed(futures):
                    try: f.result()
                    except: pass
        
        # This is the line that creates the file
        self.reporter.generate_markdown()

    def _fire(self, ep, param, payload, v_type):
        try:
            start = time.time()
            resp = self.session.get(ep['url'], params={param: payload}, timeout=5)
            dur = time.time() - start
            
            if v_type == "SQLi":
                if dur > 4 or any(x in resp.text.lower() for x in ['mysql', 'sql syntax', 'error']):
                    self.nexus.record_kill({"target": ep['url'], "type": v_type, "param": param, "payload": payload, "confidence": 95})
            elif v_type == "XSS" and (payload in resp.text or "<script>" in resp.text.lower()):
                self.nexus.record_kill({"target": ep['url'], "type": v_type, "param": param, "payload": payload, "confidence": 85})
            elif v_type == "LFI" and any(i in resp.text for i in ['root:', 'bin:']):
                self.nexus.record_kill({"target": ep['url'], "type": v_type, "param": param, "payload": payload, "confidence": 100})
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            if v_type == "SQLi" and 'sleep' in payload.lower():
                self.nexus.record_kill({"target": ep['url'], "type": v_type, "param": param, "payload": payload, "confidence": 90, "status": "TIMEOUT_MATCH"})
        except: pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = OmnibusEngine(sys.argv[1])
        engine.engage()

    def sync_to_platform(self):
        import json
        data = {
            "last_scan": time.ctime(),
            "total_kills": len(self.nexus.knowledge.get('confirmed_vulns', [])),
            "findings": self.nexus.knowledge.get('confirmed_vulns', [])
        }
        # Path adjusted for your repo structure (writing to root metadata.json)
        try:
            with open("metadata.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"[+] PurpleGuard Platform Synced: metadata.json updated.")
        except Exception as e:
            print(f"[-] Sync Failed: {e}")

# --- CHAOS LOGIC MODULE ---
import time
import random

def chaos_delay(base_delay=5, intensity=0.5):
    """Adds non-linear jitter to mimic human behavior."""
    jitter = base_delay * intensity
    actual_sleep = base_delay + random.uniform(-jitter, jitter)
    time.sleep(max(0.1, actual_sleep))

def get_chaotic_headers():
    """Cycles identity to prevent JA3/Fingerprint tracking."""
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(ua_list),
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
# --- END CHAOS LOGIC ---

# --- WAF WATCHDOG SNIPER ---
BASE_DELAY = 5  # Global starting delay

def watchdog_monitor(status_code):
    """Adjusts swarm speed based on WAF responses."""
    global BASE_DELAY
    if status_code in [403, 429]:
        print(f"[!] WAF DETECTED ({status_code}). Escalating Chaos Level...")
        BASE_DELAY *= 2  # Double the wait time
        time.sleep(30)   # Immediate emergency cool-down
    elif status_code == 200 and BASE_DELAY > 5:
        BASE_DELAY -= 0.5 # Gradually speed back up if clear
    
    # Run the chaos delay with the updated base
    chaos_delay(base_delay=BASE_DELAY, intensity=0.8)
# --- END WATCHDOG ---
