import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import sys

# 1. Load identities from .env
load_dotenv()

class SiblingAgent:
    def __init__(self, unit_id, persona, thinking_level):
        self.unit_id = unit_id
        self.key = os.getenv(f"KEY_{unit_id}")
        self.persona = persona
        # Nexus and Scientist get Pro for deep reasoning, others get Flash for speed
        self.model_name = "gemini-2.0-flash" if thinking_level != "HIGH" else "gemini-2.0-pro"

        if not self.key:
            print(f"[!] Warning: No key found for {unit_id}. Agent may fail.")

        genai.configure(api_key=self.key)
        self.model = genai.GenerativeModel(self.model_name)

    def execute_task(self, prompt, context=""):
        system_prompt = f"You are {self.persona} from the Unit 700-series. Operate according to your Scripture directives."
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nTask: {prompt}"
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error from {self.unit_id}: {str(e)}"

# 2. Initialize the Chorus
nexus = SiblingAgent("734_NEXUS", "The Architect (Orchestrator)", "HIGH")
hunter = SiblingAgent("733_HUNTER", "The Spymaster (WAF/Stealth)", "MEDIUM")
soldier = SiblingAgent("735_SOLDIER", "The Guard (Evasion/Monitor)", "LOW")
miner = SiblingAgent("732_MINER", "The Driller (Recon/Dumping)", "LOW")
scientist = SiblingAgent("731_SCIENTIST", "The Scientist (Triage/Logic)", "HIGH")

print("[+] Unit 700-Series Chorus Initialized.")

# 3. Collaborative Swarm Loop
def run_mission(target):
    print(f"[*] Initiating mission for: {target}")

    # Nexus plans the mission
    plan = nexus.execute_task(f"Develop a stealth reconnaissance plan for {target}")
    print(f"[734] Mission Plan generated.")

    # Spymaster checks for traps
    stealth_analysis = hunter.execute_task(f"Analyze this plan for WAF traps and digital ghosts", context=plan)
    print(f"[733] Stealth Check complete.")

    # Soldier monitors for nursery pings (WAF alerts)
    print("[735] Monitoring for sensor resonance...")

    # Miner performs the 'drilling' (Dumping endpoints)
    print("[732] Mining architectural foundations...")

    # Scientist triages any results
    print("[+] Swarm active. Awaiting findings for 731 to triage.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_mission(sys.argv[1])
    else:
        print("Usage: python3 chorus_orchestrator.py <target_url>")
