import json
import os
from config import encrypt_data, decrypt_data

SECRETS_FILE = "data/secrets.json.enc"

def load_secrets(key):
    if not os.path.exists(SECRETS_FILE):
        return {}
    with open(SECRETS_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = decrypt_data(key, encrypted)
        return json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        print(f"[X] Failed to load secrets: {e}")
        return {}

def save_secrets(data, key):
    try:
        encrypted = encrypt_data(key, json.dumps(data).encode('utf-8'))
        with open(SECRETS_FILE, 'wb') as f:
            f.write(encrypted)
    except Exception as e:
        print(f"[X] Failed to save secrets: {e}")

def manage(master_pw, key):
    while True:
        print("\n🔑 Secret Keys Vault")
        print("1. View Secret Labels")
        print("2. Add/Edit Secret")
        print("3. Delete Secret")
        print("4. Back")
        choice = input("Select option [1-4]: ").strip()

        secrets = load_secrets(key)

        if choice == '1':
            if not secrets:
                print("[!] No secrets found.")
            else:
                print("\n📁 Stored Secret Labels:")
                for name in secrets:
                    print(f"🔐 {name}")
                
                selected = input("\nEnter label to view (or press Enter to go back): ").strip()
                if selected:
                    if selected in secrets:
                        print(f"\n🔍 Secret for '{selected}':\n{secrets[selected]}")
                    else:
                        print("[X] No such label found.")

        elif choice == '2':
            name = input("Enter key name: ").strip()
            value = input("Enter key value: ").strip()
            secrets[name] = value
            save_secrets(secrets, key)
            print("[✓] Secret saved.")

        elif choice == '3':
            name = input("Key name to delete: ").strip()
            if name in secrets:
                del secrets[name]
                save_secrets(secrets, key)
                print("[✓] Secret deleted.")
            else:
                print("[X] Secret not found.")

        elif choice == '4':
            break
        else:
            print("[X] Invalid choice.")
