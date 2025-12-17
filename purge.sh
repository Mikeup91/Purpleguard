#!/data/data/com.termux/files/usr/bin/bash

# Define paths
DATA_FILE="public/metadata.json"
BACKUP_DIR="$HOME/storage/downloads/purpleguard_archives"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

echo "[!] PURGE SEQUENCE INITIATED..."

# 1. Archive the current data to phone storage
mkdir -p "$BACKUP_DIR"
if [ -f "$DATA_FILE" ]; then
    cp "$DATA_FILE" "$BACKUP_DIR/backup_$TIMESTAMP.json"
    echo "[+] Current session archived to: $BACKUP_DIR"
fi

# 2. Reset the metadata.json to a clean state
cat > "$DATA_FILE" << 'DATA'
{
    "total_kills": 0,
    "last_scan": "CLEARED",
    "findings": [],
    "ai_analysis": "",
    "mutated_payloads": []
}
DATA

echo "[+] Telemetry wiped. Dashboard reset to 0."
echo "[!] SYSTEM READY FOR NEW TARGET."
