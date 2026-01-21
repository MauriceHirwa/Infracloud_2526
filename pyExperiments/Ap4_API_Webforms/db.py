import sqlite3
from datetime import datetime

DB_NAME = "user.db"

# ------------------------------------------------------
# Init + migration
# ------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_HASH (
            USERNAME TEXT PRIMARY KEY NOT NULL,
            HASH TEXT NOT NULL,
            CREATED_AT TEXT,
            PASSWORD_CHANGED_AT TEXT,
            LAST_LOGIN_AT TEXT
        )
    """)

    c.execute("PRAGMA table_info(USER_HASH)")
    cols = {row[1] for row in c.fetchall()}

    if "CREATED_AT" not in cols:
        c.execute("ALTER TABLE USER_HASH ADD COLUMN CREATED_AT TEXT")

    if "PASSWORD_CHANGED_AT" not in cols:
        c.execute("ALTER TABLE USER_HASH ADD COLUMN PASSWORD_CHANGED_AT TEXT")

    if "LAST_LOGIN_AT" not in cols:
        c.execute("ALTER TABLE USER_HASH ADD COLUMN LAST_LOGIN_AT TEXT")

    now = datetime.utcnow().isoformat()
    c.execute("UPDATE USER_HASH SET CREATED_AT = COALESCE(CREATED_AT, ?)", (now,))
    c.execute(
        "UPDATE USER_HASH SET PASSWORD_CHANGED_AT = COALESCE(PASSWORD_CHANGED_AT, CREATED_AT)"
    )

    conn.commit()
    conn.close()


# ------------------------------------------------------
# CRUD helpers
# ------------------------------------------------------
def create_user(username, password_hash):
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO USER_HASH
        (USERNAME, HASH, CREATED_AT, PASSWORD_CHANGED_AT, LAST_LOGIN_AT)
        VALUES (?, ?, ?, ?, ?)
        """,
        (username, password_hash, now, now, None)
    )
    conn.commit()
    conn.close()


def get_user_hash(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def update_last_login(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE USER_HASH SET LAST_LOGIN_AT = ? WHERE USERNAME = ?",
        (datetime.utcnow().isoformat(), username)
    )
    conn.commit()
    conn.close()


def update_password(username, new_hash):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        UPDATE USER_HASH
        SET HASH = ?, PASSWORD_CHANGED_AT = ?
        WHERE USERNAME = ?
        """,
        (new_hash, datetime.utcnow().isoformat(), username)
    )
    conn.commit()
    conn.close()


def get_user_info(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT USERNAME, CREATED_AT, PASSWORD_CHANGED_AT, LAST_LOGIN_AT
        FROM USER_HASH WHERE USERNAME = ?
    """, (username,))
    row = c.fetchone()
    conn.close()
    return row


def delete_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM USER_HASH")
    conn.commit()
    conn.close()
