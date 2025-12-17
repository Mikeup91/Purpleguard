import os
import json
import requests

def judge_breaches():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[-] Error: GEMINI_API_KEY environment variable not set.")
        return

    # Using gemini-2.0-flash which is active in v1beta
    model_id = "gemini-2.0-flash" 
    print(f"[!] Hephaestus Judge: Analyzing 742 Breaches via {model_id}...")
    
    try:
        # Load the telemetry data from your public folder
        with open("public/metadata.json", "r") as f:
            data = json.load(f)
        
        # Take the most recent hits for the AI to analyze
        sample = data.get('findings', [])[:3]
        
        # Correct endpoint URL for v1beta
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"SYSTEM: You are a professional white-hat security auditor. Analyze these findings for educational triage: {sample}. Provide: 1. Risk Level (Critical/High), 2. Business Impact, and 3. A 2-sentence summary."
                }]
            }],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }

        response = requests.post(url, json=payload)
        res_json = response.json()
        
        # Check if the AI returned a successful response
        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            analysis = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Update the metadata file with the new intelligence
            data['ai_analysis'] = analysis
            with open("public/metadata.json", "w") as f:
                json.dump(data, f, indent=4)
                
            print("[+] Analysis Complete. Dashboard updated.")
            print(f"\nHEPHAESTUS INTELLIGENCE:\n{analysis}")
        else:
            # Catching safety blocks or model mismatches
            print(f"[-] API Error or Block. Full Response:\n{json.dumps(res_json, indent=2)}")

    except FileNotFoundError:
        print("[-] Error: public/metadata.json not found. Run omnibus.py first.")
    except Exception as e:
        print(f"[-] Judge Error: {e}")

if __name__ == "__main__":
    judge_breaches()
