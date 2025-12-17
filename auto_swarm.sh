#!/data/data/com.termux/files/usr/bin/bash

TARGET_FILE="targets.txt"

if [ ! -f "$TARGET_FILE" ]; then
    echo "[-] Error: targets.txt not found."
    exit 1
fi

echo "[!] AUTO-SWARM ACTIVATED: Processing target list..."

while IFS= read -r line; do
    # Skip empty lines or comments
    [[ -z "$line" || "$line" =~ ^# ]] && continue

    echo "----------------------------------------------------"
    echo "[⚡] TARGET ACQUIRED: $line"
    echo "----------------------------------------------------"

    # 1. Run the Swarm (Scout + Omnibus)
    ./swarm.sh "$line"

    # 2. Trigger the AI Analysis immediately after each target
    echo "[🧠] Running Hephaestus Analysis..."
    python3 core/engine/hephaestus_judge.py

    # 3. Cool-down period to prevent IP blocks
    echo "[💤] Mission complete. Cooling down for 60 seconds..."
    sleep 60

done < "$TARGET_FILE"

echo "[🏁] ALL TARGETS PROCESSED. Check your dashboard for the full kill-count."
