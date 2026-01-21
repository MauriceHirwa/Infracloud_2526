from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db_name = "user.db"


def get_db_connection():
    """Opent een verbinding met SQLite."""
    return sqlite3.connect(db_name)


def ensure_tables_exist():
    """Maakt de tabel voor gehashte accounts aan als die nog niet bestaat."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_HASHED (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL UNIQUE,
            PASSWORD_HASH TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    ensure_tables_exist()

    if request.method == 'GET':
        return render_template("signup_v2.html", error_msg="")

    username_entered = request.form.get('username', '').strip()
    password_entered = request.form.get('password', '')

    if not username_entered or not password_entered:
        return render_template("signup_v2.html", error_msg="Username en password zijn verplicht.")
    if len(username_entered) < 3:
        return render_template("signup_v2.html", error_msg="Username moet minstens 3 karakters zijn.")
    if len(password_entered) < 6:
        return render_template("signup_v2.html", error_msg="Password moet minstens 6 karakters zijn.")

    password_hash = generate_password_hash(password_entered)

    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO USER_HASHED (USERNAME, PASSWORD_HASH) VALUES (?, ?)",
            (username_entered, password_hash)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return render_template("signup_v2.html", error_msg="Deze username bestaat al. Kies een andere.")

    # ✅ Simpel succesbericht (geen HTML success page)
    return "Secure successful", 201


@app.route('/', methods=['GET', 'POST'])
def login():
    ensure_tables_exist()

    if request.method == 'GET':
        return render_template("login.html", error_msg="")

    username_entered = request.form.get('username', '').strip()
    password_entered = request.form.get('password', '')

    if not username_entered or not password_entered:
        return render_template("login.html", error_msg="Missing username or password")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT PASSWORD_HASH FROM USER_HASHED WHERE USERNAME = ?", (username_entered,))
    row = c.fetchone()
    conn.close()

    if row is None:
        return render_template("login.html", error_msg="Invalid username or password")

    if not check_password_hash(row[0], password_entered):
        return render_template("login.html", error_msg="Invalid username or password")

    # ✅ Simpel succesbericht (geen HTML success page)
    return "Login successful", 200


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    ensure_tables_exist()

    if request.method == 'GET':
        return render_template("forgot_password.html", error_msg="")

    username_entered = request.form.get('username', '').strip()

    if not username_entered:
        return render_template("forgot_password.html", error_msg="Username is verplicht.")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM USER_HASHED WHERE USERNAME = ?", (username_entered,))
    row = c.fetchone()
    conn.close()

    if row is None:
        return render_template("forgot_password.html", error_msg="Deze username bestaat niet.")

    return redirect(url_for('reset_password', username=username_entered))


@app.route('/reset-password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    ensure_tables_exist()

    if request.method == 'GET':
        return render_template("reset_password.html", error_msg="", username=username)

    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not new_password or not confirm_password:
        return render_template("reset_password.html",
                               error_msg="Beide velden zijn verplicht.",
                               username=username)

    if len(new_password) < 6:
        return render_template("reset_password.html",
                               error_msg="Password moet minstens 6 karakters zijn.",
                               username=username)

    if new_password != confirm_password:
        return render_template("reset_password.html",
                               error_msg="Passwords komen niet overeen.",
                               username=username)

    new_hash = generate_password_hash(new_password)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE USER_HASHED SET PASSWORD_HASH = ? WHERE USERNAME = ?",
        (new_hash, username)
    )
    conn.commit()

    updated_rows = c.rowcount
    conn.close()

    if updated_rows == 0:
        return render_template("reset_password.html",
                               error_msg="User bestaat niet (meer).",
                               username=username)

    # ✅ Simpel succesbericht (geen HTML success page)
    return "Reset successful", 200


if __name__ == "__main__":
    app.run(debug=True)
