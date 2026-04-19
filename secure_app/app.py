from flask import Flask, render_template, request, redirect, session
from crypto_utils import encrypt, decrypt
from auth import create_user, validate_user
import sqlite3
import base64

app = Flask(__name__, template_folder='templates')
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        create_user(username, password)
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = validate_user(username, password)

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt_page():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        text = request.form["text"]

        cipher_bytes = encrypt(text)
        cipher_text = base64.b64encode(cipher_bytes).decode()

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO messages(data) VALUES(?)", (cipher_text,))
        conn.commit()
        conn.close()

        return render_template("encrypt.html", result=cipher_text)

    return render_template("encrypt.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt_page():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        cipher_text = request.form["text"]

        try:
            cipher_bytes = base64.b64decode(cipher_text.encode())
            plain_text = decrypt(cipher_bytes)
            return render_template("decrypt.html", result=plain_text)
        except:
            return "Decryption Failed ❌"

    return render_template("decrypt.html")

if __name__ == "__main__":
    app.run(debug=True)