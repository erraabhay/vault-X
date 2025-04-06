# 📁 SecureVault/utils/password_vault.py
import json
import os
from getpass import getpass
from config import encrypt_data, decrypt_data

VAULT_FILE = "data/passwords.json.enc"

def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        data = decrypt_data(key, encrypted)
        return json.loads(data.decode())
    except Exception:
        print("[X] Failed to decrypt password vault.")
        return {}

def save_vault(data, key):
    encrypted = encrypt_data(key, json.dumps(data).encode())
    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted)

def manage(master_pw, key):
    while True:
        print("\n🔐 Password Vault")
        print("1. View Entries")
        print("2. Add Entry")
        print("3. Delete Entry")
        print("4. Back")
        choice = input("Select option [1-4]: ").strip()

        vault = load_vault(key)

        if choice == '1':
            if not vault:
                print("[!] No entries found.")
            else:
                for name, creds in vault.items():
                    print(f"- {name}: {creds['username']} / {creds['password']}")

        elif choice == '2':
            name = input("Service Name: ").strip()
            username = input("Username: ").strip()
            password = getpass("Password: ").strip()
            vault[name] = {"username": username, "password": password}
            save_vault(vault, key)
            print("[✓] Entry added.")

        elif choice == '3':
            name = input("Service name to delete: ").strip()
            if name in vault:
                del vault[name]
                save_vault(vault, key)
                print("[✓] Entry deleted.")
            else:
                print("[X] Entry not found.")

        elif choice == '4':
            break
        else:
            print("[X] Invalid choice.")
