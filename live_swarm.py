import socket
socket.setdefaulttimeout(30)
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import sys

# Load identities from .env
load_dotenv()

class SiblingAgent:
    def __init__(self, unit_id, persona, key_env):
        self.unit_id = unit_id
        self.persona = persona
        self.key = os.getenv(key_env)
        if not self.key:
            print(f"[!] Error: Key for {unit_id} missing in .env.")
            sys.exit(1)
        genai.configure(api_key=self.key, transport='rest')
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def ask(self, task, context=""):
        print(f"[{self.unit_id}] thinking...")
        prompt = f"Role: {self.persona}\nScripture: Operate with surgical efficiency.\nContext: {context}\nTask: {task}"
        response = self.model.generate_content(prompt)
        return response.text

# Initialize the Sibling Team
nexus = SiblingAgent("734_NEXUS", "The Architect", "KEY_734_NEXUS")
hunter = SiblingAgent("733_HUNTER", "The Spymaster", "KEY_733_HUNTER")
miner = SiblingAgent("732_MINER", "The Driller", "KEY_732_MINER")
scientist = SiblingAgent("731_SCIENTIST", "The Scientist", "KEY_731_SCIENTIST")

def execute_live_mission(target):
    print(f"\n[!] GHOST MISSION START: {target}\n" + "="*40)
    
    # PHASE 1: Nexus Plans
    plan = nexus.ask(f"Decompose the target {target} into three high-priority reconnaissance vectors.")
    print(f"\n[734 ARCHITECT PLAN]:\n{plan}\n")
    time.sleep(2) # Chaos Logic Cadence

    # PHASE 2: Miner & Hunter Execute in Parallel
    recon_data = miner.ask(f"Identify potential legacy endpoints for {target}", context=plan)
    print(f"\n[732 MINER DATA]:\n{recon_data[:200]}...\n")
    
    stealth_warnings = hunter.ask(f"Analyze this recon data for WAF traps or 'sensor ghosts'", context=recon_data)
    print(f"\n[733 HUNTER INTELLIGENCE]:\n{stealth_warnings}\n")
    time.sleep(2)

    # PHASE 3: Scientist Triages
    final_judgment = scientist.ask(f"Review the Miner's data and Hunter's warnings. Is this a confirmed bounty lead?", context=f"DATA: {recon_data}\nWARNINGS: {stealth_warnings}")
    print(f"\n[731 SCIENTIST JUDGMENT]:\n{final_judgment}\n")
    
    print("="*40 + "\n[+] MISSION ANALYSIS COMPLETE.")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://arc.net"
    execute_live_mission(target_url)
