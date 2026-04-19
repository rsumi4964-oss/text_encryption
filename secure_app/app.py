import os
import sys
import sqlite3
import base64
import csv
import io

# Ensure secure_app/ is on the path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import (
    Flask, render_template, request,
    redirect, session, jsonify, Response
)
from config import DB_PATH, TEMPLATE_DIR, STATIC_DIR
from crypto_utils import encrypt, decrypt
from auth import create_user, validate_user
from init_db import init_db

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)
app.secret_key = "supersecretkey_change_in_production"

# ── Auto-initialize DB on startup ────────────────────────────────────────────
init_db()


# ── Helper ────────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        try:
            create_user(username, password)
            return redirect("/login")
        except Exception:
            error = "Username already exists. Please choose another."
    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = validate_user(username, password)
        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            error = "Invalid credentials. Please try again."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM messages WHERE user=?",
                         (session["user"],)).fetchone()[0]
    conn.close()
    return render_template("dashboard.html", user=session["user"],
                           total_encryptions=total)


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt_page():
    if "user" not in session:
        return redirect("/login")

    result = None
    if request.method == "POST":
        text = request.form["text"]
        cipher_bytes = encrypt(text)
        cipher_text = base64.b64encode(cipher_bytes).decode()

        conn = get_db()
        conn.execute(
            "INSERT INTO messages(user, original_text, data) VALUES(?, ?, ?)",
            (session["user"], text, cipher_text)
        )
        conn.commit()
        conn.close()
        result = cipher_text

    return render_template("encrypt.html", result=result)


@app.route("/decrypt", methods=["GET", "POST"])
def decrypt_page():
    if "user" not in session:
        return redirect("/login")

    result = None
    error = None
    if request.method == "POST":
        cipher_text = request.form["text"].strip()
        try:
            cipher_bytes = base64.b64decode(cipher_text.encode())
            plain_text = decrypt(cipher_bytes)
            result = plain_text
        except Exception:
            error = "Decryption failed. Make sure you paste a valid cipher text."

    return render_template("decrypt.html", result=result, error=error)


@app.route("/report")
def report():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    messages = conn.execute(
        "SELECT id, user, original_text, data, timestamp FROM messages ORDER BY timestamp DESC"
    ).fetchall()

    total_count = len(messages)
    unique_users = conn.execute(
        "SELECT COUNT(DISTINCT user) FROM messages"
    ).fetchone()[0]

    user_count = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE user=?", (session["user"],)
    ).fetchone()[0]

    conn.close()
    return render_template(
        "report.html",
        messages=messages,
        total_count=total_count,
        unique_users=unique_users,
        user_count=user_count,
        current_user=session["user"]
    )


@app.route("/report/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id=?", (msg_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/report/export")
def export_csv():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    messages = conn.execute(
        "SELECT id, user, original_text, data, timestamp FROM messages ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User", "Original Text", "Cipher Text", "Timestamp"])
    for m in messages:
        writer.writerow([m["id"], m["user"], m["original_text"], m["data"], m["timestamp"]])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=encryption_report.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)