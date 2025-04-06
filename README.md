# vault-X
---

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Terminal-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()

> A terminal-based encrypted vault to securely store passwords, keys, notes, images, and folders – all protected by a master password with AES-256 encryption.

---

## 🚀 Features

### ✅ Master Password Protection
- Secure onboarding with password verification
- AES-256 encryption key derived using password + salt
- 3-attempt login system with fail-safe exit

---

### 🔐 Vault Modules

| Module        | Description |
|---------------|-------------|
| 🔒 **Password Vault**     | Store and manage encrypted passwords |
| 🔑 **Secret Keys Vault**  | Store API tokens, SSH keys, and confidential strings |
| 📝 **Notes Vault**        | Write and encrypt personal or sensitive notes |
| 🖼️ **Image Vault**        | Securely store and encrypt images |
| 📁 **Folder Vault**       | Add folders and encrypt entire contents securely |

> All data is encrypted with AES-256, accessible only through your master password.

---

### 🧼 Temp File Management
- `temp/` directory used for decrypted previews
- Option to clean up temporary files directly from the menu

---

## 🧱 Project Structure

```
SecureVault/
├── data/
│   ├── images/
│   ├── notes/
│   ├── folders/
│   └── metadata.vault
├── temp/
├── utils/
│   ├── password_vault.py
│   ├── secret_keys.py
│   ├── notes_vault.py
│   ├── image_vault.py
│   ├── folder_vault.py
│   └── cleanup.py
├── config.py
└── vault_master.py
```

---

## 📦 Installation

### Requirements
- Python 3.8 or higher
- Works on Windows, Linux, and macOS

### Setup

```bash
git clone https://github.com/erraabhay/vault-X.git
cd vault-X
python vault_master.py
```

---

## 🔐 Security Design

- **AES-256 Encryption** for all stored data
- **Salted Key Derivation** using PBKDF2 or scrypt
- **No plain-text secrets** stored anywhere
- If metadata is deleted, old encrypted files remain inaccessible

> Even if someone resets the master password by deleting metadata, they **cannot decrypt previously stored data** without the correct key and salt.

---

## 💡 Suggested Features (Future Scope)

- 🔄 Cloud sync with encryption (via Dropbox/Drive API)
- 📸 Intruder detection via webcam on wrong attempts
- 🧠 Password strength analyzer
- ⌨️ Command-line arguments for automation
- 🗂️ Search and tagging inside vaults
- 🔍 Biometric or hardware key integration (YubiKey)

---

## 🧑‍💻 Author

**Developer:** [abhay]  
📧 `erraabhay@gmail.com`

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
