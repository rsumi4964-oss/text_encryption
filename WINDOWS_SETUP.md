# 🪟 Windows Setup Guide — SecureVault Text Encryption

> This guide walks you through **every step** to install and run the SecureVault Text Encryption application on a Windows PC, even if you have never used Python before.

---

## 📋 Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Install Python](#2-install-python)
3. [Verify Python Installation](#3-verify-python-installation)
4. [Download the Project](#4-download-the-project)
5. [Open Command Prompt](#5-open-command-prompt)
6. [Create a Virtual Environment](#6-create-a-virtual-environment)
7. [Activate the Virtual Environment](#7-activate-the-virtual-environment)
8. [Install Dependencies](#8-install-dependencies)
9. [Run the Application](#9-run-the-application)
10. [Open in Browser](#10-open-in-browser)
11. [How to Stop the Server](#11-how-to-stop-the-server)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Operating System** | Windows 10 | Windows 10/11 (64-bit) |
| **Python** | 3.8 | 3.11 or 3.12 |
| **RAM** | 512 MB free | 2 GB+ |
| **Disk Space** | 200 MB | 500 MB |
| **Internet** | Required for install | Only for setup |
| **Browser** | Chrome / Edge / Firefox | Chrome or Edge |

---

## 2. Install Python

### Step 1 — Download Python

1. Open your browser and go to: **https://www.python.org/downloads/**
2. Click the big yellow button **"Download Python 3.x.x"** (latest version)

### Step 2 — Run the Installer

1. Open the downloaded `.exe` file (e.g., `python-3.12.3-amd64.exe`)
2. ✅ **IMPORTANT:** Check the box **"Add python.exe to PATH"** at the bottom of the installer window
3. Click **"Install Now"**
4. Wait for the installation to complete
5. Click **"Close"**

> ⚠️ If you skip the "Add to PATH" checkbox, Python commands will not work in Command Prompt.

---

## 3. Verify Python Installation

1. Press **Win + R**, type `cmd`, press **Enter** to open Command Prompt
2. Type the following and press Enter:

```cmd
python --version
```

Expected output (version number may differ):
```
Python 3.12.3
```

3. Also verify pip is installed:

```cmd
pip --version
```

Expected output:
```
pip 24.0 from C:\Users\...\pip (python 3.12)
```

✅ If you see version numbers, Python is correctly installed.

---

## 4. Download the Project

### Option A — Using Git (Recommended)

If you have Git installed ([download here](https://git-scm.com/download/win)):

```cmd
git clone <your-repo-url>
```

### Option B — Download as ZIP

1. Go to the GitHub repository page
2. Click the green **"Code"** button → **"Download ZIP"**
3. Extract the ZIP file to a folder, e.g.:  
   `C:\Users\YourName\Documents\text_encryption`

---

## 5. Open Command Prompt

1. Press **Win + R**, type `cmd`, press **Enter**
2. Navigate to the project folder using the `cd` command:

```cmd
cd C:\Users\YourName\Documents\text_encryption
```

> Replace `C:\Users\YourName\Documents\text_encryption` with the actual path where you saved the project.

**Tip:** You can copy the folder path from File Explorer's address bar.

Confirm you are in the right folder:

```cmd
dir
```

You should see files like `requirements.txt`, `README.md`, and a folder called `secure_app`.

---

## 6. Create a Virtual Environment

A virtual environment keeps the project's dependencies isolated from the rest of your system.

Run this command:

```cmd
python -m venv venv
```

This creates a new folder called `venv` inside the project directory.

> ⏳ This may take 10–20 seconds.

---

## 7. Activate the Virtual Environment

Run this command:

```cmd
venv\Scripts\activate
```

You will know it worked when your command prompt changes to show `(venv)` at the beginning:

```
(venv) C:\Users\YourName\Documents\text_encryption>
```

> ⚠️ You must activate the virtual environment **every time** you open a new Command Prompt to run this project.

### If activation is blocked (PowerShell users only)

If you use PowerShell and see a security error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

---

## 8. Install Dependencies

With the virtual environment activated, run:

```cmd
pip install -r requirements.txt
```

This installs:
- `Flask` — the web server framework
- `cryptography` — for RSA-2048 encryption
- `Werkzeug` — for secure password hashing

> ⏳ This may take 1–3 minutes depending on your internet connection.

Expected final output:
```
Successfully installed Flask-x.x cryptography-x.x Werkzeug-x.x ...
```

---

## 9. Run the Application

Make sure your virtual environment is still active (you see `(venv)` in the prompt), then run:

```cmd
python secure_app\app.py
```

Expected output:

```
Initializing database at: C:\Users\YourName\...\database.db
Database initialized successfully ✅
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

> ✅ The database is **automatically created** on first run. You do not need to do anything extra.

---

## 10. Open in Browser

1. Open **Chrome**, **Edge**, or **Firefox**
2. In the address bar, type:

```
http://127.0.0.1:5000
```

3. Press **Enter**

You should see the **SecureVault** landing page! 🎉

### First-Time Setup

1. Click **Register** — create your account
2. Click **Login** — sign in with your credentials
3. Click **Encrypt Text** — type any message and encrypt it
4. Click **Decrypt Text** — paste the cipher text to decrypt
5. Click **View Report** — see your full encryption history

---

## 11. How to Stop the Server

Go back to the Command Prompt window and press:

```
Ctrl + C
```

The server will stop. You can close the Command Prompt after that.

---

## 12. Troubleshooting

### ❌ `'python' is not recognized as an internal or external command`

**Cause:** Python was not added to PATH during installation.

**Fix:**
1. Uninstall Python from *Control Panel → Programs*
2. Re-download from python.org
3. **Check "Add python.exe to PATH"** before clicking Install Now
4. Reopen Command Prompt and try again

---

### ❌ `'pip' is not recognized`

**Cause:** pip is missing or PATH is not set.

**Fix:**
```cmd
python -m pip install --upgrade pip
```

---

### ❌ `venv\Scripts\activate` gives an error

**Cause:** Windows execution policy blocks scripts.

**Fix (run in PowerShell as Administrator):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ `ModuleNotFoundError: No module named 'flask'`

**Cause:** Virtual environment is not activated.

**Fix:** Activate the virtual environment first:
```cmd
venv\Scripts\activate
```
Then run the app again.

---

### ❌ `Address already in use` or `Port 5000 is in use`

**Cause:** Another program is already using port 5000 (common on Windows — AirPlay uses 5000 sometimes).

**Fix:** Edit `secure_app\app.py`, last line, change the port:
```python
app.run(debug=True, port=5001)
```
Then access the app at `http://127.0.0.1:5001`

---

### ❌ Decryption says "Decryption Failed" after restarting

**Cause:** RSA keys are generated fresh every time the server starts. Old cipher text cannot be decrypted with new keys.

**Fix:** Always encrypt and decrypt within the **same server session**. Do not restart the server between encrypting and decrypting.

---

### ❌ Blank or broken page in browser

**Cause:** Static files may not be loading.

**Fix:**
1. Clear browser cache (`Ctrl + Shift + Delete`)
2. Hard refresh the page (`Ctrl + Shift + R`)

---

## ✅ Quick Reference Cheat Sheet

```cmd
:: Navigate to project
cd C:\path\to\text_encryption

:: Activate virtual environment (every time)
venv\Scripts\activate

:: Install packages (first time only)
pip install -r requirements.txt

:: Run the app
python secure_app\app.py

:: Open in browser
http://127.0.0.1:5000

:: Stop the server
Ctrl + C

:: Deactivate venv (when done)
deactivate
```

---

## 📞 Need Help?

If you are still stuck, check:
- Python official docs: https://docs.python.org/3/
- Flask docs: https://flask.palletsprojects.com/
- Open an issue on the GitHub repository
