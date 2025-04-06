# 📁 SecureVault/config.py

import os
import base64
import json
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

# ========================== 🔒 Constants & Paths ==========================

backend = default_backend()
DATA_DIR = "data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
NOTES_DIR = os.path.join(DATA_DIR, "notes")
FOLDER_DIR = os.path.join(DATA_DIR, "folders")
TEMP_DIR = "temp"

# 🔐 Vault File Paths (All .vault extensions)
PATHS = {
    "metadata": os.path.join(DATA_DIR, "metadata.vault"),
    "notes": os.path.join(DATA_DIR, "notes.vault"),
    "passwords": os.path.join(DATA_DIR, "passwords.vault"),
    "secrets": os.path.join(DATA_DIR, "secrets.vault"),
    "image_vault": os.path.join(DATA_DIR, "image_vault.vault"),
    "folder_vault": os.path.join(DATA_DIR, "folder_vault.vault")  # ✅ NEW!
}

METADATA_FILE = PATHS["metadata"]
METADATA_MARKER = b"vault-ok"

# ========================== 🔐 Crypto Functions ==========================

def generate_salt(length=16):
    return os.urandom(length)

def derive_key(password, salt, iterations=100_000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    return kdf.derive(password.encode())

def encrypt_data(key, plaintext: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return base64.b64encode(nonce + ciphertext)

def decrypt_data(key, encrypted_data: bytes) -> bytes:
    try:
        raw = base64.b64decode(encrypted_data)
        nonce = raw[:12]
        ciphertext = raw[12:]
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)
    except (InvalidTag, ValueError):
        raise ValueError("Decryption failed. Possibly wrong password or corrupted file.")

# ========================== 🧠 Metadata ==========================

def is_first_time():
    return not os.path.exists(METADATA_FILE)

def save_metadata(password):
    salt = generate_salt()
    key = derive_key(password, salt)
    encrypted = encrypt_data(key, METADATA_MARKER)
    metadata = {
        "salt": base64.b64encode(salt).decode(),
        "verify": encrypted.decode()
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

def load_metadata(password):
    if not os.path.exists(METADATA_FILE):
        raise FileNotFoundError("Metadata not found.")
    
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)

    salt = base64.b64decode(metadata["salt"])
    key = derive_key(password, salt)
    try:
        decrypted = decrypt_data(key, metadata["verify"].encode())
        if decrypted == METADATA_MARKER:
            return key
        else:
            raise ValueError("Incorrect password or corrupted metadata.")
    except Exception:
        raise ValueError("Incorrect password or corrupted metadata.")

# ========================== 🔁 Master Reset ==========================

def reset_master_password(old_password, new_password):
    _ = load_metadata(old_password)  # Validate old password
    save_metadata(new_password)      # Save new metadata
    return True
