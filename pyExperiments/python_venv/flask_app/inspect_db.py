
import sqlite3
import os

# Full path to your actual database
db_path = os.path.join(os.path.dirname(__file__), "user.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in DB:", tables)

# Query USER_HASH (change to USER_PLAIN if needed)
table_name = "USER_HASH"

try:
    cursor.execute(f'SELECT * FROM "{table_name}";')
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print("\nRows as dicts (column -> value):")
    for row in rows:
        print(dict(zip(columns, row)))

except sqlite3.OperationalError as e:
    print("Error:", e)

# Close connection
cursor.close()
conn.close()

print("\n" + "-" * 40)
print("Done")
print("-" * 40)
print("Connection closed.")