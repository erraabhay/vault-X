# 📁 SecureVault/utils/cleanup.py
import os

TEMP_FILES = [
    "temp/output.tmp",
    "temp/decrypted_file.tmp",
    "temp/session.tmp"
]

def clean_temp_output():
    cleaned = False
    for file_path in TEMP_FILES:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[i] Removed temp file: {file_path}")
                cleaned = True
            except Exception as e:
                print(f"[!] Failed to remove {file_path}: {e}")
    if not cleaned:
        print("[i] No temp files found to clean.")
