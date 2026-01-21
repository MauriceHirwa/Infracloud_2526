from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash

import db  # 👈 your database module

microweb_app = Flask(__name__)

# Init DB at startup
db.init_db()

# ------------------------------------------------------
# Routes
# ------------------------------------------------------
@microweb_app.route('/')
def main():
    return render_template("login.html")


@microweb_app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    if request.method == 'GET':
        return render_template("signup.html")

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return "Missing username or password\n", 400

    try:
        db.create_user(username, generate_password_hash(password))
    except Exception:
        return "Username already exists\n", 409

    return "Secure signup succeeded\n"


@microweb_app.route('/login/v2', methods=['POST'])
def login_v2():
    username = request.form.get('username')
    password = request.form.get('password')

    pw_hash = db.get_user_hash(username)
    if not pw_hash or not check_password_hash(pw_hash, password):
        return "Invalid username/password\n", 401

    db.update_last_login(username)
    user = db.get_user_info(username)

    return render_template("account.html", user=user)


@microweb_app.route('/update_pw/v2', methods=['GET', 'POST'])
def update_password():
    if request.method == 'GET':
        return render_template("update_pw.html")

    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    go_to_login = request.form.get('go_to_login')

    pw_hash = db.get_user_hash(username)
    if not pw_hash or not check_password_hash(pw_hash, old_password):
        return "Old password incorrect\n", 401

    db.update_password(username, generate_password_hash(new_password))

    if go_to_login == "1":
        return render_template(
            "login.html",
            message="Password updated successfully. Please log in."
        )

    return "Password updated successfully\n"


@microweb_app.route('/delete/all', methods=['POST', 'DELETE'])
def delete_all():
    db.delete_all_users()
    return "All test users deleted\n"


# ------------------------------------------------------
# Run
# ------------------------------------------------------
if __name__ == "__main__":
    microweb_app.run(
        host="0.0.0.0",
        port=5080,
        ssl_context="adhoc",
        debug=True
    )
