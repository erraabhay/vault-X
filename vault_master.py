
import os
import getpass
from config import is_first_time, save_metadata, load_metadata
from utils.password_vault import manage as manage_passwords
from utils.secret_keys import manage as manage_secrets
from utils.notes_vault import manage as manage_notes
from utils.image_vault import manage as manage_images
from utils.folder_vault import manage as manage_folders  
from utils.cleanup import clean_temp_output

def initialize_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/images", exist_ok=True)
    os.makedirs("data/notes", exist_ok=True)
    os.makedirs("data/folders", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

def main():
    print("\n🔐 Welcome to SecureVault Terminal Interface 🔐\n")
    initialize_directories()

  
    if is_first_time():
        print("[!] First-time setup detected.")
        while True:
            pw1 = getpass.getpass("🛠️  Create a master password: ")
            pw2 = getpass.getpass("🔁 Confirm master password: ")
            if pw1 == pw2:
                save_metadata(pw1)
                print("[✓] Master password set successfully!\n")
                break
            else:
                print("[X] Passwords did not match. Try again.\n")

    
    attempts = 3
    key = None
    while attempts > 0:
        password = getpass.getpass("Enter master password: ")
        try:
            key = load_metadata(password)
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            attempts -= 1
    if key is None:
        print("\n[!] Too many failed attempts. Exiting.")
        return

    
    while True:
        print("\n SecureVault Main Menu")
        print("1️  Password Vault")
        print("2️  Secret Keys")
        print("3️  Notes Vault")
        print("4️  Image Vault")
        print("5️  Folder Vault")
        print("6️  Cleanup Temporary Files")
        print("7️  Exit")

        choice = input(" Select option [1-7]: ").strip()

        if choice == '1':
            manage_passwords(password, key)
        elif choice == '2':
            manage_secrets(password, key)
        elif choice == '3':
            manage_notes(password, key)
        elif choice == '4':
            manage_images(password, key)
        elif choice == '5':
            manage_folders(key) 
        elif choice == '6':
            clean_temp_output()
        elif choice == '7':
            print("\n[✓] Exiting SecureVault. Stay safe! 🔒")
            break
        else:
            print("[X] Invalid choice. Try again.")

if __name__ == "__main__":
    main()
