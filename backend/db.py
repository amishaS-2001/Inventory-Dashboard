import sqlite3

def connect_db():
    return sqlite3.connect("inventory.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER,
        last_updated TEXT
    )
    """)
    conn.commit()
    conn.close()
