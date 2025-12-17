#!/data/data/com.termux/files/usr/bin/bash

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: ./swarm.sh <target_url>"
    exit 1
fi

echo "[!] INITIALIZING SWARM ON: $TARGET"

# 1. Run the Scout to find parameters and links
echo "[*] Phase 1: Scouting for vectors..."
python3 core/engine/scout.py "$TARGET"

# 2. Extract the newly scouted URLs from metadata.json and feed them to Omnibus
echo "[*] Phase 2: Launching Omnibus Engine on scouted targets..."

# We use 'jq' to parse the JSON easily. Let's install it first just in case.
pkg install jq -y &> /dev/null

# Get all 'SCOUTED' targets and run the engine on each
jq -r '.findings[] | select(.type=="SCOUTED") | .target' public/metadata.json | while read -r url; do
    echo "[~] Attacking scouted path: $url"
    python3 core/engine/omnibus.py "$url"
done

echo "[+] SWARM COMPLETE. Check dashboard for confirmed kills."
