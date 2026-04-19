# 🔐 SecureVault — Text Encryption System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3%2B-black?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Encryption-RSA--2048-purple?style=flat-square&logo=gnuprivacyguard" alt="RSA-2048">
  <img src="https://img.shields.io/badge/Database-SQLite-blue?style=flat-square&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT">
</p>

> **SecureVault** is a full-stack web application that lets authenticated users encrypt and decrypt arbitrary text using **RSA-2048 asymmetric encryption**. All encrypted messages are stored in a local SQLite database and can be browsed, deleted, and exported from a dedicated **report dashboard**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **RSA-2048 Encryption** | Military-grade asymmetric public/private key encryption |
| 👤 **User Authentication** | Secure registration & login with bcrypt-hashed passwords |
| 🗄️ **Persistent Storage** | All encrypted messages stored with timestamps in SQLite |
| 📊 **Encryption Report** | Full history table with stats, per-row delete, and CSV export |
| 📋 **Copy to Clipboard** | One-click copy for cipher text and decrypted results |
| 🗑️ **AJAX Delete** | Smooth animated deletion of history entries |
| ⬇️ **Export CSV** | Download complete encryption history as a spreadsheet |
| 🖨️ **Print Report** | Print-friendly report view |
| 🎨 **Premium Dark UI** | Glassmorphism design with gradient accents and animations |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **Encryption** | `cryptography` library — RSA-OAEP with SHA-256 |
| **Auth / Hashing** | Werkzeug `generate_password_hash` / `check_password_hash` |
| **Database** | SQLite 3 (via Python `sqlite3`) |
| **Frontend** | Jinja2 templates, Vanilla CSS (glassmorphism), Vanilla JS |
| **Fonts** | Google Fonts — Inter |

---

## 📁 Project Structure

```
text_encryption/
├── secure_app/
│   ├── app.py           # Flask application & all routes
│   ├── auth.py          # User registration & login logic
│   ├── crypto_utils.py  # RSA key generation, encrypt/decrypt
│   ├── config.py        # Shared path configuration
│   └── init_db.py       # Database initializer
├── templates/
│   ├── base.html        # Base layout (navbar, footer)
│   ├── index.html       # Landing page
│   ├── login.html       # Login form
│   ├── register.html    # Registration form
│   ├── dashboard.html   # User dashboard
│   ├── encrypt.html     # Encrypt text page
│   ├── decrypt.html     # Decrypt text page
│   └── report.html      # Encryption history report
├── static/
│   └── style.css        # Premium dark glassmorphism CSS
├── database.db          # Auto-created SQLite database
├── requirements.txt
├── WINDOWS_SETUP.md     # Detailed Windows setup guide
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Download |
|---|---|---|
| **Python** | 3.8 or higher | [python.org](https://www.python.org/downloads/) |
| **pip** | Included with Python | — |
| **Git** *(optional)* | Any | [git-scm.com](https://git-scm.com/) |

> **Windows users:** See the detailed [WINDOWS_SETUP.md](WINDOWS_SETUP.md) guide for step-by-step instructions with screenshots guidance.

---

### 🪟 Windows Setup

```cmd
:: 1. Open Command Prompt (Win + R → type cmd → Enter)

:: 2. Clone or download the project
git clone <your-repo-url>
cd text_encryption

:: 3. Create virtual environment
python -m venv venv

:: 4. Activate virtual environment
venv\Scripts\activate

:: 5. Install dependencies
pip install -r requirements.txt

:: 6. Run the application
python secure_app\app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

### 🐧 Linux / macOS Setup

```bash
# 1. Clone the project
git clone <your-repo-url>
cd text_encryption

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python secure_app/app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## 📖 Usage Guide

1. **Register** — Create a new account at `/register`
2. **Login** — Sign in at `/login`
3. **Encrypt** — Navigate to **Encrypt Text**, type your message, click *Encrypt Now*
4. **Copy cipher** — Use the *Copy* button to grab the Base64 cipher text
5. **Decrypt** — Navigate to **Decrypt Text**, paste the cipher, click *Decrypt Now*
6. **Report** — Click *View Report* from the dashboard to see all encryptions
   - View stats (total count, unique users)
   - Delete individual records (AJAX, no page reload)
   - Export all records to CSV
   - Print the report

---

## 🔒 How the Encryption Works

```
Plain Text
    │
    ▼
RSA Public Key  ──►  OAEP Padding (SHA-256)  ──►  Cipher Bytes
    │
    ▼
Base64 Encode  ──►  Stored in DB / Displayed to user

─────────────────────────────────────────────────

Base64 Cipher
    │
    ▼
Base64 Decode  ──►  Cipher Bytes
    │
    ▼
RSA Private Key  ──►  OAEP Unpad  ──►  Plain Text
```

> ⚠️ **Note:** The RSA key pair is generated **in memory** at startup. This means encrypted data **cannot be decrypted** after restarting the server (new keys are generated). For production use, keys should be persisted to disk.

---

## 📊 Database Schema

### `users` table
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| username | TEXT UNIQUE | Login username |
| password | TEXT | bcrypt-hashed password |

### `messages` table
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| user | TEXT | Username who encrypted |
| original_text | TEXT | Plain text before encryption |
| data | TEXT | Base64-encoded RSA cipher |
| timestamp | DATETIME | When it was encrypted |

---

## ⚙️ Configuration

Edit `secure_app/app.py` to change:

```python
app.secret_key = "supersecretkey_change_in_production"
```

> ⚠️ **Always change the secret key before deploying to production!**

---

## 🧪 Routes Summary

| Route | Method | Auth | Description |
|---|---|---|---|
| `/` | GET | No | Landing page |
| `/register` | GET, POST | No | Create account |
| `/login` | GET, POST | No | Sign in |
| `/logout` | GET | Yes | Sign out |
| `/dashboard` | GET | Yes | User dashboard |
| `/encrypt` | GET, POST | Yes | Encrypt text |
| `/decrypt` | GET, POST | Yes | Decrypt text |
| `/report` | GET | Yes | Encryption history |
| `/report/delete/<id>` | POST | Yes | Delete a record (AJAX) |
| `/report/export` | GET | Yes | Download history as CSV |

---

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `'python' is not recognized` | Python not in PATH | Re-install Python with **"Add to PATH"** checked |
| `ModuleNotFoundError: flask` | venv not activated | Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux) |
| `Port 5000 already in use` | Another app using 5000 | Change port: `app.run(port=5001)` in `app.py` |
| Decryption fails after restart | Keys are in-memory only | Encrypt and decrypt in the **same server session** |
| `pip` command not found | Python not installed correctly | Reinstall Python from python.org |

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Cryptography](https://cryptography.io/) — RSA encryption primitives
- [Werkzeug](https://werkzeug.palletsprojects.com/) — Password hashing
- [Google Fonts](https://fonts.google.com/) — Inter typeface
