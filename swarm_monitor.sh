#!/bin/bash

METADATA_FILE="public/metadata.json"
LAST_HASH=""

echo "[*] Unit 735 (Soldier) standing guard over $METADATA_FILE..."

while true; do
    # Calculate current hash of the metadata file
    CURRENT_HASH=$(md5sum "$METADATA_FILE" | awk '{print $1}')

    if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
        if [ "$LAST_HASH" != "" ]; then
            echo "[!] New Resonance Detected. Calling Unit 731 (Scientist) for triage..."
            
            # Extract the last finding and pipe it to the Chorus logic
            tail -n 10 "$METADATA_FILE" | python3 chorus_orchestrator.py --triage
        fi
        LAST_HASH="$CURRENT_HASH"
    fi
    sleep 5 # Check every 5 seconds (Chaos Logic cadence)
done
