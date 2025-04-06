
import os
import time
import zipfile
import tempfile
import shutil
import threading
from config import encrypt_data, decrypt_data

VAULTED_DIR = "data/vaulted"
TEMP_DIR = "data/temp_decrypted"
os.makedirs(VAULTED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def secure_folder_to_vault(folder_path, key):
    if not os.path.isdir(folder_path):
        print("[X] Invalid folder path.")
        return

    folder_name = os.path.basename(folder_path.rstrip('/\\'))
    vault_path = os.path.join(VAULTED_DIR, f"{folder_name}.vault")

    try:
        zip_bytes = tempfile.SpooledTemporaryFile()
        with zipfile.ZipFile(zip_bytes, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        zip_bytes.seek(0)

        encrypted = encrypt_data(key, zip_bytes.read())
        with open(vault_path, 'wb') as f:
            f.write(encrypted)

        print(f"[✓] Folder encrypted and saved as: {vault_path}")
    except Exception as e:
        print(f"[X] Failed to encrypt folder: {e}")

def decrypt_vault_to_temp(vault_file, key):
    try:
        with open(os.path.join(VAULTED_DIR, vault_file), 'rb') as f:
            encrypted = f.read()

        decrypted_data = decrypt_data(key, encrypted)
        temp_folder = os.path.join(TEMP_DIR, vault_file.replace('.vault', ''))
        os.makedirs(temp_folder, exist_ok=True)

        zip_temp = tempfile.SpooledTemporaryFile()
        zip_temp.write(decrypted_data)
        zip_temp.seek(0)

        with zipfile.ZipFile(zip_temp, 'r') as zipf:
            zipf.extractall(temp_folder)

        print(f"[✓] Decrypted to temporary folder: {temp_folder}")
        print("[🕒] This will self-destruct in 2 minutes.")

        threading.Thread(target=auto_delete, args=(temp_folder, 120), daemon=True).start()

    except Exception as e:
        print(f"[X] Failed to decrypt .vault file: {e}")

def auto_delete(path, delay_sec):
    time.sleep(delay_sec)
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print(f"[💥] Temporary folder '{os.path.basename(path)}' deleted after {delay_sec} seconds.")

def manage(key):
    while True:
        print("\n📁 Secure Folder Vault")
        print("1. Encrypt and Store a Folder")
        print("2. List Vaulted Folders")
        print("3. View a Vault (Decrypt Temporarily)")
        print("4. Delete a Vault")
        print("5. Back")

        choice = input("Select option [1-5]: ").strip()

        if choice == '1':
            folder_path = input("📂 Enter full path to folder: ").strip()
            secure_folder_to_vault(folder_path, key)

        elif choice == '2':
            vaulted = [f for f in os.listdir(VAULTED_DIR) if f.endswith('.vault')]
            if not vaulted:
                print("[!] No folders vaulted yet.")
            else:
                print("📦 Vaulted folders:")
                for i, f in enumerate(vaulted, 1):
                    print(f"{i}. {f}")

        elif choice == '3':
            vaulted = [f for f in os.listdir(VAULTED_DIR) if f.endswith('.vault')]
            if not vaulted:
                print("[!] No vaulted folders.")
                continue
            for i, f in enumerate(vaulted, 1):
                print(f"{i}. {f}")
            idx = input("🔍 Enter number to view: ").strip()
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(vaulted):
                    decrypt_vault_to_temp(vaulted[idx], key)
                else:
                    print("[X] Invalid selection.")
            except:
                print("[X] Invalid input.")

        elif choice == '4':
            vaulted = [f for f in os.listdir(VAULTED_DIR) if f.endswith('.vault')]
            if not vaulted:
                print("[!] No vaulted folders.")
                continue
            for i, f in enumerate(vaulted, 1):
                print(f"{i}. {f}")
            idx = input("🗑️  Enter number to delete: ").strip()
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(vaulted):
                    os.remove(os.path.join(VAULTED_DIR, vaulted[idx]))
                    print("[✓] Vault deleted.")
                else:
                    print("[X] Invalid selection.")
            except:
                print("[X] Invalid input.")

        elif choice == '5':
            break
        else:
            print("[X] Invalid option.")
