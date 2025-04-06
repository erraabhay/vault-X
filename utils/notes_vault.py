import os
import json
import time
import tempfile
import threading
from config import encrypt_data, decrypt_data

NOTES_FILE = "data/notes.json.enc"
NOTES_DIR = "data/notes"

def ensure_notes_dir():
    os.makedirs(NOTES_DIR, exist_ok=True)

def load_notes(key):
    if not os.path.exists(NOTES_FILE):
        return {}
    with open(NOTES_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = decrypt_data(key, encrypted)
        return json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        print(f"[X] Failed to decrypt notes index: {e}")
        return {}

def save_notes_index(data, key):
    try:
        encrypted = encrypt_data(key, json.dumps(data).encode('utf-8'))
        with open(NOTES_FILE, 'wb') as f:
            f.write(encrypted)
    except Exception as e:
        print(f"[X] Failed to save notes index: {e}")

def destroy_temp_file(file_path):
    time.sleep(120)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"\n[!] Temp file '{os.path.basename(file_path)}' auto-deleted after 2 minutes.")

def open_temp_file(decrypted_data, label, is_binary=False):
    ext = ".pdf" if decrypted_data[:4] == b"%PDF" else ".txt"
    suffix = f"_{label}{ext}"
    mode = 'wb' if is_binary else 'w'
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode=mode)
    try:
        if is_binary:
            temp_file.write(decrypted_data)
        else:
            temp_file.write(decrypted_data.decode('utf-8', errors='ignore'))
        temp_file.close()
        print(f"[✓] Temp file created: {temp_file.name}")
        print("🕒 This file will self-destruct in 2 minutes.")
        threading.Thread(target=destroy_temp_file, args=(temp_file.name,), daemon=True).start()
    except Exception as e:
        print(f"[X] Failed to create temp file: {e}")

def manage(master_pw, key):
    ensure_notes_dir()

    while True:
        print("\n📝 Notes Vault")
        print("1. View Notes")
        print("2. Add New Note (Text Input)")
        print("3. Add Note from File (.txt / .pdf)")
        print("4. Delete Note")
        print("5. Back")

        choice = input("Select option [1-5]: ").strip()
        notes = load_notes(key)

        if choice == '1':
            if not notes:
                print("[!] No notes found.")
            else:
                print("\n📁 Stored Notes:")
                for label in notes.keys():
                    print(f"🔐 {label}.vault")

                selected = input("\nEnter label to view (or press Enter to go back): ").strip()
                if selected and selected in notes:
                    enc_path = os.path.join(NOTES_DIR, notes[selected])
                    if os.path.exists(enc_path):
                        try:
                            with open(enc_path, 'rb') as f:
                                encrypted_data = f.read()
                            decrypted_data = decrypt_data(key, encrypted_data)

                            # Detect file type
                            is_file_upload = notes[selected].endswith('.vault') and (
                                decrypted_data[:4] == b"%PDF" or decrypted_data.isascii() == False
                            )

                            if is_file_upload:
                                open_temp_file(decrypted_data, selected, is_binary=True)
                            else:
                                print(f"\n📄 Content of '{selected}':\n")
                                print(decrypted_data.decode('utf-8', errors='ignore'))

                        except Exception as e:
                            print(f"[X] Failed to decrypt or read the note: {e}")
                    else:
                        print("[X] Encrypted note file missing.")
                elif selected:
                    print("[X] Label not found.")

        elif choice == '2':
            title = input("Note Title: ").strip()
            print("Enter content (end with a single '.' on a line):")
            lines = []
            while True:
                line = input()
                if line.strip() == ".":
                    break
                lines.append(line)
            content = "\n".join(lines)
            encrypted = encrypt_data(key, content.encode('utf-8'))
            file_path = os.path.join(NOTES_DIR, f"{title}.vault")
            with open(file_path, 'wb') as f:
                f.write(encrypted)
            notes[title] = f"{title}.vault"
            save_notes_index(notes, key)
            print("[✓] Note saved securely.")

        elif choice == '3':
            label = input("Enter label for the note: ").strip()
            file_path = input("Enter path to .txt or .pdf: ").strip()

            if not os.path.exists(file_path):
                print("[X] File not found.")
                continue

            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted = encrypt_data(key, data)
                dest_path = os.path.join(NOTES_DIR, f"{label}.vault")
                with open(dest_path, 'wb') as f:
                    f.write(encrypted)
                notes[label] = f"{label}.vault"
                save_notes_index(notes, key)
                print("[✓] File stored securely as:", f"{label}.vault")
            except Exception as e:
                print(f"[X] Failed to encrypt or store file: {e}")

        elif choice == '4':
            label = input("Enter label to delete: ").strip()
            if label in notes:
                encrypted_file = os.path.join(NOTES_DIR, notes[label])
                if os.path.exists(encrypted_file):
                    os.remove(encrypted_file)
                del notes[label]
                save_notes_index(notes, key)
                print("[✓] Note deleted.")
            else:
                print("[X] Note not found.")

        elif choice == '5':
            break
        else:
            print("[X] Invalid choice.")
