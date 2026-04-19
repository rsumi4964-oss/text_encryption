import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)

    cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", 
                (username, hashed_password))

    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()

    if user:
        stored_password = user[2]

        if check_password_hash(stored_password, password):
            return user

    return None