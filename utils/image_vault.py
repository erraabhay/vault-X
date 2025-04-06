import os
import json
import time
import tempfile
import subprocess
from config import encrypt_data, decrypt_data

IMAGE_DB_FILE = "data/image_vault.json.enc"
VAULT_IMAGE_DIR = "data/images"

if not os.path.exists(VAULT_IMAGE_DIR):
    os.makedirs(VAULT_IMAGE_DIR)


def load_images(key):
    if not os.path.exists(IMAGE_DB_FILE):
        return {}
    with open(IMAGE_DB_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = decrypt_data(key, encrypted)
        return json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        print(f"[X] Failed to decrypt image database: {e}")
        return {}


def save_images(data, key):
    try:
        encrypted = encrypt_data(key, json.dumps(data).encode('utf-8'))
        with open(IMAGE_DB_FILE, 'wb') as f:
            f.write(encrypted)
    except Exception as e:
        print(f"[X] Failed to save image database: {e}")


def decrypt_and_view_image(label, vault_path, key):
    try:
        with open(vault_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = decrypt_data(key, encrypted_data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(decrypted_data)
            tmp_file_path = tmp_file.name

        print(f"[✓] Image '{label}' decrypted. Auto-destroy in:")
        for i in range(5, 0, -1):
            print(f"   ⏳ {i} seconds", end='\r')
            time.sleep(1)

        subprocess.run(['start', tmp_file_path], shell=True)

        print("[!] Image will be deleted in 10 seconds.")
        time.sleep(10)
        os.remove(tmp_file_path)
        print("[✓] Temp file deleted securely.")

    except Exception as e:
        print(f"[X] Failed to decrypt/view image: {e}")


def manage(master_pw, key):
    while True:
        print("\n🖼️ Image Vault")
        print("1. View Image List")
        print("2. Add & Encrypt Image")
        print("3. View Decrypted Image")
        print("4. Delete Image Record")
        print("5. Back")
        choice = input("Select option [1-5]: ").strip()

        images = load_images(key)

        if choice == '1':
            if not images:
                print("[!] No image records found.")
            else:
                print("\n📁 Stored Images:")
                for name in images.keys():
                    print(f"📁 {name}")

        elif choice == '2':
            name = input("Enter image name/label: ").strip()
            path = input("Enter full image path: ").strip()

            if not os.path.exists(path):
                print("[X] File not found.")
                continue

            try:
                with open(path, 'rb') as img_file:
                    data = img_file.read()
                encrypted_data = encrypt_data(key, data)

                vault_path = os.path.join(VAULT_IMAGE_DIR, f"{name}.vault")
                with open(vault_path, 'wb') as f:
                    f.write(encrypted_data)

                images[name] = vault_path
                save_images(images, key)
                print(f"[✓] Image '{name}' encrypted and saved to vault.")
            except Exception as e:
                print(f"[X] Failed to store image: {e}")

        elif choice == '3':
            name = input("Enter image name to decrypt/view: ").strip()
            if name in images:
                decrypt_and_view_image(name, images[name], key)
            else:
                print("[X] Image not found.")

        elif choice == '4':
            name = input("Enter image name to delete: ").strip()
            if name in images:
                try:
                    os.remove(images[name])
                    del images[name]
                    save_images(images, key)
                    print("[✓] Image and record deleted.")
                except Exception as e:
                    print(f"[X] Failed to delete image file: {e}")
            else:
                print("[X] Record not found.")

        elif choice == '5':
            break
        else:
            print("[X] Invalid choice.")
