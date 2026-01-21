from flask import Flask, request, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

microweb_app = Flask(__name__)

DB_NAME = "user.db"

# -------------------- Database Setup --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Cleartext table (for assignment demonstration)
    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_PLAIN (
            USERNAME TEXT PRIMARY KEY NOT NULL,
            PASSWORD TEXT NOT NULL
        )
    """)

    # Secure hashed table
    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_HASH (
            USERNAME TEXT PRIMARY KEY NOT NULL,
            HASH TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------- Delete All -------------------------
@microweb_app.route('/delete/all', methods=['POST', 'DELETE'])
def delete_all():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM USER_PLAIN")
    c.execute("DELETE FROM USER_HASH")

    conn.commit()
    conn.close()

    return "All test users deleted\n"


# ------------------ Signup v1 (plain text) ----------------
@microweb_app.route('/signup/v1', methods=['POST'])
def signup_v1():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
                  (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists (insecure table)\n"
    finally:
        conn.close()

    return "Signup successful (insecure)\n"


def verify_plain(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?", (username,))
    row = c.fetchone()
    conn.close()

    return row and row[0] == password


@microweb_app.route('/login/v1', methods=['POST'])
def login_v1():
    if verify_plain(request.form['username'], request.form['password']):
        return "Login success (insecure)\n"
    return "Invalid username/password\n"


# ------------------ Signup v2 (secure hash) ----------------
@microweb_app.route('/signup/v2', methods=['POST'])
def signup_v2():
    username = request.form['username']
    password = request.form['password']

    hashed_pw = generate_password_hash(password)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)",
                  (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists\n"
    finally:
        conn.close()

    return "Secure signup succeeded\n"


def verify_hash(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    row = c.fetchone()
    conn.close()

    return row and check_password_hash(row[0], password)


@microweb_app.route('/login/v2', methods=['POST'])
def login_v2():
    if verify_hash(request.form['username'], request.form['password']):
        return "Login success (secure hash)\n"
    return "Invalid username/password\n"


# ------------------ Render Login Page ---------------------
@microweb_app.route('/')
def main():
    return render_template("login.html")

# ------------------ Render account Page ---------------------
@microweb_app.route('/account')
def account_page():
    return render_template("account.html")


# ------------------ Launch -------------------------------
if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5555, ssl_context='adhoc')