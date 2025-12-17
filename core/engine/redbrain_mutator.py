import os
import json
import requests

def mutate_payloads():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[-] Error: GEMINI_API_KEY not set.")
        return

    print("[!] RedBrain Mutator: Evolving Payloads from 742 Hits...")
    
    try:
        with open("public/metadata.json", "r") as f:
            data = json.load(f)
        
        # Focus on the 'findings' the Judge just analyzed
        hits = data.get('findings', [])[:3]
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"SYSTEM: You are an adversarial payload engineer. Context: {hits}. TASK: Generate 5 highly obfuscated, mutated versions of these successful attack vectors. Use encoding (Base64, Hex, URL), polyglots, and WAF-bypass techniques. Output ONLY a JSON list of strings."
                }]
            }]
        }

        response = requests.post(url, json=payload)
        res_json = response.json()
        
        if 'candidates' in res_json:
            mutations = res_json['candidates'][0]['content']['parts'][0]['text']
            # Clean AI text to ensure it's valid JSON
            clean_json = mutations.replace("```json", "").replace("```", "").strip()
            
            data['mutated_payloads'] = json.loads(clean_json)
            with open("public/metadata.json", "w") as f:
                json.dump(data, f, indent=4)
                
            print("[+] Mutation Successful. 5 New Vectors added to Nexus.")
            print(f"\nRED-BRAIN GENERATED:\n{clean_json}")
        else:
            print("[-] Mutation Refused by Safety Filters.")

    except Exception as e:
        print(f"[-] Mutator Error: {e}")

if __name__ == "__main__":
    mutate_payloads()
